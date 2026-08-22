FROM manimcommunity/manim:v0.20.1

WORKDIR /manim
COPY pyproject.toml README.md /tmp/jp-standard/
COPY src /tmp/jp-standard/src
RUN python -m pip install --no-cache-dir /tmp/jp-standard

ENV PYTHONUNBUFFERED=1
