# 🤖 Telegram BIST Bot - Interactive Stock Analysis

A comprehensive Telegram bot for BIST (Borsa Istanbul) stock analysis, featuring multiple technical analysis methods including moving averages, RSI, momentum analysis, and AI-powered predictions using machine learning.

## ✨ Features

- **📊 Multiple Analysis Methods**: Moving averages, RSI, momentum, and AI predictions
- **🤖 Machine Learning Integration**: RandomForest algorithm for stock price predictions
- **📈 Real-time Data**: Live stock data from Yahoo Finance
- **🎯 BIST 100 Coverage**: Complete analysis of BIST 100 index stocks
- **📱 Interactive Interface**: User-friendly Telegram bot interface with inline keyboards
- **🔍 Individual Stock Analysis**: Detailed analysis for specific stocks
- **📊 Top 5 Stock Recommendations**: AI-powered stock selection system
- **⚡ Fast Response**: Optimized for quick analysis and responses

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Framework**: python-telegram-bot
- **Data Source**: Yahoo Finance (yfinance)
- **Machine Learning**: scikit-learn (RandomForest)
- **Data Processing**: pandas
- **Analysis**: Technical indicators (RSI, Moving Averages, Momentum)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Internet connection for real-time data

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PythonProjects
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Telegram bot**
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Copy the bot token

4. **Configure the bot**
   - Open `telegram_bist_bot.py`
   - Replace `'TELEGRAM_TOKEN_HERE'` with your actual bot token
   ```python
   TOKEN = 'your_actual_bot_token_here'
   ```

5. **Run the bot**
   ```bash
   python telegram_bist_bot.py
   ```

6. **Start using the bot**
   - Find your bot on Telegram
   - Send `/start` to begin

## 📁 Project Structure

```
PythonProjects/
├── telegram_bist_bot.py    # Main bot application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── LICENSE                # MIT License
└── .gitignore            # Git ignore file
```

## 🎯 Bot Functions

### 1. **BIST 100 Moving Average Analysis**
- Analyzes all BIST 100 stocks for moving average signals
- Identifies stocks below MA50, MA100, and MA200
- Shows current price vs moving averages

### 2. **Individual Stock Moving Average Analysis**
- Enter any stock code for detailed MA analysis
- Compares current price with 50, 100, and 200-day moving averages
- Provides buy/sell recommendations

### 3. **AI-Powered Stock Analysis**
- Uses RandomForest machine learning algorithm
- Analyzes 1 year of historical data
- Predicts stock price direction (up/down)
- Shows prediction accuracy

### 4. **RSI (Relative Strength Index) Analysis**
- Calculates RSI for all BIST 100 stocks
- Identifies oversold/overbought conditions
- Shows top 10 buying opportunities

### 5. **Momentum Analysis**
- Calculates 10-day momentum for stocks
- Identifies strongest momentum stocks
- Shows percentage change over 10 days

### 6. **Top 5 Stock Recommendations**
- Combines all analysis methods
- Scores stocks based on multiple factors
- Provides comprehensive recommendations

## 🔧 Configuration

### Environment Setup
1. **Python Environment**: Ensure Python 3.8+ is installed
2. **Dependencies**: Install required packages
3. **Telegram Bot**: Create and configure bot token
4. **Data Access**: Internet connection for Yahoo Finance data

### Customization Options
- **BIST 100 Symbols**: Modify `BIST100_SYMBOLS` list
- **Analysis Parameters**: Adjust RSI periods, moving average windows
- **Machine Learning**: Modify RandomForest parameters
- **Response Messages**: Customize bot responses and warnings

## 📦 Dependencies

Create a `requirements.txt` file with:

```txt
python-telegram-bot>=20.0
pandas>=1.5.0
yfinance>=0.2.0
scikit-learn>=1.1.0
numpy>=1.21.0
```

## 🌐 Deployment

### Local Development
```bash
python telegram_bist_bot.py
```

### Cloud Deployment
- **Heroku**: Deploy as Python app
- **Railway**: Connect GitHub repository
- **DigitalOcean**: Deploy on droplet
- **AWS**: Use EC2 or Lambda

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "telegram_bist_bot.py"]
```

## 🔒 Security & Privacy

### Important Notes
- **No Personal Data Storage**: Bot doesn't store user data
- **Public Data Only**: Uses publicly available stock data
- **Educational Purpose**: Analysis is for educational purposes only
- **No Investment Advice**: Not financial advice, use at your own risk

### API Keys
- **Telegram Bot Token**: Keep your bot token secure
- **No External APIs**: Uses free Yahoo Finance data

## 🎨 Customization Guide

### Adding New Analysis Methods
1. Create new analysis function
2. Add to `handle_choice` function
3. Update menu options
4. Add corresponding message handler

### Modifying Stock List
```python
BIST100_SYMBOLS = [
    "YOUR_STOCK.IS",
    "ANOTHER_STOCK.IS"
]
```

### Customizing Responses
- Modify `UYARI_MESAJI` for custom warnings
- Update analysis explanations
- Customize recommendation messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Bot Not Responding**
   - Check bot token is correct
   - Ensure bot is not blocked
   - Verify internet connection

2. **Data Fetching Errors**
   - Check Yahoo Finance availability
   - Verify stock symbols are correct
   - Ensure stable internet connection

3. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility
   - Verify package versions

4. **Analysis Errors**
   - Check stock symbol format (should end with .IS)
   - Verify data availability for specific stocks
   - Check for sufficient historical data

## 📞 Support

If you encounter any issues or have questions:

1. Search existing [GitHub issues](https://github.com/earkali/stock-broker-bot/issues)
2. Create a new issue with detailed description

## ⚠️ Disclaimer

**IMPORTANT**: This bot is for educational purposes only. The analysis provided is not financial advice. Always do your own research before making investment decisions. The developers are not responsible for any financial losses.

---

<div align="center">

**Made with ❤️ by [@earkali](https://github.com/earkali)**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/earkali)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/earkali)

*"The stock market is a device for transferring money from the impatient to the patient."* - Warren Buffett

</div> 
