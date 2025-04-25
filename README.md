# Unfog

### A WhatsApp-based Personal Finance Assistant Using Monzo API and Multi-Agent Swarm

---

## Project Overview
"Unfog" is a personal finance assistant that simplifies financial management by letting users interact with smart agents via WhatsApp. The project uses the Monzo API and the Swarm framework for multi-agent collaboration to provide users with clear insights into their finances, helping them budget, save, track expenses, and more—all through natural language conversations.

### Key Features
- **WhatsApp-Based Interaction**: Access financial information and take actions simply by chatting with Unfog on WhatsApp.
- **Multi-Agent System**: Specialized agents handle different financial tasks (budgeting, savings, spending categorization, etc.).
- **Natural Language Understanding**: Users interact naturally via questions and commands like “How much have I spent on groceries this month?” or “Help me save £50.”
- **Real-time Notifications**: Alerts for spending thresholds, savings opportunities, and potential fraud.
- **Seamless Financial Management**: Monitor spending, adjust budgets, manage subscriptions, and much more, all through simple text interactions.

---

## How It Works
1. **Connect with WhatsApp**: Users interact with the system by chatting with the Unfog bot via WhatsApp.
2. **Multi-Agent Collaboration**: Different financial tasks (e.g., tracking bills, managing budgets, saving goals) are handled by independent agents using the Swarm framework.
3. **Monzo API Integration**: The system pulls real-time transaction and account data from Monzo to offer personalized insights and suggestions.
4. **Natural Language Processing**: Users type queries or commands in natural language, which are interpreted by the NLP engine, and tasks are delegated to the appropriate agents.

---

## Agent Overview
Each agent in the Swarm framework plays a specific role:

1. **Transaction Monitor Agent**: Fetches transactions from Monzo and routes them to relevant agents.
2. **Budget Analyzer Agent**: Tracks spending against budgets and provides alerts.
3. **Savings Planner Agent**: Helps users reach savings goals by monitoring spending patterns and income.
4. **Expense Categorization Agent**: Automatically categorizes transactions and learns from user input.

---

## Setup and Installation

### Prerequisites
- WhatsApp Business API Access
- Monzo API access and authentication
- OpenAI for natural language understanding

### Installation Steps
1. Clone the repository.
    ```bash
    git clone https://github.com/LontraX/unfog.git
    cd unfog
    ```
2. Set up the required environment variables for Monzo API and WhatsApp API.
3. Install dependencies:
    
4. Run the server:
    

---

## How to Use

1. **Connect Your Monzo Account**: Follow the link to authenticate with Monzo.
2. **Start a Conversation**: Send a message on WhatsApp to the Unfog bot, like “What’s my balance?” or “Help me save £20 this month.”
3. **Receive Real-Time Insights**: The bot will respond based on the information provided by Monzo and processed by different agents.

---

## Contributing
We welcome contributions from the open-source community! To get started:
- Fork the repository.
- Submit pull requests with clear descriptions of your changes.

---

## Future Plans
- Expand agent capabilities (e.g., investments, credit tracking).
- Integrate with other banks and financial services.
- Build a web dashboard for more detailed insights.

---

## License


---

## Contact
If you have any questions or feedback, feel free to reach out to [olumidejoda@gmail.com].
