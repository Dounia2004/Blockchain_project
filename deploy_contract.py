from web3 import Web3

# Connexion à Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

print(f"Connecté: {w3.is_connected()}")

# Comptes
accounts = w3.eth.accounts
print(f"Comptes disponibles: {len(accounts)}")

# ABI simplifiée
abi = [
    {"inputs": [{"internalType": "address", "name": "_landlord", "type": "address"}, {"internalType": "address", "name": "_tenant", "type": "address"}, {"internalType": "uint256", "name": "_monthlyRent", "type": "uint256"}, {"internalType": "uint256", "name": "_securityDeposit", "type": "uint256"}], "stateMutability": "nonpayable", "type": "constructor"},
    {"inputs": [], "name": "landlord", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "tenant", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "isActive", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "signContract", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
]

# Bytecode
bytecode = "0x608060405234801561000f575f80fd5b5060405161063b38038061063b83398181016040528101906100319190610171565b835f806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508260015f6101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555081600281905550806003819055505f60045f6101000a81548160ff021916908315150217905550505050506101d5565b5f80fd5b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61010d826100e4565b9050919050565b61011d81610103565b8114610127575f80fd5b50565b5f8151905061013881610114565b92915050565b5f819050919050565b6101508161013e565b811461015a575f80fd5b50565b5f8151905061016b81610147565b92915050565b5f805f8060808587031215610189576101886100e0565b5b5f6101968782880161012a565b94505060206101a78782880161012a565b93505060406101b88782880161015d565b92505060606101c98782880161015d565b91505092959194509250565b610459806101e25f395ff3fe608060405234801561000f575f80fd5b506004361061007b575f3560e01c8063adf0779111610059578063adf07791146100d9578063b8b4f1a0146100f7578063dc1997ea14610101578063e4cbecdf1461011f5761007b565b806312065fe01461007f578063220e5ab31461009d57806322f3e2d4146100bb575b5f80fd5b61008761013d565b6040516100949190610307565b60405180910390f35b6100a5610144565b6040516100b29190610307565b60405180910390f35b6100c361014a565b6040516100d0919061033a565b60405180910390f35b6100e161015c565b6040516100ee9190610392565b60405180910390f35b6100ff610181565b005b6101096102c6565b6040516101169190610392565b60405180910390f35b6101276102e9565b6040516101349190610307565b60405180910390f35b5f47905090565b60035481565b60045f9054906101000a900460ff1681565b60015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610210576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161020790610405565b60405180910390fd5b600160045f6101000a81548160ff02191690831515021790555060015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff165f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff167f2e8ef42a9628bc1660f1f397a4fb77b6369005ddbe363f5510591f88db43b11860405160405180910390a3565b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60025481565b5f819050919050565b610301816102ef565b82525050565b5f60208201905061031a5f8301846102f8565b92915050565b5f8115159050919050565b61033481610320565b82525050565b5f60208201905061034d5f83018461032b565b92915050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61037c82610353565b9050919050565b61038c81610372565b82525050565b5f6020820190506103a55f830184610383565b92915050565b5f82825260208201905092915050565b7f4f6e6c792074656e616e740000000000000000000000000000000000000000005f82015250565b5f6103ef600b836103ab565b91506103fa826103bb565b602082019050919050565b5f6020820190508181035f83015261041c816103e3565b905091905056fea2646970667358221220f9d37a9d9f522287b190a9e7ec56303033e7d4ec734db0ba4c05e641987f28ee64736f6c63430008150033"

# Paramètres
landlord = accounts[0]
tenant = accounts[1]
monthly_rent = w3.to_wei(0.5, 'ether')
security_deposit = w3.to_wei(2, 'ether')

print(f"\nDéploiement du contrat...")
print(f"Propriétaire: {landlord}")
print(f"Locataire: {tenant}")

# Création du contrat
RentalContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Transaction
transaction = RentalContract.constructor(landlord, tenant, monthly_rent, security_deposit).build_transaction({
    'from': landlord,
    'nonce': w3.eth.get_transaction_count(landlord),
    'gas': 3000000,
    'gasPrice': w3.to_wei('20', 'gwei')
})

# Clé privée
private_key = input("\nCollez la clé privée du compte 0 (dans Ganache): ")

# Envoi
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print(f"Transaction: {tx_hash.hex()}")

# Attente
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"\n✅ CONTRAT DÉPLOYÉ !")
print(f"📍 Adresse: {tx_receipt.contractAddress}")

# Sauvegarde
with open('contract_address.txt', 'w') as f:
    f.write(tx_receipt.contractAddress)
print("\n✅ Adresse sauvegardée dans contract_address.txt")