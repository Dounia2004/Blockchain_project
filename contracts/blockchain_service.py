import json
import os
from web3 import Web3

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        # Load the ABI and Bytecode from the compiled JSON
        contract_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            'blockchain', 'build', 'contracts', 'RentalContract.json'
        )
        with open(contract_path, 'r') as file:
            contract_json = json.load(file)
            self.abi = contract_json['abi']
            self.bytecode = contract_json['bytecode']
        
    def is_connected(self):
        return self.w3.is_connected()
        
    def _get_contract(self, address):
        checksum_address = Web3.to_checksum_address(address)
        return self.w3.eth.contract(address=checksum_address, abi=self.abi)
    
    def get_contract_info(self, contract_address):
        try:
            contract = self._get_contract(contract_address)
            return {
                'landlord': contract.functions.landlord().call(),
                'tenant': contract.functions.tenant().call(),
                'is_active': contract.functions.isActive().call(),
                'contract_address': contract_address
            }
        except Exception as e:
            return {'error': str(e)}

    def deploy_contract(self, landlord_address, tenant_address, monthly_rent, deposit, duration_months):
        try:
            # 1. Convert amounts to Wei (using standard 'ether' decimals)
            monthly_rent_wei = self.w3.to_wei(monthly_rent, 'ether')
            deposit_wei = self.w3.to_wei(deposit, 'ether')
            
            # 2. Get the contract class
            RentalContract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
            
            # 3. Build & send the deployment transaction
            tx_hash = RentalContract.constructor(
                Web3.to_checksum_address(landlord_address),
                Web3.to_checksum_address(tenant_address),
                monthly_rent_wei,
                deposit_wei
            ).transact({'from': landlord_address})
            
            # 4. Wait for it to be mined
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'contract_address': tx_receipt.contractAddress,
                'tx_hash': self.w3.to_hex(tx_hash)
            }
        except Exception as e:
            raise Exception(f"Validation ou déploiement échoué: {str(e)}")

    def sign_contract(self, contract_address, tenant_private_key, deposit_amount):
        try:
            contract = self._get_contract(contract_address)
            account = self.w3.eth.account.from_key(tenant_private_key)
            
            tx = contract.functions.signContract().build_transaction({
                'from': account.address,
                'nonce': self.w3.eth.get_transaction_count(account.address),
            })
            
            # Sign and send
            signed_tx = account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            raise Exception(f"Sign failed: {str(e)}")

    def pay_rent(self, contract_address, tenant_private_key, rent_amount):
        try:
            contract = self._get_contract(contract_address)
            account = self.w3.eth.account.from_key(tenant_private_key)
            rent_wei = self.w3.to_wei(rent_amount, 'ether')
            
            tx = contract.functions.payRent().build_transaction({
                'from': account.address,
                'value': rent_wei,
                'nonce': self.w3.eth.get_transaction_count(account.address),
            })
            
            signed_tx = account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            raise Exception(f"Pay rent failed: {str(e)}")