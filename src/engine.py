def _fetch_total_token_usd_value(balance_json):
    usd_value = 0
    if 'tokens' in balance_json:
        for token in balance_json['tokens']:
            try:
                usd_value += token['usd_value']
            except Exception as e:
                continue

    return usd_value


def _fetch_total_protocol_usd_value(balance_json):
    usd_value = 0
    if 'protocols' in balance_json:
        for protocol in balance_json['protocols']:
            try:
                usd_value += protocol['usd']
            except Exception as e:
                continue

    return usd_value


def calculate_user_profile(balance_json):
    total_usd_value = 0
    total_usd_value += _fetch_total_token_usd_value(balance_json)
    total_usd_value += _fetch_total_protocol_usd_value(balance_json)

    balance_json['profile']['total_usd_value'] = total_usd_value
    if total_usd_value >= 1000000:
        balance_json['profile']['size_class'] = 'whale'
    elif 100000 < total_usd_value < 1000000:
        balance_json['profile']['size_class'] = 'shark'
    elif 10000 < total_usd_value < 100000:
        balance_json['profile']['size_class'] = 'shrimp'
    else:
        balance_json['profile']['size_class'] = 'crab'

    return balance_json
