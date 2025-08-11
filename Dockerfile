# 1. Koristimo službeni Python image
FROM python:3.11-slim

# 2. Postavi radni direktorij unutar kontejnera
WORKDIR /app

# 3. Kopiraj requirements.txt i instaliraj ovisnosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Kopiraj ostatak projekta u kontejner
COPY . .

# 5. Postavi Flask varijable (ime app-a i debug mod)
ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0

# 6. Pokreni Flask server
CMD ["flask", "run"]

