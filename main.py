import random

from jinja2 import Environment, FileSystemLoader
from yaml import Loader, load

ticket_counter = 0
remaining_questions = list()


def validate_data(k: int, t: int, n: int) -> None:
    if k * t != n:
        raise Exception(
            "Несочетающееся количество вопросов!\n"
            f"Количество вопросов в билете: {k}\n"
            f"Количество билетов: {t}\n"
            f"Общее количество вопросов: {n}\n"
            f"{k} * {t} != {n}"
        )


class Ticket():
    def __init__(self, _id: int, _questions: list[str]) -> None:
        self.id = _id
        self.questions = _questions.copy()

    def __repr__(self) -> str:
        return f'\'id\': {self.id}, \'questions\': {self.questions}'

    def __str__(self) -> str:
        return self.__repr__()


def create_ticket(questions: list):
    global ticket_counter
    ticket_counter += 1
    ticket = Ticket(ticket_counter, questions)
    return ticket


def pick_random_questions(amount: int):
    global remaining_questions
    choices = random.sample(remaining_questions, k=amount)
    remaining_questions = list(set(remaining_questions) - set(choices))
    return choices


def main() -> None:
    with open("data.yaml", encoding="utf-8") as f:
        data = load(f, Loader=Loader)

    k: int = data["questions_count_per_ticket"]
    t: int = data["tickets_count"]
    n = len(data["questions"])
    validate_data(k, t, n)

    global remaining_questions

    remaining_questions = data['questions']
    tickets = [
        create_ticket(pick_random_questions(data['questions_count_per_ticket']))
        for _ in range(data['tickets_count'])
    ]
    template_data = {
        'subject': data['subject'],
        'group': data['group'],
        'semester': data['semester'],
        'tickets': tickets,
        'all_questions': data['questions']
    }

    env = Environment(loader=FileSystemLoader("."))
    for name in ("assignments", "program"):
        template = env.get_template(f"template_{name}.tex")
        template_stream = template.stream(data=template_data)
        template_stream.dump(f"{name}.tex", encoding="utf-8")


if __name__ == '__main__':
    main()
