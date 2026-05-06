from web3 import Web3

class BlockchainService:
    def __init__(self):
        # Connexion à Ganache
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        # Adresse du contrat (depuis Ganache)
        self.contract_address = Web3.to_checksum_address('0xb2C5395b7ffEA3D188EF11FB5A1F7aECA5f0b000')
        
        # ABI complète (copiée depuis votre fichier JSON)
        self.abi = [
            {"inputs": [{"internalType": "address", "name": "_landlord", "type": "address"}, {"internalType": "address", "name": "_tenant", "type": "address"}, {"internalType": "uint256", "name": "_monthlyRent", "type": "uint256"}, {"internalType": "uint256", "name": "_securityDeposit", "type": "uint256"}], "stateMutability": "nonpayable", "type": "constructor"},
            {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "landlord", "type": "address"}, {"indexed": True, "internalType": "address", "name": "tenant", "type": "address"}], "name": "ContractSigned", "type": "event"},
            {"inputs": [], "name": "getBalance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "isActive", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "landlord", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "monthlyRent", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "securityDeposit", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "signContract", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [], "name": "tenant", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}
        ]
        
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
    
    def is_connected(self):
        """Vérifie la connexion à Ganache"""
        return self.w3.is_connected()
    
    def get_contract_info(self):
        """Récupère toutes les informations du contrat"""
        try:
            return {
                'landlord': self.contract.functions.landlord().call(),
                'tenant': self.contract.functions.tenant().call(),
                'monthly_rent': self.w3.from_wei(self.contract.functions.monthlyRent().call(), 'ether'),
                'security_deposit': self.w3.from_wei(self.contract.functions.securityDeposit().call(), 'ether'),
                'is_active': self.contract.functions.isActive().call(),
                'balance': self.w3.from_wei(self.contract.functions.getBalance().call(), 'ether'),
                'contract_address': self.contract_address
            }
        except Exception as e:
            return {'error': str(e)}
    
    def sign_contract(self, tenant_private_key):
        """Signe le contrat (appelé par le locataire)"""
        try:
            tenant_address = self.w3.eth.account.from_key(tenant_private_key).address
            
            transaction = self.contract.functions.signContract().build_transaction({
                'from': tenant_address,
                'gas': 100000,
                'gasPrice': self.w3.to_wei('20', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(tenant_address)
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(transaction, tenant_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            return {'success': True, 'tx_hash': tx_hash.hex()}
        except Exception as e:
            return {'success': False, 'error': str(e)}