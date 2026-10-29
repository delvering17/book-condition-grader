import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package", ROOT / "scripts/package.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))

    def tearDown(self):
        self.temp.cleanup()

    def test_archives_are_portable_complete_and_exclude_private_data(self):
        (self.root / ".env").write_text("PRIVATE_FIXTURE=never-publish")
        private = self.root / "evals/private"
        private.mkdir()
        (private / "photo.jpg").write_bytes(b"private")
        (self.root / package.SKILL_DIR / "private-photo.jpg").write_bytes(b"private")
        products = package.build(self.root)
        with zipfile.ZipFile(products[0]) as archive:
            names = set(archive.namelist())
            self.assertIn("plugin.json", names)
            self.assertIn("GRADING.md", names)
            self.assertIn("skills/book-condition-grader/SKILL.md", names)
            self.assertIn("assets/book.svg", names)
            self.assertNotIn(".env", names)
            self.assertFalse(any(p.endswith(".jpg") for p in names))
            self.assertFalse(any("private" in p or ".git" in p or "__pycache__" in p for p in names))
        with zipfile.ZipFile(products[1]) as archive:
            names = set(archive.namelist())
            self.assertIn("book-condition-grader/SKILL.md", names)
            for ref in package.REFERENCES:
                self.assertIn(f"book-condition-grader/references/{ref}", names)

    def test_build_is_reproducible_and_checksums_match(self):
        products = package.build(self.root)
        before = {p.name: p.read_bytes() for p in products}
        products = package.build(self.root)
        self.assertEqual(before, {p.name: p.read_bytes() for p in products})
        for line in (self.root / "dist/SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ")
            self.assertEqual(digest, hashlib.sha256((self.root / "dist" / name).read_bytes()).hexdigest())

    def test_standalone_contains_both_references(self):
        text = package.standalone(self.root)
        for ref in package.REFERENCES:
            content = (self.root / package.SKILL_DIR / "references" / ref).read_text()
            self.assertIn(content, text)
            self.assertNotIn(f"(references/{ref})", text)

    def test_missing_reference_stops_build(self):
        (self.root / package.SKILL_DIR / "references" / package.REFERENCES[0]).unlink()
        with self.assertRaises(ValueError):
            package.build(self.root)

    def test_stale_link_guide_stops_build_until_regenerated(self):
        reference = self.root / package.SKILL_DIR / "references" / package.REFERENCES[0]
        reference.write_text(reference.read_text() + "\n개정된 적용 안내.\n")
        with self.assertRaises(ValueError):
            package.build(self.root)
        package.write_guide(self.root)
        package.build(self.root)

    def test_repository_home_contains_complete_rules_without_following_links(self):
        package.write_guide(self.root)
        readme = (self.root / "README.md").read_text()
        for ref in package.REFERENCES:
            content = (self.root / package.SKILL_DIR / "references" / ref).read_text()
            self.assertIn(content, readme)
        self.assertNotIn("**예상등급: [등급", readme)

    def test_tampered_home_page_rules_stop_build_until_regenerated(self):
        destination = self.root / "README.md"
        destination.write_text(destination.read_text().replace("찢김≤2cm", "찢김≤20cm"))
        with self.assertRaises(ValueError):
            package.build(self.root)
        package.write_guide(self.root)
        package.build(self.root)

    def test_missing_or_escaping_icon_stops_build(self):
        manifest_path = self.root / "plugin.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["extensions"]["com.openai"]["interface"]["logo"] = "./../outside.svg"
        (self.root.parent / "outside.svg").write_text("<svg/>")
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            package.build(self.root)

    def test_evaluation_cannot_pass_without_evidence(self):
        destination = self.root / "evals/results.json"
        results = json.loads(destination.read_text())
        results["cases"][0]["status"] = "passed"
        destination.write_text(json.dumps(results))
        with self.assertRaises(ValueError):
            package.validate(self.root)

    def test_duplicate_scenarios_are_rejected(self):
        destination = self.root / "evals/test-cases.json"
        scenarios = json.loads(destination.read_text())
        scenarios["cases"][1]["id"] = scenarios["cases"][0]["id"]
        destination.write_text(json.dumps(scenarios))
        with self.assertRaises(ValueError):
            package.validate(self.root)


if __name__ == "__main__":
    unittest.main()
