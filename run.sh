#!/bin/bash


uv run \
fastapi run --entrypoint src.to_do_list_api.main:app
