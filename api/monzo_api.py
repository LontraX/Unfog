import requests
import os
from urllib.parse import urlencode

class MonzoAPI:
    BASE_URL = "https://api.monzo.com"

    def __init__(self):
        self.client_id = os.getenv("MONZO_CLIENT_ID")
        self.client_secret = os.getenv("MONZO_CLIENT_SECRET")
        self.redirect_uri = os.getenv("MONZO_REDIRECT_URI")
        self.access_token = os.getenv("MONZO_ACCESS_TOKEN")

    def get_accounts(self):
        """Retrieve accounts for the user."""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        url = f"{self.BASE_URL}/accounts"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch accounts: " + response.text)
        
    def get_balance_by_account_id(self, account_id):
        """Retrieve the balance for a specific account by its ID."""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        account_id = ""
        url = f"{self.BASE_URL}/balance?account_id={account_id}"  # Add account_id as a query parameter
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch balance: " + response.text)
        
    def get_pots(self, account_id):
        """Retrieve the pots for a specific account by its ID."""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        account_id = ""
        url = f"{self.BASE_URL}/pots?current_account_id={account_id}" 
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch pots: " + response.text)
        
    def deposit_to_pot(self, pot_id, account_id, amount, dedupe_id):
        """Deposit money into a specific pot."""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = f"{self.BASE_URL}/pots/{pot_id}/deposit"
        data = {
            'source_account_id': account_id,
            'amount': amount,          # Amount in minor units (e.g., pennies for GBP)
            'dedupe_id': dedupe_id     # Unique identifier to prevent duplicate transactions
        }
        response = requests.put(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the updated pot details
        else:
            raise Exception("Failed to deposit to pot: " + response.text)

    def withdraw_from_pot(self, pot_id, account_id, amount, dedupe_id):
        """Withdraw money from a specific pot into a user's account."""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = f"{self.BASE_URL}/pots/{pot_id}/withdraw"
        data = {
            'destination_account_id': account_id,  # ID of the account to receive the funds
            'amount': amount,                      # Amount to withdraw in minor units (e.g., pennies for GBP)
            'dedupe_id': dedupe_id                 # Unique identifier to prevent duplicate transactions
        }
        response = requests.put(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the updated pot details after the withdrawal
        else:
            raise Exception("Failed to withdraw from pot: " + response.text)
        
    def get_transactions(self, account_id):
        """
        Retrieve transactions for the user's account.

        Args:
            account_id (str): The ID of the account to retrieve transactions for.

        Returns:
            list: A list of transaction dictionaries.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
            ValueError: If the response does not contain the expected 'transactions' key.
        """
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'account_id': account_id
        }
        url = f"{self.BASE_URL}/transactions"

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            if 'transactions' not in data:
                raise ValueError("Response JSON does not contain 'transactions' key.")

            transactions = data['transactions']
            print(f"Retrieved {len(transactions)} transactions for account {account_id}.")
            return transactions

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            print(f"An error occurred: {err}")
            raise
        
    def get_transaction_by_transaction_id(self, transaction_id):
        """Retrieve a specific transaction, expanding merchant details."""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        url = f"{self.BASE_URL}/transactions/{transaction_id}?expand[]=merchant"  # Expand merchant details
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the transaction data with expanded merchant details
        else:
            raise Exception("Failed to fetch transaction: " + response.text)
