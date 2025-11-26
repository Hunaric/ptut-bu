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
- Page de profil
- Page de mot de passe 
- FAQ
- Accueil pour personnes non loge avec ses quelques pages




 ps aux | grep uvicorn

 pkill -f uvicorn

 docker exec -it ptut_back alembic upgrade head

## Pour executer postgre depuis le shell

```shell
docker exec -it ptut_db psql -U ptut_user -d ptut_db
```

Puis dans psql :

```sql 
SELECT * FROM users;
```


Attention: la commande suivant est utilisee pour supprimer l ancienne base de donnees
```shell
docker-compose down -v
docker-compose up -d
```

Ça réinitialise ptut_db et toutes les données disparaissent, tu pourras recréer tes utilisateurs sans conflit.

Dans pgAdmin avec le localhost:5050:

```
Clique sur Add New Server.

Onglet General : mets un nom (ex. PTUT_DB).

Onglet Connection :

Host name/address: db (ou localhost si tu utilises le port 5433 exposé)

Port: 5432 (dans le conteneur) ou 5433 (si tu veux passer par le port mappé)

Database: ptut_db

Username: ptut_user

Password: ptut_pass

Clique Save.
```

3️⃣ Explorer les données

Clique sur ton serveur → Databases → ptut_db → Schemas → public → Tables.

Clique sur la table users → View/Edit Data → All Rows.

Là tu verras tous les utilisateurs que tu as créés.