import json
from web3 import Web3
from solcx import compile_standard, install_solc

# Installe la version de Solidity
install_solc('0.8.21')

# Connexion à Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

if not w3.is_connected():
    print("❌ Impossible de se connecter à Ganache")
    exit()

print("✅ Connecté à Ganache")

# Lecture du contrat Solidity
with open('contracts/RentalContract.sol', 'r') as f:
    contract_code = f.read()

# Compilation
compiled = compile_standard({
    "language": "Solidity",
    "sources": {"RentalContract.sol": {"content": contract_code}},
    "settings": {
        "outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}
    }
}, solc_version='0.8.21')

# Extraction du bytecode et ABI
bytecode = compiled['contracts']['RentalContract.sol']['RentalContract']['evm']['bytecode']['object']
abi = compiled['contracts']['RentalContract.sol']['RentalContract']['abi']

print("✅ Contrat compilé")

# Comptes Ganache
accounts = w3.eth.accounts
landlord = accounts[0]
tenant = accounts[1]

print(f"Propriétaire: {landlord}")
print(f"Locataire: {tenant}")

# Paramètres (SANS duration_months car le nouveau contrat n'en a pas)
monthly_rent = w3.to_wei(0.5, 'ether')
security_deposit = w3.to_wei(2, 'ether')

print(f"Loyer mensuel: 0.5 ETH")
print(f"Caution: 2 ETH")

# Création du contrat - 4 paramètres seulement
RentalContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Construction de la transaction avec 4 paramètres
transaction = RentalContract.constructor(landlord, tenant, monthly_rent, security_deposit).build_transaction({
    'from': landlord,
    'nonce': w3.eth.get_transaction_count(landlord),
    'gas': 3000000,
    'gasPrice': w3.to_wei('20', 'gwei')
})

# Clé privée
private_key = input("Entrez la clé privée du compte 0 (voir dans Ganache): ")

# Signature et envoi
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print(f"Transaction envoyée: {tx_hash.hex()}")

# Attente de la confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"✅ Contrat déployé à: {tx_receipt.contractAddress}")

# Sauvegarde de l'ABI et de l'adresse
with open('contract_info.json', 'w') as f:
    json.dump({
        'address': tx_receipt.contractAddress,
        'abi': abi
    }, f, indent=2)

print("✅ Informations sauvegardées dans contract_info.json")