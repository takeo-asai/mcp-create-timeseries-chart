# Makefile for generating SVG files from Python scripts

clean:
	rm -rf *.svg
	rm -rf *.csv

run:
	uv run python main.py
