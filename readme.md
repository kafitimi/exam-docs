# Генерация программы и билетов для экзамена

**Механизм работы**

1. Преподаватель создает собственный **приватный** репозиторий.
2. Преподаватель заполняет:

* файл c данными по вопросам экзамена (data.yaml)
* файл шаблона для билетов экзамена (template_assignments.tex)
* файл шаблона для программы экзамена (template_program.tex)

После коммита GitHub Action должен сгенерировать в разделе Releases файлы pdf:

* программы экзамена (program.pdf)
* экзаменационных билетов (assignments.pdf)

**Ссылки для пользователя**

* [Учебник по LaTeX](https://en.wikibooks.org/wiki/LaTeX)
* [Что такое XeLaTeX](https://www.overleaf.com/learn/latex/XeLaTeX)
* [Учебник по Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)

**Ссылки для разработчика**

* [LaTeX.Online](https://latexonline.cc/)
* [GitHub Action Checkout](https://github.com/marketplace/actions/checkout)
* [GitHub Action GH Release](https://github.com/marketplace/actions/gh-release)
