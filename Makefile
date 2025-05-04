# Makefile for MCP server for generating Stock charts

clean:
	rm -rf tmp/*.png
	rm -rf tmp/*.csv
	rm -rf src/__pycache__/
	docker rmi mcp-timeseries-server

build:
	docker build -t mcp-timeseries-server .
exec: 
	docker run -it --rm mcp-timeseries-server

run:
	uv run python main.py
