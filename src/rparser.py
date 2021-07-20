import html
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from resolveit.resolveit_types import Answer, Question


class Parser(object):
    # Attribute values
    QUESTION = "question"
    ANSWERS = "answers"
    ANSWER = "answer"
    QUESTION_HEADER = "question-header"
    DESCRIPTION = "s-prose js-post-body"
    TAGS = "mt24 mb12"
    VOTES = "data-score"

    def __init__(self, content: str) -> None:
        self.soup = BeautifulSoup(content, "lxml")

    def get_question_data(self) -> Question:
        question_tree = self.soup.find("div", class_=self.QUESTION)
        question: Question = Question(
            title=self.get_question_header(),
            description=self.get_description(question_tree),
            tags=self.get_tags(question_tree),
            votes=self.get_votes(question_tree),
        )
        return question

    def get_answers_data(self) -> List[Answer]:
        answers_tree = self.soup.find("div", id=self.ANSWERS)
        answers_list: List[Answer] = []
        for answer_tree in answers_tree.find_all("div", class_=self.ANSWER):
            answer: Answer = Answer(
                description=self.get_description(answer_tree),
                votes=self.get_votes(answer_tree),
            )
            answers_list.append(answer)

        return answers_list

    def get_question_header(self) -> str:
        return html.unescape(
            self.soup.find("div", id=self.QUESTION_HEADER).h1.text.strip()
        )

    def get_description(self, soup_tree: Tag) -> str:
        return html.unescape(
            soup_tree.find("div", class_=self.DESCRIPTION).text.strip()
        )

    def get_tags(self, soup_tree: Tag) -> List[str]:
        tag_list: List[str] = []
        tags = soup_tree.find("div", class_=self.TAGS)
        for tag in tags.find_all("a", class_="post-tag"):
            tag_list.append(tag.text.strip())

        return tag_list

    def get_votes(self, soup_tree: Tag) -> int:
        return soup_tree[self.VOTES]
