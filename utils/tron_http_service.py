"""
-------------------------------------------------
   File Name:        TronService.py
   Description:      
   Author:           simon
   Version:          1.0
-------------------------------------------------
"""
import requests
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
endpoint_uri = "https://api.shasta.trongrid.io"
api_key=""
class TronService:
    @staticmethod
    def create_wallet():

        private = PrivateKey.random()
        address = private.public_key.to_base58check_address()
        return {
            "address": address,
            "private_key": private.hex()
        }

    @staticmethod
    def get_balance(address):
        url = f"{endpoint_uri}/v1/accounts/{address}"
        response = requests.get(url)
        print(response.text)

    @staticmethod
    def transfer_trx(from_address, to_address, private_key_hex, amount):
        provider = HTTPProvider(endpoint_uri="https://api.trongrid.io", api_key="你的API_KEY")
        client = Tron(provider=provider)
        private_key = PrivateKey.fromhex(private_key_hex)
        derived_address = private_key.public_key.to_base58check_address()
        if derived_address != from_address:
            raise ValueError("私钥和地址不匹配！")
        txn = client.trx.transfer(from_address, to_address, amount).build()
        signed_txn = txn.sign(private_key)
        result = signed_txn.broadcast().wait()
        return result

    @staticmethod
    def transfer_trc10(from_address, to_address, private_key_hex, token_id, amount):
        client = Tron(network=network)
        private_key = PrivateKey.fromhex(private_key_hex)
        derived_address = private_key.public_key.to_base58check_address()
        if derived_address != from_address: raise ValueError("私钥和地址不匹配！")
        txn = client.trx.transfer_asset(from_address, to_address, token_id, amount).build()
        signed_txn = txn.sign(private_key)
        result = signed_txn.broadcast().wait()
        return result

    @staticmethod
    def transfer_trc20(from_address, to_address, private_key_hex, contract_address, amount):
        client = Tron(network=network)

        private_key = PrivateKey.fromhex(private_key_hex)
        derived_address = private_key.public_key.to_base58check_address()
        if derived_address != from_address: raise ValueError(
            "私钥和地址不匹配！")
        # 获取合约对象
        contract = client.get_contract(contract_address)
        # 构造交易：调用合约的 transfer 方法
        txn = contract.functions.transfer(to_address, amount).with_owner(from_address).build()
        signed_txn = txn.sign(private_key)
        result = signed_txn.broadcast().wait()
        return result


from_address = "THzUm9MKDkNQLFHqeTAVsuAsTnhczTSxKv"
to_address = "TUreh7oeV11TC7Ar3hJdd5kLkHGZGYQVki"
private_key_hex = "3d30bdcfbefcb058ea1f73be6c15543f641223ce2b1879665f8ff68256a47734"
amount = 1000
print(TronService.transfer_trx(from_address, to_address, private_key_hex, amount))
TronService.get_balance("THzUm9MKDkNQLFHqeTAVsuAsTnhczTSxKv")
TronService.get_balance("TUreh7oeV11TC7Ar3hJdd5kLkHGZGYQVki")
