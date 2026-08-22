#!/bin/bash



# Create the container if it doesn't exist
if [[ ! "$(docker container ls --all --quiet --filter name=taskdb)" ]]; then
    docker run \
        --name taskdb \
        --volume taskdata:/var/lib/postgresql/data \
        --env-file .env \
        --publish 4321:5432 \
        --detach \
        postgres:16-trixie
else
    docker start taskdb
fi


if [[ DEBUG -eq 1 ]]; then
    .venv/bin/fastapi dev --entrypoint src.to_do_list_api.main:app
else
    .venv/bin/fastapi run --entrypoint src.to_do_list_api.main:app
fi
