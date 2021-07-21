import os
import sys
from typing import List
from unittest import TestCase, main

import orjson

RESOLVEIT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
sys.path.append(RESOLVEIT_PATH)

from resolveit.resolveit_types import Answer, Question
from resolveit.rparser import Parser


class TestResolveIT(TestCase):
    parsed_data = Parser("")

    @classmethod
    def setUpClass(cls) -> None:
        with open("tests/fixtures/stackoverflow.json", "rb") as f:
            stackoverflow_data = orjson.loads(f.read())["html"]
            cls.parsed_data = Parser(stackoverflow_data)

        super().setUpClass()

    def test_get_question_data(self) -> None:
        with open("tests/fixtures/question.json", "r") as f:
            expected_data = Question(**orjson.loads(f.read())["question"])

        self.assertEqual(self.parsed_data.get_question_data(), expected_data)

    def test_get_answers_data(self) -> None:
        expected_data: List[Answer] = []
        with open("tests/fixtures/answers.json", "r") as f:
            answers = orjson.loads(f.read())["answers"]
            for answer in answers:
                expected_data.append(Answer(**answer))

        self.assertEqual(self.parsed_data.get_answers_data(), expected_data)


if __name__ == "__main__":
    main()
