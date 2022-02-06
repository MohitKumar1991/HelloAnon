from web3 import Web3


async def fetch_ens(address):
    # Connect to INFURA HTTP End Point
    infura_url = 'https://mainnet.infura.io/v3/d2ee0514d1f241f38de158909e077f98'  # infura uri
    w3 = Web3(Web3.HTTPProvider(infura_url))
    try:
        checksum_address = w3.toChecksumAddress(address)
        print(w3.ens.name(checksum_address))
        return {'ens': w3.ens.name(checksum_address)}
    except Exception as e:
        return {'ens': ''}
