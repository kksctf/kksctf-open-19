VARS=

.PHONY: run restart start build stop down status

all: run

run: down build start

restart: run

start:
	${VARS} docker-compose -f docker-compose.yml up -d

build:
	${VARS} docker-compose -f docker-compose.yml build

stop:
	${VARS} docker-compose -f docker-compose.yml stop

down:
	${VARS} docker-compose -f docker-compose.yml down

status:
	${VARS} docker-compose -f docker-compose.yml ps
