// Extracted from: docs\Chapters\03.md
// Original example number: 11
// Auto-generated - do not edit directly

class SavingsAccount extends BankAccount {
  private interestRate: number
  
  constructor(initialBalance: number, rate: number) {
    super(initialBalance) // Call parent constructor
    this.interestRate = rate
  }
  
  applyInterest(): void {
    const interest = this.getBalance() * this.interestRate
    this.deposit(interest)
  }
}