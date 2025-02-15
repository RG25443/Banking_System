import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance is {self.balance}.")
        elif amount > 0:
            self.balance -= amount
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        return f"Account Number: {self.account_number}, Account Holder: {self.account_holder}, Balance: {self.balance}"

class BankingSystem:
    def __init__(self, root):
        self.accounts = {}

        self.root = root
        self.root.title("Banking System")
        self.root.configure(bg="#f0f0f0")

        # Common font for widgets
        self.font = ("Arial", 12, "bold")

        # Date Display
        self.date_label = tk.Label(self.root, text=f"Today's Date: {datetime.now().strftime('%Y-%m-%d')}", font=("Arial", 14), bg="#f0f0f0")
        self.date_label.pack(pady=10)

        # Widgets for account creation
        self.create_account_frame = self.create_section_frame(root, "Account Creation", "#f1f1f1")
        
        self.acc_num_label = self.create_label(self.create_account_frame, "Account Number:")
        self.acc_num_entry = self.create_entry(self.create_account_frame)

        self.acc_holder_label = self.create_label(self.create_account_frame, "Account Holder:")
        self.acc_holder_entry = self.create_entry(self.create_account_frame)

        self.initial_balance_label = self.create_label(self.create_account_frame, "Initial Balance:")
        self.initial_balance_entry = self.create_entry(self.create_account_frame)

        self.create_acc_button = self.create_button(self.create_account_frame, "Create Account", "blue", self.create_account)

        # Widgets for transactions
        self.transaction_frame = self.create_section_frame(root, "Transactions", "#e9f7fc")

        self.trans_acc_num_label = self.create_label(self.transaction_frame, "Account Number:")
        self.trans_acc_num_entry = self.create_entry(self.transaction_frame)

        self.amount_label = self.create_label(self.transaction_frame, "Amount:")
        self.amount_entry = self.create_entry(self.transaction_frame)

        self.deposit_button = self.create_button(self.transaction_frame, "Deposit", "green", self.deposit)
        self.withdraw_button = self.create_button(self.transaction_frame, "Withdraw", "red", self.withdraw)

        # Widgets for account information
        self.info_frame = self.create_section_frame(root, "Account Info", "#d1ecf1")

        self.info_acc_num_label = self.create_label(self.info_frame, "Account Number:")
        self.info_acc_num_entry = self.create_entry(self.info_frame)

        self.info_button = self.create_button(self.info_frame, "Display Info", "purple", self.display_info)

    def create_section_frame(self, parent, section_title, bg_color):
        frame = tk.Frame(parent, bg=bg_color, bd=5, relief="solid", padx=20, pady=20)
        frame.pack(pady=20, padx=30, fill="x")

        section_title_label = tk.Label(frame, text=section_title, font=("Arial", 16, "bold"), bg=bg_color)
        section_title_label.grid(row=0, columnspan=2, pady=10)

        return frame

    def create_label(self, parent, text):
        label = tk.Label(parent, text=text, font=self.font, bg=parent.cget("bg"))
        label.grid(padx=10, pady=5, sticky="w")
        return label

    def create_entry(self, parent):
        entry = tk.Entry(parent, font=self.font, bd=3, relief="sunken")
        entry.grid(padx=10, pady=5, sticky="w")
        return entry

    def create_button(self, parent, text, color, command):
        button = tk.Button(parent, text=text, font=self.font, bg=color, fg="white", relief="raised", bd=4, command=command)
        button.grid(padx=10, pady=10)
        return button

    def create_account(self):
        acc_num = self.acc_num_entry.get()
        acc_holder = self.acc_holder_entry.get()
        initial_balance = float(self.initial_balance_entry.get())

        if acc_num and acc_holder:
            self.accounts[acc_num] = Account(acc_num, acc_holder, initial_balance)
            messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showwarning("Error", "Account number and holder name cannot be empty!")

    def deposit(self):
        acc_num = self.trans_acc_num_entry.get()
        amount = float(self.amount_entry.get())

        if acc_num in self.accounts:
            try:
                self.accounts[acc_num].deposit(amount)
                messagebox.showinfo("Success", f"Deposited {amount}. New balance is {self.accounts[acc_num].get_balance()}.")
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
        else:
            messagebox.showwarning("Error", "Account not found!")

    def withdraw(self):
        acc_num = self.trans_acc_num_entry.get()
        amount = float(self.amount_entry.get())

        if acc_num in self.accounts:
            try:
                self.accounts[acc_num].withdraw(amount)
                messagebox.showinfo("Success", f"Withdrew {amount}. New balance is {self.accounts[acc_num].get_balance()}.")
            except InsufficientFundsError as e:
                messagebox.showwarning("Error", str(e))
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
        else:
            messagebox.showwarning("Error", "Account not found!")

    def display_info(self):
        acc_num = self.info_acc_num_entry.get()

        if acc_num in self.accounts:
            account_info = self.accounts[acc_num].display_account_info()
            messagebox.showinfo("Account Info", account_info)
        else:
            messagebox.showwarning("Error", "Account not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystem(root)
    root.mainloop()
