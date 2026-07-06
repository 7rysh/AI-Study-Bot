FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p backend/uploads backend/chroma_db

EXPOSE 7860

COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]