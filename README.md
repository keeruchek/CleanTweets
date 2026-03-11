# 🐦 CleanTweets - Twitter Sentiment Analysis

A cloud-native Twitter sentiment analysis application built with Streamlit, TextBlob, and the Twitter API.

## 📋 Features

- **Real-time Tweet Fetching**: Fetch tweets using Twitter API v2
- **Sentiment Analysis**: Classify tweets as positive, negative, or neutral
- **Emotion Detection**: Identify emotions in tweets using text2emotion
- **Interactive Dashboard**: Beautiful visualizations with Streamlit
- **Data Export**: Download analysis results as CSV
- **Secure Credentials**: Environment variable-based configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Twitter API Credentials (Get from [Twitter Developer Portal](https://developer.twitter.com/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/keeruchek/CleanTweets.git
cd CleanTweets
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your Twitter API credentials
```

5. **Run the app**
```bash
streamlit run streamlit_app.py
```

## 🔐 Configuration

Create a `.env` file in the project root:

```env
TWITTER_CONSUMER_KEY=your_key_here
TWITTER_CONSUMER_SECRET=your_secret_here
TWITTER_ACCESS_TOKEN=your_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret_here
```

Get your credentials from the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard).

## 📊 Project Structure

```
CleanTweets/
├── streamlit_app.py         # Main Streamlit application
├── sentiment_plot.py         # Core sentiment analysis logic
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## 📈 How It Works

1. **Tweet Collection**: Input search terms and fetch tweets from Twitter
2. **Cleaning**: Remove URLs, mentions, and special characters
3. **Sentiment Analysis**: Use TextBlob's polarity scores to classify sentiment
4. **Emotion Detection**: Identify specific emotions using text2emotion library
5. **Visualization**: Display results with pie charts and bar graphs

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy `streamlit_app.py`
5. Add secrets in Streamlit Cloud dashboard:
   - TWITTER_CONSUMER_KEY
   - TWITTER_CONSUMER_SECRET
   - TWITTER_ACCESS_TOKEN
   - TWITTER_ACCESS_TOKEN_SECRET

### Deploy Locally

```bash
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

## 🛠️ Technologies Used

- **Streamlit**: Web app framework
- **Tweepy**: Twitter API client
- **TextBlob**: Sentiment analysis
- **text2emotion**: Emotion detection
- **Pandas**: Data manipulation
- **Matplotlib**: Data visualization
- **Python-dotenv**: Environment management

## 📝 Example Usage

```python
from sentiment_plot import TwitterClient

# Initialize client
client = TwitterClient()

# Fetch and analyze tweets
tweets = client.get_tweets(query='Python', count=100)

# Tweets will contain sentiment labels
for tweet in tweets:
    print(f"{tweet['text']}: {tweet['sentiment']}")
```

## ⚠️ Important Notes

- **API Rate Limits**: Twitter API has rate limits. Check documentation.
- **Deprecated API Methods**: Update to Twitter API v2 endpoints if needed
- **Credentials Security**: Never commit `.env` file to git

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - see LICENSE file for details

## 📧 Support

For issues and questions, please open a GitHub issue.