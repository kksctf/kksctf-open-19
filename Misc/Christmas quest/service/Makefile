TEMPLATE_NAME="quest"
TEMPLATE_PORT="8005"
VARS=COMPOSE_PROJECT_NAME=${TEMPLATE_NAME} TEMPLATE_NAME=${TEMPLATE_NAME} TEMPLATE_PORT=${TEMPLATE_PORT}
SH = ${TEMPLATE_NAME} # `sed -n '3{p;q;}' docker-compose.yml | cut -f1 -d':'`

.PHONY: shell libc run restart start build stop down status

all: run
	
shell:
	docker exec -it $(SH) bash

libc: # get libc from container
	mkdir -p libc
	docker exec $(SH) bash -c "rm -rf /tmp/libc"
	
	docker exec $(SH) bash -c "mkdir -p /tmp/libc/64"
	docker exec $(SH) bash -c "cp /lib/x86_64-linux-gnu/ld-*.so  /tmp/libc/64"
	docker exec $(SH) bash -c "cp /lib/x86_64-linux-gnu/libc-*.so  /tmp/libc/64"
	docker cp $(SH):/tmp/libc/64 libc/64/

	docker exec $(SH) bash -c "mkdir -p /tmp/libc/32"
	docker exec $(SH) bash -c "cp /lib32/ld-*.so  /tmp/libc/32"
	docker exec $(SH) bash -c "cp /lib32/libc-*.so  /tmp/libc/32"
	docker cp $(SH):/tmp/libc/32 libc/32/

	docker exec $(SH) bash -c "rm -rf /tmp/libc"

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
