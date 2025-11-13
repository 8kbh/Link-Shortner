
# Link Shortner

Self-hosted link shortner.


<img src="https://github.com/8kbh/Link-Shortner/blob/main/.readme/interface.png?raw=true" alt=""/>


> **Try now [8kbh.ru/r/](https://8kbh.ru/r/)**

## Features

 - link shortner
 - view visits statistic
 - edit link

## Deploy
Project uses [uv project manager](https://docs.astral.sh/uv/)

### Install dependencies 
```bash
uv sync
```

### Launch
```bash
set LS_HOST=http://127.0.0.1:5020 &  waitress-serve --host 127.0.0.1 --port 5020  main:app
```
