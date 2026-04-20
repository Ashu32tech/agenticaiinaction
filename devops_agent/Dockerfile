FROM python:3.12-slim

WORKDIR /app

# Install system deps + kubectl
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl \
    && apt-get clean

# Copy project
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Optional but fine to keep
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

EXPOSE 8501

# ✅ IMPORTANT FIX
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]