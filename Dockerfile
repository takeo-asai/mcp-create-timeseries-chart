FROM ghcr.io/astral-sh/uv:python3.13-bookworm

# フォントインストール
RUN wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip -O /tmp/fonts_noto.zip && \
    mkdir -p /usr/share/fonts &&\
    unzip /tmp/fonts_noto.zip -d /usr/share/fonts

ADD .python-version ./python-version
ADD pyproject.toml ./pyproject.toml
ADD uv.lock ./uv.lock
RUN uv sync

ADD main.py ./main.py
ADD src/ ./src/
ADD tmp/ ./tmp/
ADD docs/aapl-2y.png ./docs/aapl-2y.png

ENTRYPOINT [ "uv", "run", "python", "main.py" ]
CMD [ "--prod", "true" ]
