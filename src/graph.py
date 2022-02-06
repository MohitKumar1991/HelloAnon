from re import L
import asyncio
from gql import Client, gql as gquery
from gql.transport.aiohttp import AIOHTTPTransport
from .covalent import fetch_token_balance, fetch_aave_data, fetch_sushiswap_data
from .engine import calculate_user_profile
from .ens import fetch_ens

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
    balance_json = {'profile': {
        'address': address
    },
        'protocols': [],
        'tokens': []
    }
    # resp = await asyncio.gather(fetch_sushiswap(address), fetch_quickswap(address), fetch_uniswap_data(address),
    #                             fetch_token_balance(address), fetch_aave_data(address), fetch_sushiswap_data(address),
    #                             fetch_ens(address),
    #                             return_exceptions=True)

    resp = await asyncio.gather(fetch_token_balance(address), fetch_ens(address), fetch_aave_data(address),
                                fetch_sushiswap_data(address),
                                return_exceptions=True)

    balance_json['profile']['ens'] = resp[1]['ens']
    balance_json['protocols'].append(resp[2])
    for sushiswap_lp_token in resp[3]:
        balance_json['protocols'].append(sushiswap_lp_token)
    
    balance_json['tokens'] = (resp[0]['tokens'])
    print(balance_json)
    result_json = calculate_user_profile(balance_json)

    return result_json
