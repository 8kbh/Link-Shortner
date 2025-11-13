# Link Shortner

Self-hosted link shortner.

## Features

 - link shortner
 - view open statistic
 - edit link

## Deploy
Project uses [uv project manager](https://docs.astral.sh/uv/)

### Install dependencies 
```bash
uv sync
```

### Launch
```bash
LS_HOST='http://127.0.0.1:5020' waitress-serve --host 127.0.0.1 --port 5020  main:app
```
