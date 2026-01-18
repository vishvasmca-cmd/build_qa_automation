FROM python:3.10-slim

# 1. Install System Deps for Playwright & Git
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup App
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Install Playwright Browsers
RUN playwright install --with-deps chromium

# 4. Copy Code
COPY . .

# 5. Permission fix for Hugging Face (Starts as user 1000)
RUN mkdir -p /app/projects && chmod -R 777 /app/projects
RUN mkdir -p /app/outputs && chmod -R 777 /app/outputs

# 6. Default Command (Example usage)
CMD ["python", "orchestrator.py", "--help"]
