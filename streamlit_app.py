import streamlit as st
import tweepy
import pandas as pd
import time
from transformers import pipeline
from sklearn.metrics import accuracy_score

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="CleanTweets - AI Content Moderation", layout="wide")
st.title("🛡️ CleanTweets: Real-time NLP Content Guard")

# --- INITIALIZE MODEL ---
# Using a high-performance transformer model for offensive content detection
@st.cache_resource
def load_model():
    # 'cardiffnlp/twitter-roberta-base-sentiment-latest' is excellent for multi-class
    # For offensive content, we use a specialized distilbert model for sub-1s latency
    return pipeline("text-classification", model="unitary/toxic-bert", device=-1)

classifier = load_model()

# --- RULE-BASED FILTERING ENGINE ---
def rule_based_check(text):
    blocked_keywords = ["badword1", "spamlink.com", "bot_attack"] # Add custom triggers
    for word in blocked_keywords:
        if word in text.lower():
            return True, "Rule-based: Keyword Filtered"
    return False, None

# --- STREAMLIT SIDEBAR (API SETTINGS) ---
st.sidebar.header("Settings")
mode = st.sidebar.radio("Input Source", ["Simulation (Demo)", "Live Twitter Stream"])
threshold = st.sidebar.slider("Sensitivity Threshold", 0.0, 1.0, 0.8)

# API Keys (For Live Mode)
bearer_token = st.sidebar.text_input("Twitter Bearer Token", type="password")

# --- CORE LOGIC ---
def process_tweet(tweet_text):
    start_time = time.time()
    
    # 1. Rule-based check
    is_blocked, reason = rule_based_check(tweet_text)
    
    if not is_blocked:
        # 2. Model-driven check
        prediction = classifier(tweet_text)[0]
        latency = time.time() - start_time
        
        if prediction['score'] > threshold and prediction['label'] != 'neutral':
            return {
                "status": "🔴 BLOCKED",
                "content": tweet_text,
                "reason": f"Model-driven ({prediction['label']})",
                "latency": f"{latency:.3f}s",
                "score": round(prediction['score'], 3)
            }
    else:
        latency = time.time() - start_time
        return {
            "status": "🔴 BLOCKED",
            "content": tweet_text,
            "reason": reason,
            "latency": f"{latency:.3f}s",
            "score": "N/A"
        }

    return {
        "status": "🟢 CLEAN",
        "content": tweet_text,
        "reason": "Safe Content",
        "latency": f"{time.time() - start_time:.3f}s",
        "score": "N/A"
    }

# --- UI EXECUTION ---
if mode == "Simulation (Demo)":
    st.info("Running in simulation mode with sample data.")
    sample_tweets = [
        "I love this new update! Great work.",
        "This is a total scam, click here now: spamlink.com",
        "You are absolutely terrible and I hate you.",
        "The weather is quite nice today in San Francisco.",
        "Stop being such a loser and get a life."
    ]
    
    if st.button("Start Simulation"):
        results_placeholder = st.empty()
        data = []
        for tweet in sample_tweets:
            res = process_tweet(tweet)
            data.append(res)
            # Update UI table in real-time
            results_placeholder.table(pd.DataFrame(data))
            time.sleep(0.5) # Simulate stream delay

elif mode == "Live Twitter Stream":
    if not bearer_token:
        st.warning("Please enter your Twitter Bearer Token in the sidebar.")
    else:
        st.write("🔄 Connecting to X Stream...")
        # Stream Listener setup would go here using tweepy.StreamingClient
        st.error("Live Stream requires an elevated X API Developer account.")
        # Minimal implementation for streaming:
        # class MyStream(tweepy.StreamingClient):
        #     def on_tweet(self, tweet):
        #         res = process_tweet(tweet.text)
        #         st.write(res)                    'retweets': tweet.retweet_count,
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
