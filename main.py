import random

from jinja2 import Environment, FileSystemLoader
from yaml import Loader, load


def validate_data(k: int, t: int, n: int) -> None:
    """Проверка входных данных
    :param k: количество вопросов в билете
    :param t: количество билетов
    :param n: количество вопросов в банке
    """
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


def create_tickets(k: int, t: int, questions: list[str]) -> list[Ticket]:
    """Создание билетов
    :param k: количество вопросов в билете
    :param t: количество билетов
    :param questions: банк вопросов
    """
    # Перемешиваем вопросы в банке
    random.shuffle(questions)
    # Нарезаем вопросы на билеты
    return [
        Ticket(i + 1, questions[i * k: (i + 1) * k])
        for i in range(t)
    ]


def main() -> None:
    with open("data.yaml", encoding="utf-8") as f:
        data = load(f, Loader=Loader)

    k: int = data["questions_count_per_ticket"]
    t: int = data["tickets_count"]
    n = len(data["questions"])
    validate_data(k, t, n)

    template_data = {
        'subject': data['subject'],
        'semester': data['semester'],
        'direction': data['direction'],
        'profile': data['profile'],
        'date': data['date'],
        'tickets': create_tickets(k, t, data["questions"]),
        'all_questions': data['questions']
    }

    env = Environment(loader=FileSystemLoader("."))
    for name in ("assignments", "program"):
        template = env.get_template(f"template_{name}.tex")
        template_stream = template.stream(data=template_data)
        template_stream.dump(f"{name}.tex", encoding="utf-8")


if __name__ == '__main__':
    main()
