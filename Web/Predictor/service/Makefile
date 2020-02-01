TEMPLATE_NAME="random_oracle"
TEMPLATE_PORT="20007"
VARS=COMPOSE_PROJECT_NAME=${TEMPLATE_NAME} TEMPLATE_NAME=${TEMPLATE_NAME} TEMPLATE_PORT=${TEMPLATE_PORT}
SH = ${TEMPLATE_NAME} # `sed -n '3{p;q;}' docker-compose.yml | cut -f1 -d':'`

.PHONY: shell libc run restart start build stop down status

all: run
	
shell:
	docker exec -it $(SH) bash

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

logs:
	${VARS} docker-compose -f docker-compose.yml logs -f
