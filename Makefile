.PHONY: build
build:
	docker-compose build

.PHONY: test
test:
	docker-compose run -e PYTHONPATH=/code webserver pytest -s

.PHONY: run
run:
	docker-compose up
