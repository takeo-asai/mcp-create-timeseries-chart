FROM ghcr.io/astral-sh/uv:python3.13-bookworm

ADD .python-version ./python-version
ADD pyproject.toml ./pyproject.toml
ADD uv.lock ./uv.lock
RUN uv sync

ADD main.py ./main.py
ADD src/ ./src/

ENTRYPOINT [ "uv", "run", "python" ]
CMD [ "AAPL", "2yr", "--output", "output.svg" ]
