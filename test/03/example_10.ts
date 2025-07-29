// Extracted from: docs\Chapters\03.md
// Original example number: 10
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