.PHONY: up init down clean serve test up_without_faust up_faust

up:
	make init
	make up_without_faust
	docker compose -f compose.yaml build
	make up_faust
	make serve

init:
	docker compose -f docker-compose_airflow.yaml up airflow-init

up_without_faust:
	docker compose -f docker-compose_airflow.yaml up -d
	docker compose -f compose.yaml up -d --remove-orphans $(filter-out faust,$(shell docker-compose -f compose.yaml config --services))

up_faust:
	docker compose -f compose.yaml up -d faust

down:
	docker compose -f docker-compose_airflow.yaml -f compose.yaml down

clean:
	make stop
	docker volume rm $(shell docker volume ls -qf dangling=true)
	docker rmi $(shell docker images -qf dangling=true)

serve:
	mkdir -p ./api/logs
	nohup uvicorn api.main:app --reload > ./api/logs/output.log 2>&1 &

test:
	while read line; do echo $$line | xargs http; done < test_main.http