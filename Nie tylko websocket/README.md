# Nie tylko websocket
Artur Lew - Prezentacja PyConPL 2025

Ten projekt zawiera materiały do prezentacji.

## Jak uruchomić backend?
```shell
cd src

pdm sync

pdm run dev1
pdm run dev2
```

Aplikacja jest [tutaj](http://localhost:8000).

## Jak uruchomić frontend?
```shell
cd src

python -m http.server 8001
```
Aplikacja jest [tutaj](http://localhost:8001).

## Jak uruchomić redis?
```shell
cd src

wsl docker compose up redis -d
```

## Jak uruchomić całość?
```shell
cd src

wsl docker compose up -d
```

Redis insight jest [tutaj](http://localhost:5540).

## Jak uruchomić tunel cloudflare?
```shell
cloudflared tunnel --url http://localhost:8000
```
