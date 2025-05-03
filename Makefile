# Makefile for generating SVG files from Python scripts

clean:
	rm -rf output.svg

run:
	uv run python main.py
