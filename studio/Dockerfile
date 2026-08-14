FROM node:20-bookworm

# Install Python dan dependency sistem buat Whisper + Chromium (Remotion)
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    ffmpeg \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Install Python dependencies
COPY requirements.txt ./
RUN pip3 install --break-system-packages -r requirements.txt

# Copy semua source code
COPY . .

# Install Chromium buat Remotion render
RUN npx remotion browser ensure

EXPOSE 5000
CMD ["python3", "app.py"]
