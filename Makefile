SHELL := /bin/bash

up:
	docker compose -f docker-compose.prod.yml up -d

down:
	docker compose -f docker-compose.prod.yml down

logs:
	docker compose -f docker-compose.prod.yml logs -f --tail=200

ps:
	docker compose -f docker-compose.prod.yml ps

backup:
	bash deploy/backup.sh backups

restore:
	bash deploy/restore.sh $(SQL) $(RDB)
