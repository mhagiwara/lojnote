.PHONY: build
build:
	docker-compose build

.PHONY: test
test:
	docker-compose run -e PYTHONPATH=/code webserver pytest -s

.PHONY: run
run:
	docker-compose run -p 5000:5000 -e PYTHONPATH=/code webserver python webserver/main.py
