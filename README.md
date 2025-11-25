# Projet PTUT - Bibliotheque Universitaire avec statistique d'emprunt
---
## Frontend
Nous utilisons Angular pour son coté modulaire.
Modules installe avec npm:
- swiper
- @fullcalendar/timegrid
- @fullcalendar/core   
- @fullcalendar/angular   
- @fullcalendar/daygrid   
- @fullcalendar/interaction
- apexcharts
- ng-apexcharts

Commande pour installer les dependances Docker de l'appli
`docker run -it --rm -p 4200:4200 -v $(pwd):/app angular-front`

Pour demarrer le projet avec Docker
`docker compose up --build`
et pour l'arreter:
`docker compose down`

A faire:
- Barre du header
- Page de profil
- Page de mot de passe 
- FAQ
- Accueil pour personnes non loge avec ses quelques pages
- Page de connexion et d'inscription




 ps aux | grep uvicorn

 pkill -f uvicorn