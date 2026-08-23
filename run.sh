#!/bin/bash


uv run fastapi dev --host 0.0.0.0 --port 8000 --entrypoint src.to_do_list_api.main:app
