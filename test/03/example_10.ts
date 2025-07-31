// Extracted from: docs\Chapters\03.md
// Original example number: 10
// Language: TypeScript
// Auto-generated - do not edit directly

class BankAccount {
  private balance: number
  
  constructor(initialBalance: number) {
    this.balance = initialBalance
  }
  
  deposit(amount: number): void {
    this.balance += amount
  }
  
  getBalance(): number {
    return this.balance
  }
}

const account = new BankAccount(1000)
account.deposit(250)
console.log(account.getBalance()) // 1250

// Classes support inheritance through `extends`:
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