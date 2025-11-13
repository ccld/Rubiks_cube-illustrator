FROM python:3.11-slim

# Install minimal system deps for many scientific packages and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libfreetype6-dev \
    libpng-dev \
    fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser/app
USER appuser

# Copy only requirements first to leverage Docker cache
COPY --chown=appuser:appuser requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY --chown=appuser:appuser . .

# Use headless backend for matplotlib
ENV MPLBACKEND=Agg \
    PYTHONUNBUFFERED=1

# Default command: run the main script (adjust if your main is different)
ENTRYPOINT ["python", "Rubiks_illustrator.py"]
