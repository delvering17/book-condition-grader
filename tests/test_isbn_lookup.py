import importlib.util
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("isbn_lookup", ROOT / "skills/book-condition-grader/scripts/isbn_lookup.py")
isbn_lookup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(isbn_lookup)


class ISBNLookupTests(unittest.TestCase):
    def test_user_isbn_creates_exact_read_only_search_url(self):
        details = isbn_lookup.lookup_details("9791141691370")
        self.assertEqual(details["url"], "https://www.aladin.co.kr/shop/usedshop/wc2b_search.aspx?ActionType=1&SearchTarget=All&KeyWord=9791141691370")
        self.assertFalse(details["lookup_performed"])

    def test_normalizes_printed_label_spaces_and_hyphens(self):
        self.assertEqual(isbn_lookup.normalize_isbn("ISBN-13: 979-11-416-9137-0"), "9791141691370")

    def test_converts_valid_isbn10(self):
        self.assertEqual(isbn_lookup.normalize_isbn("0-306-40615-2"), "9780306406157")

    def test_accepts_x_only_as_isbn10_check_digit(self):
        self.assertEqual(isbn_lookup.normalize_isbn("ISBN: 0-8044-2957-x"), "9780804429573")
        with self.assertRaises(ValueError):
            isbn_lookup.normalize_isbn("X804429570")

    def test_rejects_bad_checksums_without_repairing_them(self):
        for value in ("9791141691371", "0306406153", "0804429570"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                isbn_lookup.normalize_isbn(value)

    def test_rejects_addons_other_barcodes_and_query_injection(self):
        for value in ("12345", "9791141691370 12345", "4006381333931", "9791141691370&ActionType=2", "979114169137O", "https://example.com"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                isbn_lookup.normalize_isbn(value)

    def test_query_contains_only_expected_parameters(self):
        url = urlsplit(isbn_lookup.lookup_details("0306406152")["url"])
        self.assertEqual(url.scheme, "https")
        self.assertEqual(url.netloc, "www.aladin.co.kr")
        self.assertEqual(parse_qs(url.query), {"ActionType": ["1"], "SearchTarget": ["All"], "KeyWord": ["9780306406157"]})


if __name__ == "__main__":
    unittest.main()
