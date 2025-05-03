# Makefile for generating SVG files from Python scripts

clean:
	rm -rf *.png
	rm -rf *.svg
	rm -rf */*.csv
	rm -rf */__pycache__/

run:
	uv run python main.py
