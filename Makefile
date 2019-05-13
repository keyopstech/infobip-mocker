start:
	docker-compose up -d --remove-orphans

stop:
	docker-compose down

log:
	docker-compose logs -f