import streamlit as st
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import preprocessor as p
import text2emotion as te
import matplotlib.pyplot as plt
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="CleanTweets", layout="wide", initial_sidebar_state="expanded")

# Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        color: #1DA1F2;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">🐦 CleanTweets - Sentiment Analysis</div>', unsafe_allow_html=True)

class TwitterClient:
    """Twitter API client for fetching and analyzing tweets."""
    
    def __init__(self):
        try:
            consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
            consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            
            if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
                raise ValueError("Missing Twitter API credentials in .env file")
            
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(auth)
        except Exception as e:
            st.error(f"Authentication failed: {e}")
            self.api = None
    
    def clean_tweet(self, tweet):
        """Clean tweet text by removing links and special characters."""
        return ' '.join(p.clean(tweet).split())
    
    def get_tweet_sentiment(self, tweet):
        """Classify sentiment using TextBlob."""
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweets(self, query, count=100):
        """Fetch tweets and analyze sentiment."""
        tweets = []
        try:
            fetched_tweets = self.api.search_tweets(q=query, count=count, lang="en", tweet_mode="extended")
            
            for tweet in fetched_tweets:
                parsed_tweet = {
                    'text': tweet.full_text,
                    'sentiment': self.get_tweet_sentiment(tweet.full_text),
                    'retweets': tweet.retweet_count,
                    'likes': tweet.favorite_count
                }
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            
            return tweets
        except tweepy.TweepError as e:
            st.error(f"Error fetching tweets: {e}")
            return []

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
query = st.sidebar.text_input("Enter search term:", value="Python", placeholder="e.g., AI, Machine Learning")
tweet_count = st.sidebar.slider("Number of tweets to fetch:", 10, 200, 100)
fetch_button = st.sidebar.button("Fetch Tweets", key="fetch_button")

# Main Content Area
if fetch_button or 'tweets' in st.session_state:
    if fetch_button:
        with st.spinner("🔄 Fetching tweets..."):
            twitter_client = TwitterClient()
            if twitter_client.api:
                st.session_state.tweets = twitter_client.get_tweets(query, tweet_count)
    
    if st.session_state.get('tweets'):
        tweets = st.session_state.tweets
        
        # Calculate Statistics
        total_tweets = len(tweets)
        positive_tweets = [t for t in tweets if t['sentiment'] == 'positive']
        negative_tweets = [t for t in tweets if t['sentiment'] == 'negative']
        neutral_tweets = [t for t in tweets if t['sentiment'] == 'neutral']
        
        pos_pct = (len(positive_tweets) / total_tweets * 100) if total_tweets > 0 else 0
        neg_pct = (len(negative_tweets) / total_tweets * 100) if total_tweets > 0 else 0
        neu_pct = (len(neutral_tweets) / total_tweets * 100) if total_tweets > 0 else 0
        
        # Display Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tweets", total_tweets)
        with col2:
            st.metric("😊 Positive", f"{len(positive_tweets)} ({pos_pct:.1f}%)")
        with col3:
            st.metric("😐 Neutral", f"{len(neutral_tweets)} ({neu_pct:.1f}%)")
        with col4:
            st.metric("😞 Negative", f"{len(negative_tweets)} ({neg_pct:.1f}%)")
        
        # Visualization
        st.subheader("📊 Sentiment Distribution")
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart
            labels = ['Positive', 'Neutral', 'Negative']
            sizes = [len(positive_tweets), len(neutral_tweets), len(negative_tweets)]
            colors = ['#28a745', '#ffc107', '#dc3545']
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Sentiment Analysis for '{query}'")
            st.pyplot(fig)
        
        with col2:
            # Bar Chart
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(labels, sizes, color=colors)
            ax.set_ylabel('Number of Tweets')
            ax.set_title('Tweet Count by Sentiment')
            st.pyplot(fig)
        
        # Display Tweets
        st.subheader("📱 Tweet Details")
        
        tabs = st.tabs(["Positive", "Neutral", "Negative"])
        
        with tabs[0]:
            st.write(f"**{len(positive_tweets)} Positive Tweets**")
            for tweet in positive_tweets[:10]:
                st.write(f"✅ {tweet['text']}")
                st.write(f"❤️ {tweet['likes']} | 🔄 {tweet['retweets']}")
                st.divider()
        
        with tabs[1]:
            st.write(f"**{len(neutral_tweets)} Neutral Tweets**")
            for tweet in neutral_tweets[:10]:
                st.write(f"➖ {tweet['text']}")
                st.write(f"❤️ {tweet['likes']} | 🔄 {tweet['retweets']}")
                st.divider()
        
        with tabs[2]:
            st.write(f"**{len(negative_tweets)} Negative Tweets**")
            for tweet in negative_tweets[:10]:
                st.write(f"❌ {tweet['text']}")
                st.write(f"❤️ {tweet['likes']} | 🔄 {tweet['retweets']}")
                st.divider()
        
        # Download Results
        df = pd.DataFrame(tweets)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f"tweets_{query}.csv",
            mime="text/csv"
        )
    else:
        st.info("👈 Enter a search term and click 'Fetch Tweets' to get started!")
else:
    st.info("👈 Enter a search term and click 'Fetch Tweets' to get started!")

st.sidebar.divider()
st.sidebar.info("**CleanTweets** | Sentiment Analysis powered by Streamlit & Twitter API")
