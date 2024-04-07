# Ecommerce
Ecommerce Basic app

## docs
I'll use https://mkdocstrings.github.io/usage/#result
with https://squidfunk.github.io/mkdocs-material/

## setup
```
cd backend
poetry install
cd ..
cd frontend
bun install
```

## how to run
setup services:
```
docker-compose up -d
```

backend:
```
cd backend
poetry run uvicorn ecommerce.main:app --reload
```
frontend:
```
cd frontend
bun run dev
```