def _fetch_total_token_usd_value(balance_json):
    usd_value = 0
    if 'tokens' in balance_json:
        for token in balance_json['tokens']:
            usd_value += token['usd_value']

    return usd_value


def _fetch_total_protocol_usd_value(balance_json):
    usd_value = 0
    if 'protocols' in balance_json:
        for protocol in balance_json:
            usd_value += protocol['usd']

    return usd_value


def calculate_user_profile(balance_json):
    total_usd_value = 0
    total_usd_value += _fetch_total_token_usd_value(balance_json)
    total_usd_value += _fetch_total_protocol_usd_value(balance_json)

    if total_usd_value >= 1000000:
        balance_json['profile']['size_class'] = 'whale'
    elif 100000 < total_usd_value < 1000000:
        balance_json['profile']['size_class'] = 'shark'
    else:
        balance_json['profile']['size_class'] = 'shrimp'
