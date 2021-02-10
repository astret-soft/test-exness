PYTHON = python3

.PHONY = help setup test lint clean serve
.DEFAULT_GOAL = help

help:
	@echo "setup - установка виртуального окружения и необходимых модулей"
	@echo "test - запуск автотестов"
	@echo "lint - запуск линтера"
	@echo "clean - очистка проекта от временных файлов"
	@echo "serve - запуск сервиса"

setup:
	@echo "Setup..."
	${PYTHON} -m venv venv
	( \
	echo "pip install -r requirements.txt" > source venv/bin/activate; \
	)

test:
	${PYTHON} -m pytest
lint:
	@pylint constants.py main.py models.py

clean:
	@rm -rf build dist *.egg-info

serve:
	${PYTHON} -m uvicorn main:app --reload
