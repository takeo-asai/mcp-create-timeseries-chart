# Makefile for MCP server for generating Stack charts

clean:
	rm -rf *.png
	rm -rf *.svg
	rm -rf */*.csv
	rm -rf */__pycache__/
	docker rmi mcp-timeseries-server

build:
	docker build -t mcp-timeseries-server .
exec: 
	docker run -it --rm mcp-timeseries-server

run:
	uv run python main.py
