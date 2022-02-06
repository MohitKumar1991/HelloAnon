from gql import Client, gql as gquery
from gql.transport.aiohttp import AIOHTTPTransport

import json

##https://thegraph.com/hosted-service/subgraph/sameepsi/quickswap03

##https://thegraph.com/hosted-service/subgraph/zephyrys/uniswap-polygon-but-it-works

SIMPLE_QUERY = """query {
        swaps(where:{ sender:$address }) {
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

def make_gql_query_string(param_types=None):
    query_str = SIMPLE_QUERY.replace("$address","\"0x569376A1f338bAc253FD7e6dC75B20D1b54293c6\"")
    prefix = ''
    if param_types is not None:
        prefix = 'query '
        prefix += json.dumps(param_types).replace('"', '').replace('{', '(').replace('}', ')')
        prefix += '{'
    print(prefix + query_str)
    return gquery(prefix + query_str)


async def make_graph_query(gQ):
    transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/sushiswap/matic-exchange")
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        res = await session.execute(gQ)
        return res


def parse_swap_data(swaps):
    tvl = float(0)
    for s in swaps:
        tvl = tvl  + float(s['amountUSD'])
    return  {
        'tvl': tvl,
        'total_swaps': len(swaps)
    }


async def fetch_user_data():
    resp =  await make_graph_query(make_gql_query_string())
    return parse_swap_data(resp['swaps'])
