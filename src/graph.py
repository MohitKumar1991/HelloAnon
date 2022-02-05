from gql import Client, gql as gquery
from gql.transport.aiohttp import AIOHTTPTransport

import json

SIMPLE_QUERY = """query {
    userReserves(first:5) {
        id
    }
}
"""


def make_gql_query_string(param_types=None):
    query_str = SIMPLE_QUERY
    prefix = ''
    if param_types is not None:
        prefix = 'query '
        prefix += json.dumps(param_types).replace('"', '').replace('{', '(').replace('}', ')')
        prefix += '{'
    print(prefix + query_str)
    return gquery(prefix + query_str)


async def make_graph_query(gQ):
    transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/aave/protocol-v2")
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        res = await session.execute(gQ)
        return res


async def fetch_user_data():
    return await make_graph_query(make_gql_query_string())
