.PHONY: build
build:
	docker-compose build

.PHONY: run
run:
	docker-compose run -p 5000:5000 -e PYTHONPATH=/code webserver python webserver/main.py
