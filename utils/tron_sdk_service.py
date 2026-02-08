"""
-------------------------------------------------
   File Name:        TronService.py
   Description:      
   Author:           simon
   Version:          1.0
-------------------------------------------------
"""
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider

network = "shasta"
endpoint_uri = f"https://api.{network}.trongrid.io"
api_key = "115beec4-8381-460b-9ed2-0a76188e7500"


class TronService:
    provider = HTTPProvider(endpoint_uri=endpoint_uri, api_key=api_key)
    client = Tron(provider=provider)

    @staticmethod
    def generate_wallet():

        private = PrivateKey.random()
        address = private.public_key.to_base58check_address()
        return {
            "address": address,
            "private_key": private.hex()
        }

    @classmethod
    def get_balance(cls, address):
        account = cls.client.get_account(address)
        print(f"account: {account}")
        balance = account.get("balance", 0)
        print("Balance:", balance / 1_000_000, "TRX")
        return balance

    @classmethod
    def transfer_trx(cls, from_address, to_address, private_key_hex, amount):
        private_key = PrivateKey.fromhex(private_key_hex)
        derived_address = private_key.public_key.to_base58check_address()
        if derived_address != from_address:
            raise ValueError("私钥和地址不匹配！")
        txn = cls.client.trx.transfer(from_address, to_address, amount).build()
        signed_txn = txn.sign(private_key)
        result = signed_txn.broadcast().wait()
        return result

    @classmethod
    def transfer_trc10(cls, from_address, to_address, private_key_hex, token_id, amount):
        pass
        return ""

    @classmethod
    def transfer_trc20(cls, from_address, to_address, private_key_hex, contract_address, amount):
        client = Tron(network=network)

        private_key = PrivateKey.fromhex(private_key_hex)
        derived_address = private_key.public_key.to_base58check_address()
        if derived_address != from_address: raise ValueError(
            "私钥和地址不匹配！")
        # 获取合约对象
        contract = cls.client.get_contract(contract_address)
        # 构造交易：调用合约的 transfer 方法
        txn = contract.functions.transfer(to_address, amount).with_owner(from_address).build()
        signed_txn = txn.sign(private_key)
        result = signed_txn.broadcast().wait()
        return result


# from_address = "THzUm9MKDkNQLFHqeTAVsuAsTnhczTSxKv"
# to_address = "TUreh7oeV11TC7Ar3hJdd5kLkHGZGYQVki"
# private_key_hex = "3d30bdcfbefcb058ea1f73be6c15543f641223ce2b1879665f8ff68256a47734"
# amount = 1000
# print(TronService.transfer_trx(from_address, to_address, private_key_hex, amount))
# TronService.get_balance("THzUm9MKDkNQLFHqeTAVsuAsTnhczTSxKv")
# TronService.get_balance("TUreh7oeV11TC7Ar3hJdd5kLkHGZGYQVki")
