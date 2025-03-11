#!/bin/bash
docker compose down
docker compose up -d --build

docker compose exec nginx /bin/bash /code/install-nginx.sh
docker compose exec nginx supervisorctl restart all
