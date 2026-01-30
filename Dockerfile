FROM python:3.11-slim

WORKDIR /app

# Install system deps (if needed) and pip
RUN apt-get update && apt-get install -y build-essential curl --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8501
EXPOSE 8501

CMD ["bash", "-lc", "streamlit run crm_app.py --server.port ${PORT} --server.address 0.0.0.0"]
