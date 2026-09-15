FROM python:3.12-slim
WORKDIR /workspace
COPY . .
RUN pip install --no-cache-dir . pytest jsonschema
CMD ["sh", "scripts/check.sh"]
