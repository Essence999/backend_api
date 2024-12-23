FROM python:3.11.9

WORKDIR /app

COPY pip.conf /etc/pip.conf
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src/ ./src/
# Adicionar o COPY certs para rodar em HTTPS
# COPY certs/ ./certs/
COPY static/ ./static/

EXPOSE 8000

# Roda o projeto em HTTPS
# CMD ["uvicorn", "src.main:app","--host", "0.0.0.0",  "--port", "8000", "--ssl-keyfile=certs/server.key", "--ssl-certfile=certs/server.crt"]

# Roda o projeto em HTTP
# CMD ["uvicorn", "src.main:app","--host", "0.0.0.0",  "--port", "8000"]
CMD ["fastapi", "run", "src/main.py", "--proxy-headers", "--port", "8000"]