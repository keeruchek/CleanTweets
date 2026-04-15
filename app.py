import streamlit as st
import tweepy
import pandas as pd
import time
from transformers import pipeline

# --- CONFIGURATION ---
st.set_page_config(page_title="CleanTweets - AI Content Moderation", layout="wide")
st.title("🛡️ CleanTweets: Real-time NLP Content Guard")

# --- MODEL LOADING ---
@st.cache_resource
def load_model():
    # 'unitary/toxic-bert' is optimized for content moderation
    return pipeline("text-classification", model="unitary/toxic-bert", device=-1)

classifier = load_model()

# --- HELPER FUNCTIONS ---
def rule_based_check(text):
    blocked_keywords = ["badword1", "spamlink.com", "bot_attack"]
    for word in blocked_keywords:
        if word in text.lower():
            return True, "Rule-based: Keyword Filtered"
    return False, None

def process_tweet(tweet_text):
    start_time = time.time()
    is_blocked, reason = rule_based_check(tweet_text)
    
    if not is_blocked:
        prediction = classifier(tweet_text)[0]
        latency = time.time() - start_time
        
        # Threshold Logic
        if prediction['score'] > 0.8 and prediction['label'] != 'neutral':
            return {
                "status": "🔴 BLOCKED",
                "content": tweet_text,
                "reason": f"Model: {prediction['label']}",
                "latency": f"{latency:.3f}s"
            }
    else:
        return {
            "status": "🔴 BLOCKED",
            "content": tweet_text,
            "reason": reason,
            "latency": f"{time.time() - start_time:.3f}s"
        }

    return {
        "status": "🟢 CLEAN",
        "content": tweet_text,
        "reason": "Safe",
        "latency": f"{time.time() - start_time:.3f}s"
    }

# --- UI EXECUTION ---
st.sidebar.header("Settings")
mode = st.sidebar.radio("Input Source", ["Simulation (Demo)", "Live Twitter Stream"])

if mode == "Simulation (Demo)":
    st.info("Running in simulation mode.")
    sample_tweets = [
        "I love this new update! Great work.",
        "This is a total scam, click here now: spamlink.com",
        "You are absolutely terrible.",
        "The weather is nice today."
    ]
    
    if st.button("Start Simulation"):
        results = []
        placeholder = st.empty()
        for tweet in sample_tweets:
            res = process_tweet(tweet)
            results.append(res)
            placeholder.table(pd.DataFrame(results))
            time.sleep(0.5)

elif mode == "Live Twitter Stream":
    st.warning("Live Stream requires valid Twitter API v2 Bearer Token.")
    bearer_token = st.sidebar.text_input("Bearer Token", type="password")
    
    if bearer_token:
        # Note: In a production environment, use Streamlit Secrets for the token
        st.write("Stream logic requires a dedicated Class handler. See documentation.")
        st.info("Ensure you are using 'tweepy.StreamingClient' with 'tweet_fields=['public_metrics']'.")
