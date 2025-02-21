from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get('/healthz')
def health_check():
    return {'status': 'ok'}