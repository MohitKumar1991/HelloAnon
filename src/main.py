from fastapi import FastAPI
from .graph import fetch_user_data
from .covalent import fetch_token_balance
from .ens import fetch_ens

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/polygon_balance/{address}")
async def polygon_balance(address):
    return await fetch_user_data(address)


@app.get("/token_balance/{address}")
async def token_balance(address):
    return await fetch_token_balance(address)


@app.get("/ens/{address}")
async def get_ens(address):
    return await fetch_ens(address)

