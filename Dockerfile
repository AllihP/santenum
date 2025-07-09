# Dockerfile
# Choisissez une image de base Python
FROM python:3.13.4-slim-bullseye

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Rendre le script entrypoint.sh exécutable
RUN chmod +x entrypoint.sh

# Exposer le port que Gunicorn va écouter
EXPOSE 8000 # Ou le port que Render alloue, mais 8000 est un standard pour Django

# Définir le point d'entrée (entrypoint.sh) pour l'exécution du conteneur
ENTRYPOINT ["./entrypoint.sh"]
