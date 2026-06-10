FROM jupyterhub/jupyterhub:5.4.6

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --chmod=755 init.sh /init.sh
COPY requirements.txt /requirements.txt

RUN uv pip install --system --break-system-packages --no-cache-dir -r /requirements.txt
