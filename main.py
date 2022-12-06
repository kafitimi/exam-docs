from yaml import load, Loader
from jinja2 import Environment, FileSystemLoader

names = ("assignments", "program")

with open("data.yaml", encoding="utf-8") as f:
    data = load(f, Loader=Loader)

env = Environment(loader=FileSystemLoader("."))
for name in names:
    template = env.get_template(f"template_{name}.tex")
    template.stream(data=data).dump(f"{name}.tex", encoding="utf-8")
