// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RentalContract {
    address public landlord;
    address public tenant;
    uint256 public monthlyRent;
    uint256 public securityDeposit;
    uint256 public startDate;
    uint256 public endDate;
    bool public isActive;
    
    event ContractSigned(address indexed landlord, address indexed tenant);
    event RentPaid(address indexed tenant, uint256 amount, uint256 date);
    
    constructor(
        address _landlord,
        address _tenant,
        uint256 _monthlyRent,
        uint256 _securityDeposit,
        uint256 _durationInMonths
    ) {
        landlord = _landlord;
        tenant = _tenant;
        monthlyRent = _monthlyRent;
        securityDeposit = _securityDeposit;
        startDate = block.timestamp;
        endDate = block.timestamp + (_durationInMonths * 30 days);
        isActive = false;
    }
    
    function signContract() external payable {
        require(msg.sender == tenant, "Only tenant can sign");
        require(msg.value == securityDeposit, "Incorrect deposit amount");
        require(isActive == false, "Contract already signed");
        
        isActive = true;
        emit ContractSigned(landlord, tenant);
    }
    
    function payRent() external payable {
        require(msg.sender == tenant, "Only tenant can pay");
        require(isActive == true, "Contract not active");
        require(msg.value == monthlyRent, "Incorrect rent amount");
        require(block.timestamp <= endDate, "Contract expired");
        
        payable(landlord).transfer(msg.value);
        emit RentPaid(tenant, msg.value, block.timestamp);
    }
    
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}