import random

from jinja2 import Environment, FileSystemLoader
from yaml import Loader, load

ticket_counter = 0
remaining_questions = list()


class Questions_count_wrong(Exception):
    def __init__(self, questions_size, count_per_ticket):
        super().__init__('multiplication of questions count per ticket and '
                         'tickets count must be equal size of question list\n'
                         f'{questions_size} != {count_per_ticket}')


class Questions_amount_per_ticket_is_wrong(Exception):
    def __init__(self, questions_size, qcpt_mul_tc):
        super().__init__('modulo divide of count of questions and questions '
                         'count per ticket must be  should be 0\n'
                         f'{questions_size} % {qcpt_mul_tc} !=0')


def validate_data(data: dict) -> None:
    if len(data['questions']) % data['questions_count_per_ticket'] != 0:
        raise Questions_amount_per_ticket_is_wrong(len(data['questions']), data['questions_count_per_ticket'])
    if len(data['questions']) != data['questions_count_per_ticket'] * data['tickets_count']:
        raise Questions_count_wrong(len(data['questions']), data['questions_count_per_ticket'] * data['tickets_count'])


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


def main():
    with open("data.yaml", encoding="utf-8") as f:
        data = load(f, Loader=Loader)

    validate_data(data)

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
