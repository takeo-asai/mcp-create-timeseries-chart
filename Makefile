# Makefile for generating SVG files from Python scripts

clean:
	rm -rf *.png
	rm -rf *.svg
	rm -rf *.csv

run:
	uv run python main.py
