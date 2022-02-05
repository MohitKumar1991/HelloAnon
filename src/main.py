import json
import uvicorn
from fastapi import FastAPI
from .graph import fetch_user_data, make_gql_query_string
from .covalent import fetch_token_balance

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/graph")
async def graph():
    return await fetch_user_data()

@app.get("/token_balance")
async def token_balance():
    return await fetch_token_balance()
