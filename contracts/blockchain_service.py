from web3 import Web3

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        # 🔴 REMPLACEZ PAR L'ADRESSE DE VOTRE CONTRAT
        self.contract_address = Web3.to_checksum_address('0xb2C5395b7ffEA3D188E11FB51AF7aECA5f0b000')
        
        self.abi = [
            {"inputs": [{"internalType": "address", "name": "_landlord", "type": "address"}, {"internalType": "address", "name": "_tenant", "type": "address"}, {"internalType": "uint256", "name": "_monthlyRent", "type": "uint256"}, {"internalType": "uint256", "name": "_securityDeposit", "type": "uint256"}], "stateMutability": "nonpayable", "type": "constructor"},
            {"inputs": [], "name": "landlord", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "tenant", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "isActive", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "signContract", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
        ]
        
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
    
    def is_connected(self):
        return self.w3.is_connected()
    
    def get_contract_info(self):
        try:
            return {
                'landlord': self.contract.functions.landlord().call(),
                'tenant': self.contract.functions.tenant().call(),
                'is_active': self.contract.functions.isActive().call(),
                'contract_address': self.contract_address
            }
        except Exception as e:
            return {'error': str(e)}