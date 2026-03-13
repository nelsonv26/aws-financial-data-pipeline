FROM apache/superset:latest

USER root

#  Instalamos dentro del venv correcto (esto es lo que faltaba)
RUN . /app/.venv/bin/activate && \
    uv pip install \
        pyathena[pandas] \
        boto3

# (eliminé sqlalchemy-trino y sqlalchemy-athena porque no son necesarios
# y pueden causar conflictos. pyathena ya incluye el soporte SQLAlchemy)

USER superset