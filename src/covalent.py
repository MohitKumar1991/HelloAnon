import aiohttp


COVALENT_TOKEN_API = 'https://api.covalenthq.com/v1/137/address/0x5dd596c901987a2b28c38a9c1dfbf86fffc15d77/balances_v2/?key=ckey_a26b822b9ea9402390d8f996d27'


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
