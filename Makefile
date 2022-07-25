init:
	cp ./.env ./frontend/packages/api/.env
	cp ./.env ./frontend/packages/utils/.env
	cp ./.env ./frontend/packages/web-console/.env
	cp ./.env ./frontend/packages/web-shop/.env
	cp ./.env ./frontend/packages/web-mypage/.env
	cp ./.env ./frontend/packages/web-card/.env
	cp ./.env ./django/.env
	cp ./.env ./mysql/.env
	mkdir -p ./frontend/dist

up:
	docker-compose up -d

down:
	docker-compose stop

build:
	docker-compose build

rebuild:
	docker-compose build --no-cache
