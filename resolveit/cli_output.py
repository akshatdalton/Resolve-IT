from typing import Dict, List, Union

from urwid import (
    AttrMap,
    Button,
    Divider,
    ExitMainLoop,
    Frame,
    LineBox,
    ListBox,
    MainLoop,
    Overlay,
    Padding,
    SimpleFocusListWalker,
    Text,
    WidgetPlaceholder,
    connect_signal,
)

from resolveit.fetch_results import get_question_and_answers
from resolveit.resolveit_types import Answer, Question


class CascadingBoxes(WidgetPlaceholder):
    def open_box(self, box: Union[ListBox, Padding]) -> None:
        self.original_widget: Frame
        self.original_widget = Overlay(
            top_w=LineBox(box),
            bottom_w=self.original_widget,
            align="center",
            # These are in percentage.
            width=("relative", 100),
            valign="middle",
            height=("relative", 100),
        )


class Interface(object):
    def __init__(self, search_results: List[Dict[str, str]]) -> None:
        self.search_results = search_results
        self.palette = [("reversed", "standout", "")]
        self.footer = Text(
            [
                "\n",
                ("menu", " ENTER "),
                ("light gray", " View answers "),
                ("menu", " Q "),
                ("light gray", " Quit"),
            ]
        )

        # This will be used to toggle between search result and answers interface.
        self.viewing_answers = False

        self.main = Padding(self.create_menu(), left=2, right=2)
        self.layout = Frame(self.main, footer=self.footer)
        self.top = CascadingBoxes(self.layout)
        self.main_loop = MainLoop(
            self.top, palette=self.palette, unhandled_input=self.handle_input
        )

    def display_interface(self) -> None:
        self.main_loop.run()

    def create_menu(self) -> ListBox:
        body = [Text("Resolve-IT"), Divider("-")]
        for result in self.search_results:
            button = Button(f'{result["title"]} (Votes: {result["votes"]})')
            connect_signal(button, "click", self.handle_chosen_result, result["link"])
            body.append(AttrMap(button, None, focus_map="reversed"))
        return ListBox(SimpleFocusListWalker(body))

    def handle_chosen_result(self, button: Button, result_link: str) -> None:
        self.viewing_answers = True
        result = get_question_and_answers(result_link)
        question = result["question"]
        answers = result["answers"]
        result_body = []
        result_body.extend(self.stylize_question(question))
        for answer in answers:
            result_body.extend(self.stylize_answer(answer))
        self.top.open_box(ListBox(SimpleFocusListWalker(result_body)))

    def stylize_question(self, question: Question) -> List[Union[Divider, Text]]:
        question_body = [Divider("-")]
        question_body.append(Text(question.title))
        question_body.append(Divider("-"))
        question_body.append(Text([question.description, "\n"]))
        question_body.append(Divider("*"))
        if question.tags is not None:
            tags = "Tags: " + " ".join(question.tags)
            question_body.append(Text(f"{tags} Votes: {question.votes}"))
        else:
            question_body.append(Text(f"Votes: {question.votes}"))
        question_body.append(Divider("*"))
        question_body.append(Divider("="))
        return question_body

    def stylize_answer(self, answer: Answer) -> List[Union[Divider, Text]]:
        answer_body = [Text([answer.description, "\n"])]
        answer_body.append(Divider("*"))
        answer_body.append(Text(f"Votes: {answer.votes}"))
        answer_body.append(Divider("*"))
        answer_body.append(Divider("="))
        return answer_body

    def exit_program(self, button: Button) -> None:
        raise ExitMainLoop()

    def handle_input(self, input: str) -> None:
        if input in ["esc", "backspace"]:
            if self.viewing_answers:
                self.viewing_answers = False
                self.top.open_box(self.main)
            else:
                raise ExitMainLoop()
        elif input in ["q", "Q"]:
            raise ExitMainLoop()
