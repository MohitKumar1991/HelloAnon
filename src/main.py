import uvicorn, json
from fastapi import FastAPI
from .graph import fetch_user_data, make_gql_query_string
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/graph")
async def graph():
    return await fetch_user_data()