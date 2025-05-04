# Makefile for MCP server for generating Stock charts

clean:
	rm -rf tmp/*.png
	rm -rf tmp/*.csv
	rm -rf src/__pycache__/
	docker rmi spitson/mcp-create-timeseries-chart

build:
	docker build -t spitson/mcp-create-timeseries-chart .
push:
	docker push spitson/mcp-create-timeseries-chart
exec: 
	docker run -it --rm spitson/mcp-create-timeseries-chart

run:
	uv run python main.py
