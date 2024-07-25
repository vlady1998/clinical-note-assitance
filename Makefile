.PHONY: docker-build
docker-build:	## Build project with compose
	docker compose build

.PHONY: docker-up
docker-up:	## Run project with compose
	docker compose up --remove-orphans

.PHONY: docker-pull
docker-pull:	## Run project with compose
	docker compose pull

.PHONY: docker-down
docker-down:	## Run project with compose
	docker compose down
