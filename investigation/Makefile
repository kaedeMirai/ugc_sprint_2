POETRY = ./.venv/bin/poetry


venv: ##@Env Init venv and install poetry dependencies
	@rm -rf .venv || true && \
	python3 -m venv .venv && \
	.venv/bin/pip install poetry && \
	${POETRY} install --no-root

build:
	docker build -t mongo_api -f ./docker/Dockerfile .

run:
	docker-compose -f docker-compose.yaml -f docker-compose.elk.yaml up -d --build

stop:
	docker-compose -f docker-compose.yaml -f docker-compose.elk.yaml down -v

run_with_uvicorn:
	uvicorn main:app --host=0.0.0.0 --port=8282 --log-config=/app/log_conf.yaml

run_tests:
	docker-compose -f docker-compose.yaml exec mongo_api_service python3 -m pytest -vv tests

pg_run:
	docker-compose -f docker-compose.postgres.yaml up -d --build

pg_stop:
	docker compose -f docker-compose.postgres.yaml down -v

pg_logs:
	docker compose -f docker-compose.postgres.yaml logs -f postgres