#!/bin/bash


uv run \
fastapi dev --entrypoint src.to_do_list_api.main:app
