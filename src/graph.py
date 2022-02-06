from re import L
import asyncio
from gql import Client, gql as gquery
from gql.transport.aiohttp import AIOHTTPTransport

##https://thegraph.com/hosted-service/subgraph/sameepsi/quickswap03

##https://thegraph.com/hosted-service/subgraph/zephyrys/uniswap-polygon-but-it-works

##https://thegraph.com/hosted-service/subgraph/sushiswap/matic-exchange

UNISWAP_URL = "https://api.thegraph.com/subgraphs/name/zephyrys/uniswap-polygon-but-it-works"
UNISWAP_QUERY = """query {
        swaps(where:{ origin:$address }, orderBy: timestamp, orderDirection: desc) {
            id
            transaction {
                id
            }
            token0{
              name
            }
            token1 {
              name
            }

            sender
    	    recipient
    		origin
            amountUSD
        }
}
"""

SUSHISWAP_URL = "https://api.thegraph.com/subgraphs/name/sushiswap/matic-exchange"
QUICKSWAP_URL = "https://api.thegraph.com/subgraphs/name/sameepsi/quickswap03"
SUSHISWAP_QUERY = """
query {
        swaps(where:{ to: $address }, orderBy: timestamp, orderDirection: desc) {
            id
		transaction {
            id
        }
        pair {
            id
        }
        sender
        to
        amountUSD
    }
}
"""


def make_gql_query_string(qTemplate, address):
    query_str = qTemplate.replace("$address", "\"{0}\"".format(address))
    return gquery(query_str)


async def make_graph_query(graph_url, gQ):
    transport = AIOHTTPTransport(url=graph_url)
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        res = await session.execute(gQ)
        return res


def parse_swap_data(swaps):
    print(swaps)
    tvl = float(0)
    transaction_ids = set()
    for s in swaps:
        tvl = tvl + float(s['amountUSD'])
        transaction_ids.add(s['transaction']['id'])
    return {
        'tvl': tvl,
        'total_swaps': len(transaction_ids)
    }


async def fetch_uniswap_data(address):
    qAd = make_gql_query_string(UNISWAP_QUERY, address)
    swap_results = await make_graph_query(UNISWAP_URL, qAd)
    return parse_swap_data(swap_results['swaps'])


async def fetch_quickswap(address):
    qAd = make_gql_query_string(SUSHISWAP_QUERY, address)
    swap_results = await make_graph_query(QUICKSWAP_URL, qAd)
    return parse_swap_data(swap_results['swaps'])


async def fetch_sushiswap(address):
    qAd = make_gql_query_string(SUSHISWAP_QUERY, address)
    swap_results = await make_graph_query(SUSHISWAP_URL, qAd)
    return parse_swap_data(swap_results['swaps'])


async def fetch_user_data(address):
    resp = await asyncio.gather(fetch_sushiswap(address), fetch_quickswap(address), fetch_uniswap_data(address),
                                return_exceptions=True)
    print(resp)
    return [
        {
            "name": "SushiSwap",
        }.update(resp[0]),
        {
            "name": "QuickSwap",
        }.update(resp[1]),
        {
            "name": "Uniswap",
        }.update(resp[2])
    ]
