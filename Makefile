.PHONY: up init down clean serve test up_without_faust up_faust start_airflow airflow_init stop_airflow build_faust build_scraper up_scraper up_faust_save_news build_faust_save_news

up:
	make up_without_faust
	make up_faust
	make up_scraper
	make start_airflow
	make serve

airflow_init:
	docker compose -f docker-compose_airflow.yaml up airflow-init

up_without_faust:
	docker compose -f compose.yaml up -d --remove-orphans $(filter-out faust,$(shell docker-compose -f compose.yaml config --services))

up_faust:
	make build_faust
	docker compose -f compose.yaml up -d faust

build_faust:
	docker compose -f compose.yaml build faust

build_faust_save_news:
	docker compose -f compose.yaml build faust_save_news

up_faust_save_news:
	make build_faust_save_news
	docker compose -f compose.yaml up -d faust_save_news

start_airflow:
	mkdir -p ./dags ./logs ./plugins ./config
	make airflow_init
	docker compose -f docker-compose_airflow.yaml up -d

build_scraper:
	docker compose -f compose.yaml build scraper

up_scraper:
	make build_scraper
	docker compose -f compose.yaml up -d scraper

down:
	docker compose -f docker-compose_airflow.yaml -f compose.yaml down

stop_airflow:
	docker compose -f docker-compose_airflow.yaml down

clean:
	make stop
	docker volume rm $(shell docker volume ls -qf dangling=true)
	docker rmi $(shell docker images -qf dangling=true)

serve:
	mkdir -p ./api/logs
	nohup uvicorn api.main:app --reload > ./api/logs/output.log 2>&1 &

test:
	while read line; do echo $$line | xargs http; done < test_main.http