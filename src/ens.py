from web3 import Web3


async def fetch_ens():
    # Connect to INFURA HTTP End Point
    infura_url = 'https://mainnet.infura.io/v3/d2ee0514d1f241f38de158909e077f98'  # infura uri
    w3 = Web3(Web3.HTTPProvider(infura_url))
    try:
        checksum_address = w3.toChecksumAddress('0x0B36748D853621251D5249c18fC18B5ab47437a1')
        print(w3.ens.name(checksum_address))
        return {'ens': w3.ens.name(checksum_address)}
    except Exception as e:
        return {'ens': ''}
