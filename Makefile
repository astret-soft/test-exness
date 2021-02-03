PYTHON = python3

.PHONY = help setup test lint clean
.DEFAULT_GOAL = help

help:
  @echo "setup - установка виртуального окружения и необходимых модулей"
  @echo "test - запуск автотестов"
  @echo "lint - запуск линтера"
  @echo "clean - очистка проекта от временных файлов"

setup:
  @echo "Setup..."
  ${PYTHON} -m venv venv
  ( \
    echo "pip install -r requirements.txt" > source venv/bin/activate; \
    )

test:
  ${PYTHON} -m pytest -n auto --dist loadscope --html=report.html

lint:
  @pylint constants.py main.py models.py

clean:
  @rm -rf build dist *.egg-info
