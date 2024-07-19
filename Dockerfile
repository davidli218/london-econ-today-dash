FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

COPY . .

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

EXPOSE 8050

CMD [ "gunicorn", "--bind", "0.0.0.0:8050", "app.main:server" ]
