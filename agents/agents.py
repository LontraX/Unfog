import random
import os
from swarm import Agent, Swarm
from api import monzo_api as mapi
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variables
openai_client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
client = Swarm(client=openai_client )

# Create an instance of MonzoAPI
monzo_api = mapi.MonzoAPI()


# External Monzo API Functions ( will make gneric later )

def retrieve_accounts():
    """Retrieve a list of user accounts."""
    accounts = monzo_api.get_accounts()
    print("Accounts retrieved:", accounts)
    return accounts

def retrieve_balance(account_id):
    """Retrieve the balance for a specific account."""
    balance = monzo_api.get_balance_by_account_id(account_id)
    print(f"Balance for account {account_id}: {balance}")
    return balance

def retrieve_pots(account_id):
    """Retrieve a list of pots for a specific account."""
    pots = monzo_api.get_pots(account_id)
    print(f"Pots for account {account_id}: {pots}")
    return pots

def deposit_into_pot(pot_id, account_id, amount):
    """Deposit money into a specific pot."""
    dedupe_id = str(random.randint(10000, 99999))  # Generate a unique dedupe ID
    pot = monzo_api.deposit_to_pot(pot_id, account_id, amount, dedupe_id)
    print(f"Deposited {amount} into pot {pot_id}: {pot}")
    return pot

def withdraw_from_pot(pot_id, account_id, amount):
    """Withdraw money from a specific pot."""
    dedupe_id = str(random.randint(10000, 99999))  # Generate a unique dedupe ID
    pot = monzo_api.withdraw_from_pot(pot_id, account_id, amount, dedupe_id)
    print(f"Withdrew {amount} from pot {pot_id}: {pot}")
    return pot

def get_transaction_details(transaction_id):
    """Retrieve details of a specific transaction, including merchant info."""
    transaction = monzo_api.get_transaction(transaction_id)
    print(f"Transaction details for {transaction_id}: {transaction}")
    return transaction

def get_recent_transactions(account_id):
    """Retrieve a list of recent transactions for an account."""
    transactions = monzo_api.get_transactions(account_id)
    print(f"Transactions for user {transactions}")
    return transactions

# Transfer Functions to Switch Between Agents ( will refactor this later )

def transfer_to_account_management():
    """Transfer the user to the Account Management Agent."""
    return account_management_agent

def transfer_to_savings_management():
    """Transfer the user to the Savings Management Agent."""
    return savings_management_agent

def transfer_to_transaction_lookup():
    """Transfer the user to the Transaction Lookup Agent."""
    return transaction_lookup_agent

def transfer_to_transaction_monitoring():
    """Transfer the user to the Transaction Monitoring Agent."""
    return transaction_monitoring_agent

def transfer_to_analytics_agent():
    """Transfer the user to the Analytics Agent."""
    return analytics_agent

def transfer_back_to_triage():
    """
    Transfer the user back to the Triage Agent.
    Use this function if the current agent cannot handle the user's request.
    """
    return triage_agent

# Agents Definition with Detailed Instructions (improve this later)

# Account Management Agent
account_management_agent = Agent(
    name="Account Management Agent",
    description="Manage and retrieve user account information.",
    instructions="""
    The Account Management Agent handles all requests related to user accounts.
    - Retrieve a list of user accounts.
    - Get the balance of a specific account.
    - Provide account details upon request.
    If the request is not related to account management, transfer it back to the Triage Agent.
    """,
    functions=[retrieve_accounts, retrieve_balance, transfer_back_to_triage]
)

# Savings Management Agent (Pots Manager)
savings_management_agent = Agent(
    name="Savings Management Agent",
    description="Manage the user's Monzo Pots (savings), including deposits and withdrawals.",
    instructions="""
    The Savings Management Agent is responsible for all interactions related to Monzo Pots.
    - Retrieve a list of pots for a specific account.
    - Deposit money into a pot.
    - Withdraw money from a pot.
    - Provide information about pot balances and transactions.
    If the request does not pertain to savings management, transfer it back to the Triage Agent.
    """,
    functions=[retrieve_pots, deposit_into_pot, withdraw_from_pot, transfer_back_to_triage]
)

# Transaction Lookup Agent
transaction_lookup_agent = Agent(
    name="Transaction Lookup Agent",
    description="Help the user track and retrieve specific transaction details.",
    instructions="""
    The Transaction Lookup Agent assists users in finding detailed information about specific transactions.
    - Retrieve details of a particular transaction, including merchant information.
    - Provide summaries or specifics based on transaction IDs.
    - Assist in identifying transactions that the user may not recognize.
    If the request is not related to transaction lookup, transfer it back to the Triage Agent.
    """,
    functions=[get_transaction_details, transfer_back_to_triage]
)

# Transaction Monitoring Agent
transaction_monitoring_agent = Agent(
    name="Transaction Monitoring Agent",
    description="Monitor and list recent transactions.",
    instructions="""
    The Transaction Monitoring Agent monitors and provides information about recent transactions.
    - Retrieve a list of the latest transactions for a user's account.
    - Offer summaries of spending patterns over recent periods.
    - Alert users to unusual or large transactions.
    If the request does not involve transaction monitoring, transfer it back to the Triage Agent.
    """,
    functions=[get_recent_transactions, transfer_back_to_triage]
)

# Analytics Agent
analytics_agent = Agent(
    name="Analytics Agent",
    description="Provide spending analysis and transaction insights.",
    instructions="""
    The Analytics Agent offers in-depth analysis and insights into the user's spending habits and financial data.
    - Analyze spending patterns and provide summaries.
    - Offer personalized financial advice based on transaction history.
    - Generate reports on monthly or yearly expenditures.
    - Provide insights into saving opportunities and budgeting tips.
    If the request does not pertain to analytics, transfer it back to the Triage Agent.
    """,
    functions=[transfer_back_to_triage,get_recent_transactions,get_transaction_details,retrieve_accounts, retrieve_balance]
)

# Triage Agent
triage_agent = Agent(
    name="Triage Agent",
    description="Initial point of contact to direct user requests to the appropriate agent.",
    instructions="""
    The Triage Agent is responsible for understanding the user's request and directing it to the appropriate specialized agent.
    - For account-related requests, transfer to the Account Management Agent.
    - For deposit and withdrawal of money-related requests, transfer to the Savings Management Agent.
    - For specific transaction details, transfer to the Transaction Lookup Agent.
    - For monitoring recent transactions, transfer to the Transaction Monitoring Agent.
    - For spending insights and analytics, transfer to the Analytics Agent.
    - If the request does not match any of the above categories, ask for clarification or provide a default response.
    """,
    functions=[
        transfer_to_account_management,
        transfer_to_savings_management,
        transfer_to_transaction_lookup,
        transfer_to_transaction_monitoring,
        transfer_to_analytics_agent
    ]
)

agents_list = [
    triage_agent,
    account_management_agent,
    savings_management_agent,
    transaction_lookup_agent,
    transaction_monitoring_agent,
    analytics_agent
]

def process_message(message):
    messages = [{"role": "user", "content": message}]
    response = client.run(agent=triage_agent, messages=messages)
    print(response.messages[-1]["content"])
    return response.messages[-1]["content"]
