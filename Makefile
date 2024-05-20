.PHONY: start stop

up:
	docker compose up -d

down:
	docker compose down

clean:
	make stop
	docker volume rm $(shell docker volume ls -qf dangling=true)
	docker rmi $(shell docker images -qf dangling=true)