// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RentalContract {
    address public landlord;
    address public tenant;
    uint256 public monthlyRent;
    uint256 public securityDeposit;
    bool public isActive;
    
    event ContractSigned(address indexed landlord, address indexed tenant);
    
    constructor(
        address _landlord,
        address _tenant,
        uint256 _monthlyRent,
        uint256 _securityDeposit
    ) {
        landlord = _landlord;
        tenant = _tenant;
        monthlyRent = _monthlyRent;
        securityDeposit = _securityDeposit;
        isActive = false;
    }
    
    function signContract() external {
        require(msg.sender == tenant, "Only tenant can sign");
        isActive = true;
        emit ContractSigned(landlord, tenant);
    }
    
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}