#!/usr/bin/env python3
import argparse
import json
import re
from urllib.parse import urlencode

SEARCH_URL = "https://www.aladin.co.kr/shop/usedshop/wc2b_search.aspx"


def normalize_isbn(value):
    value = re.sub(r"^ISBN(?:-1[03])?\s*:?\s*", "", value.strip(), flags=re.I)
    value = re.sub(r"[\s-]", "", value).upper()
    if re.fullmatch(r"97[89][0-9]{10}", value):
        if sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(value)) % 10:
            raise ValueError("ISBN-13 체크 숫자가 맞지 않습니다")
        return value
    if re.fullmatch(r"[0-9]{9}[0-9X]", value):
        digits = [10 if digit == "X" else int(digit) for digit in value]
        if sum(digit * (10 - index) for index, digit in enumerate(digits)) % 11:
            raise ValueError("ISBN-10 체크 숫자가 맞지 않습니다")
        base = "978" + value[:9]
        check = (-sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(base))) % 10
        return base + str(check)
    raise ValueError("확인한 ISBN-10 또는 978/979로 시작하는 ISBN-13만 입력하세요")


def lookup_details(value):
    isbn = normalize_isbn(value)
    return {
        "isbn13": isbn,
        "url": SEARCH_URL + "?" + urlencode({"ActionType": "1", "SearchTarget": "All", "KeyWord": isbn}),
        "lookup_performed": False,
    }


def main():
    parser = argparse.ArgumentParser(description="ISBN을 검증하고 알라딘 팔기 조회 URL을 생성합니다. 네트워크 조회는 하지 않습니다.")
    parser.add_argument("isbn")
    args = parser.parse_args()
    try:
        result = lookup_details(args.isbn)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
