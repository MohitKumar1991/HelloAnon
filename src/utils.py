from multiprocessing.connection import Client
from wsgiref import headers
import aiohttp
from aiohttp import ClientSession
import asyncio


async def run_in_parallel(atasks):
    responses = asyncio.gather(*atasks, return_exceptions=True)


async def create_request_task(session: ClientSession, url):
    async with session.get(url, headers={
        "apikey": ""
    }) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        html = await response.text()
        print("Body:", html[:15], "...")
        return response.status


async def main(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            html = await response.text()
            print("Body:", html)
