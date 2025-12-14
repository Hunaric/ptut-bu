## Arborescence du projet back

back/
├── main.py                # Point d'entrée FastAPI (équivalent à run.py)
├── requirements.txt       # Les modules a installer
├── Dockerfile.dev
├── .env                   # Secrets / DATABASE_URL
└── app/
     ├── __init__.py
     ├── core/             # Config, utils, sécurité
     │    ├── __init__.py
     │    ├── config.py    # variables d'environnement, settings
     │    ├── security.py
     │    └── database.py  # connexion à la DB (SQLAlchemy)
     ├── models/           # SQLAlchemy
     │    ├── __init__.py
     │    ├── book.py
     ├    ├── account.py
     ├    ├── permission.py
     ├    ├── role.py
     │    ├── user.py
     │    └──
     ├── schemas/          # Pydantic pour validation
     │    ├── __init__.py
     │    ├── book.py
     ├    ├── account.py
     │    ├── user.py
     │    └──
     ├── crud/             # Logique métier
     │    ├── __init__.py
     │    ├── book.py
     ├    ├── account.py
     │    ├── user.py
     │    └──
     └── api/              # Routes FastAPI
          └── v1/
               ├── __init__.py
               ├── book.py
               ├── account.py
               ├── user.py
               └──