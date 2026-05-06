// migrations/2_deploy_rental_contract.js
const RentalContract = artifacts.require("RentalContract");

module.exports = function(deployer, network, accounts) {
  const landlord = accounts[0];
  const tenant = accounts[1];
  const monthlyRent = web3.utils.toWei("0.5", "ether");
  const securityDeposit = web3.utils.toWei("2", "ether");
  
  deployer.deploy(RentalContract, landlord, tenant, monthlyRent, securityDeposit);
};