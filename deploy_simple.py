from web3 import Web3
from solcx import compile_standard, install_solc

# Installe Solidity
install_solc('0.8.21')

# Connexion
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
print(f"Connecté: {w3.is_connected()}")

# Lecture du contrat
with open('blockchain/contracts/simple_contract.sol', 'r') as f:
    contract_code = f.read()

# Compilation
compiled = compile_standard({
    "language": "Solidity",
    "sources": {"simple_contract.sol": {"content": contract_code}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
}, solc_version='0.8.21')

bytecode = compiled['contracts']['simple_contract.sol']['SimpleStorage']['evm']['bytecode']['object']
abi = compiled['contracts']['simple_contract.sol']['SimpleStorage']['abi']

accounts = w3.eth.accounts
account = accounts[0]
private_key = input("Clé privée du compte 0: ")

# Déploiement
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
transaction = SimpleStorage.constructor().build_transaction({
    'from': account,
    'nonce': w3.eth.get_transaction_count(account),
    'gas': 3000000,
    'gasPrice': w3.to_wei('20', 'gwei')
})

signed = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"✅ Contrat déployé à: {receipt.contractAddress}")

# Test
contract = w3.eth.contract(address=receipt.contractAddress, abi=abi)
tx = contract.functions.setValue(42).build_transaction({
    'from': account,
    'nonce': w3.eth.get_transaction_count(account),
    'gas': 100000,
    'gasPrice': w3.to_wei('20', 'gwei')
})
signed = w3.eth.account.sign_transaction(tx, private_key)
w3.eth.send_raw_transaction(signed.raw_transaction)

print(f"Valeur après setValue(42): {contract.functions.getValue().call()}")