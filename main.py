from yaml import load, Loader
from jinja2 import Environment, FileSystemLoader
import random

ticket_counter = 0
remaining_questions = list()

class Questions_count_wrong(Exception):
    def __init__(self, questions_size, count_per_ticket):
        super().__init__(f'multiplication of questions count per ticket and tickets count must be equal size of question list\n{questions_size} != {count_per_ticket}')

class Questions_amount_per_ticket_is_wrong(Exception):
    def __init__(self, questions_size, qcpt_mul_tc):
        super().__init__(f'modulo divide of count of questions and questions count per ticket must be  should be 0\n{questions_size} % {qcpt_mul_tc} !=0')

def check_data_validity(data:dict):
    if len(data['questions']) % data['questions_count_per_ticket'] != 0:
        raise Questions_amount_per_ticket_is_wrong(len(data['questions']), data['questions_count_per_ticket'])
    if len(data['questions']) != data['questions_count_per_ticket'] * data['tickets_count']:
        raise Questions_count_wrong(len(data['questions']), data['questions_count_per_ticket'] * data['tickets_count'])

class Ticket():
    def __init__(self):
        self.id = 0
        self.questions = list()
    def __repr__(self) :
        return f'\'id\': {self.id}, \'questions\': {self.questions}'
    def __str__(self):
        return self.__repr__()    

def create_ticket(questions : list):
    global ticket_counter
    ticket = Ticket()
    ticket.id = ticket_counter + 1
    ticket_counter += 1
    ticket.questions = questions
    return ticket


def pick_random_questions(amount : int):
    global remaining_questions
    choices = random.sample(remaining_questions, k=amount)
    remaining_questions = list(set(remaining_questions).difference(set(choices)))
    return choices


def main():
    names = ("assignments", "program")

    with open("data.yaml", encoding="utf-8") as f:
        data = load(f, Loader=Loader)

    check_data_validity(data)

    global remaining_questions

    remaining_questions = data['questions']
    tickets = [ create_ticket(pick_random_questions(data['questions_count_per_ticket'])) for _ in range(data['tickets_count']) ]
    template_data = {
        'subject': data['subject'],
        'group': data['group'],
        'semester': data['semester'],
        'tickets': tickets,
        'all_questions' : data['questions']
    }
    
    env = Environment(loader=FileSystemLoader("."))
    for name in names:
        template = env.get_template(f"template_{name}.tex")
        template.stream(data=template_data).dump(f"{name}.tex", encoding="utf-8")


if __name__ == '__main__':
    main()