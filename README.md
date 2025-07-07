# chat-stream
Chat Stream with FASTAPI + GOOGLE GEMINI

### Implantação

a) Instalação das bibliotecas python

```
pip install -r requirements.txt
```

b) Configuração **API_KEY** do google studio no arquivo *.env*

```
touch .env
```

ou

```
nano .env
```

c) Executar a API


Certifique-se de que preencheu o arquivo .env corretamente.

No seu terminal, na pasta do projeto, execute o comando:

```
uvicorn main:app --reload --port 8001
```

d) Acessando via curl

verifique os comandos na pasta *operations*

e) Acessando via web

[https://localhost:8001/docs](https://localhost:8001/docs)

Boa diversão !!!
