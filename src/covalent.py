import aiohttp


COVALENT_TOKEN_API = 'https://api.covalenthq.com/v1/137/address/0x5dd596c901987a2b28c38a9c1dfbf86fffc15d77/balances_v2/?key=ckey_a26b822b9ea9402390d8f996d27'
COVALENT_SUSHISWAP_BALANCES_API = 'https://api.covalenthq.com/v1/137/address/0x5dd596c901987a2b28c38a9c1dfbf86fffc15d77/stacks/sushiswap/balances/?&key=ckey_a26b822b9ea9402390d8f996d27'
COVALENT_AAVE_BALANCES_API = 'https://api.covalenthq.com/v1/137/address/0x5dd596c901987a2b28c38a9c1dfbf86fffc15d77/stacks/aave_v2/balances/?&key=ckey_a26b822b9ea9402390d8f996d27'


def _fetch_token_data(response_json):
    token_data = {'tokens': []}
    if 'data' in response_json and response_json['data']:
        if 'items' in response_json['data'] and len(response_json['data']['items']) > 0:
            for item in response_json['data']['items']:
                try:
                    contract_decimals = item['contract_decimals']
                    balance = item['balance']
                    token_type = item['type']
                    quote_rate = item['quote_rate']
                    contract_ticker_symbol = item['contract_ticker_symbol']

                    if token_type == 'cryptocurrency':
                        token_count = int(balance) / (10 ** contract_decimals)
                        usd_value = token_count * quote_rate

                        token_data['tokens'].append({
                            'token': contract_ticker_symbol,
                            'balance': int(balance),
                            'usd_value': usd_value
                        })
                except Exception as e:
                    continue

    return token_data


async def fetch_token_balance():
    async with aiohttp.ClientSession() as session:
        async with session.get(COVALENT_TOKEN_API, headers={"Content-Type": "application/json"}) as response:
            response_json = await response.json()
            return _fetch_token_data(response_json)

"""
        "sushiswap": {
            "balances": [
                {
                    "token_0": {
                        "contract_decimals": 6,
                        "contract_ticker_symbol": "USDC",
                        "contract_address": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x2791bca1f2de4661ed88a30c99a7a9449aa84174.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.9981802
                    },
                    "token_1": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "DAI",
                        "contract_address": "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x8f3cf7ad23cd3cadbd9735aff958023239c6a063.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.9994249
                    },
                    "pool_token": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "USDC-DAI SLP",
                        "contract_address": "0xcd578f016888b57f1b1e3f887f392f0159e26747",
                        "logo_url": null,
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 2099135.8,
                        "total_supply": "1989737230505921431"
                    }
                },
                {
                    "token_0": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "WMATIC",
                        "contract_address": "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 1.7171521
                    },
                    "token_1": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "TITAN",
                        "contract_address": "0xaaa5b9e6c589642f98a1cda99b9d024b8407285a",
                        "logo_url": "https://logos.covalenthq.com/tokens/0xaaa5b9e6c589642f98a1cda99b9d024b8407285a.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 1.6594849E-7
                    },
                    "pool_token": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "WMATIC-TITAN SLP",
                        "contract_address": "0xa79983daf2a92c2c902cd74217efe3d8af9fba2a",
                        "logo_url": null,
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.0036422485,
                        "total_supply": "6885088857241089582165888"
                    }
                },
                {
                    "token_0": {
                        "contract_decimals": 6,
                        "contract_ticker_symbol": "USDC",
                        "contract_address": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x2791bca1f2de4661ed88a30c99a7a9449aa84174.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.9981802
                    },
                    "token_1": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "PUSD",
                        "contract_address": "0x9af3b7dc29d3c4b1a5731408b6a9656fa7ac3b72",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x9af3b7dc29d3c4b1a5731408b6a9656fa7ac3b72.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.98531926
                    },
                    "pool_token": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "USDC-PUSD SLP",
                        "contract_address": "0xc30d6bc42911aa21a63e51c7121b33b3e65cc3c4",
                        "logo_url": null,
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 2111485.5,
                        "total_supply": "32304279953614514"
                    }
                },
                {
                    "token_0": {
                        "contract_decimals": 6,
                        "contract_ticker_symbol": "USDC",
                        "contract_address": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x2791bca1f2de4661ed88a30c99a7a9449aa84174.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.9981802
                    },
                    "token_1": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "DINO",
                        "contract_address": "0xaa9654becca45b5bdfa5ac646c939c62b527d394",
                        "logo_url": "https://logos.covalenthq.com/tokens/0xaa9654becca45b5bdfa5ac646c939c62b527d394.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.048125066
                    },
                    "pool_token": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "USDC-DINO SLP",
                        "contract_address": "0x3324af8417844e70b81555a6d1568d78f4d4bf1f",
                        "logo_url": null,
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 459491.16,
                        "total_supply": "1637481169449538724"
                    }
                },
                {
                    "token_0": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "WETH",
                        "contract_address": "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x7ceb23fd6bc0add59e62ac25578270cff1b9f619.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 3012.0298
                    },
                    "token_1": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "AAVE",
                        "contract_address": "0xd6df932a45c0f255f85145f286ea0b292b21c90b",
                        "logo_url": "https://logos.covalenthq.com/tokens/0xd6df932a45c0f255f85145f286ea0b292b21c90b.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 166.7019
                    },
                    "pool_token": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "WETH-AAVE SLP",
                        "contract_address": "0x2813d43463c374a680f235c428fb1d7f08de0b69",
                        "logo_url": null,
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 1481.481,
                        "total_supply": "4179236533948112597664"
                    }
                },
                {
                    "token_0": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "WETH",
                        "contract_address": "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x7ceb23fd6bc0add59e62ac25578270cff1b9f619.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 3012.0298
                    },
                    "token_1": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "DAI",
                        "contract_address": "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x8f3cf7ad23cd3cadbd9735aff958023239c6a063.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.9994249
                    },
                    "pool_token": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "WETH-DAI SLP",
                        "contract_address": "0x6ff62bfb8c12109e8000935a6de54dad83a4f39f",
                        "logo_url": null,
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 121.37213,
                        "total_supply": "51745082337611763394202"
                    }
                },
                {
                    "token_0": {
                        "contract_decimals": 6,
                        "contract_ticker_symbol": "USDC",
                        "contract_address": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                        "logo_url": "https://logos.covalenthq.com/tokens/0x2791bca1f2de4661ed88a30c99a7a9449aa84174.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.9981802
                    },
                    "token_1": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "IRON",
                        "contract_address": "0xd86b5923f3ad7b585ed81b448170ae026c65ae9a",
                        "logo_url": "https://logos.covalenthq.com/tokens/0xd86b5923f3ad7b585ed81b448170ae026c65ae9a.png",
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 0.9940315
                    },
                    "pool_token": {
                        "contract_decimals": 18,
                        "contract_ticker_symbol": "USDC-IRON SLP",
                        "contract_address": "0x85de135ff062df790a5f20b79120f17d3da63b2d",
                        "logo_url": null,
                        "balance": "0",
                        "quote": 0.0,
                        "quote_rate": 2095652.1,
                        "total_supply": "83641708708856175"
                    }
                }
            ]
        }
"""
def _fetch_sushiswap_data(response_json):
    if 'data' in response_json and response_json['data']:
        if 'sushiswap' in response_json['data'] and 'balances' in response_json['data']['sushiswap']:
            for token_pair_balance in response_json['data']['sushiswap']['balances']:
                first_token = token_pair_balance['token_0']
                second_token = token_pair_balance['token_1']
                pool_token = token_pair_balance['pool_token']


async def fetch_sushiswap_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(COVALENT_SUSHISWAP_BALANCES_API, headers={"Content-Type": "application/json"}) as response:
            response_json = await response.json()
            return _fetch_sushiswap_data(response_json)


def _fetch_aave_data(response_json):
    total_usd_value = 0
    if 'data' in response_json and response_json['data']:
        if 'aave' in response_json['data'] and 'balances' in response_json['data']['aave']:
            for pool_balance in response_json['data']['aave']['balances']:
                balance = pool_balance['balance']
                atoken_balance = balance['atoken_balance']
                asset_contract_decimals = balance['asset_contract_decimals']
                quote_rate = balance['quote_rate']

                token_count = int(atoken_balance) / (10 ** asset_contract_decimals)
                usd_value = token_count * quote_rate
                total_usd_value += usd_value

    return {
        'name': 'Aave',
        'usd': total_usd_value
    }


async def fetch_aave_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(COVALENT_AAVE_BALANCES_API, headers={"Content-Type": "application/json"}) as response:
            response_json = await response.json()
            return _fetch_aave_data(response_json)


