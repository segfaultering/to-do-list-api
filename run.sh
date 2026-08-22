#!/bin/bash


if [[ DEBUG -eq 1 ]]; then
    uv run \
    fastapi dev --entrypoint src.to_do_list_api.main:app
else
    uv run \
    fastapi run --entrypoint src.to_do_list_api.src.main:app
fi
