# Dockerfile

# 1. Image de base
# Utilisez une image Python officielle basée sur Debian Buster (léger et stable).
FROM python:3.10-slim-buster

# 2. Empêcher la mise en cache des index apt pour des raisons de sécurité
# et pour s'assurer que les paquets sont toujours à jour.
ENV DEBIAN_FRONTEND=noninteractive

# 3. Mettre à jour les listes de paquets et installer les dépendances système.
# Ces paquets sont nécessaires pour compiler et installer 'mysqlclient' et d'autres outils.
# - build-essential: Contient les outils de compilation comme gcc, make, etc.
# - pkg-config: Un outil essentiel pour que les paquets Python qui dépendent de bibliothèques C
#   trouvent leurs dépendances système.
# - default-libmysqlclient-dev: Les fichiers de développement de la bibliothèque cliente MySQL.
#   C'est la version recommandée pour Debian/Ubuntu.
# - default-mysql-client: Utilitaires client MySQL de base (optionnel, mais utile pour le débogage).
# Supprimez les listes de paquets après l'installation pour réduire la taille de l'image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# 4. Définir le répertoire de travail dans le conteneur.
# Tous les chemins relatifs dans le Dockerfile seront par rapport à cet emplacement.
WORKDIR /app

# 5. Copier le fichier requirements.txt dans le conteneur.
# Il est copié seul pour profiter du cache Docker: si seulement requirements.txt change,
# l'étape d'installation de pip sera re-exécutée, sinon elle sera mise en cache.
COPY requirements.txt /app/requirements.txt

# 6. Installer les dépendances Python spécifiées dans requirements.txt.
# --no-cache-dir: Réduit la taille de l'image en ne stockant pas les caches d'installation.
RUN pip install --no-cache-dir -r /app/requirements.txt

# 7. Copier le reste du code de votre projet dans le conteneur.
# Le '.' représente le répertoire courant de l'hôte (où se trouve le Dockerfile).
COPY . /app

# 8. Exposer le port sur lequel votre application Django s'exécutera.
# C'est une déclaration d'intention; la publication réelle du port se fait dans docker-compose.yml.
EXPOSE 8000

# 9. Définir la commande par défaut pour démarrer l'application.
# Cette commande sera exécutée lorsque le conteneur démarre.
# Elle peut être surchargée par la section 'command' dans docker-compose.yml.
# Pour le développement, `0.0.0.0:8000` rend le serveur accessible de l'extérieur du conteneur.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]