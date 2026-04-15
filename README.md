CleanTweets: Real-time NLP Content Guard
CleanTweets is a robust, production-grade NLP pipeline designed for real-time automated content moderation. Originally architected for Twitter/X, this project has evolved into a high-performance Reddit-based monitoring system capable of detecting offensive content with high precision and sub-second inference latency.

Key Features & Engineering Highlights
Real-Time NLP Pipeline: Leverages unitary/toxic-bert Transformers and scikit-learn to classify content across multi-class sentiment categories, achieving 90% accuracy in offensive content detection.

Low-Latency Inference: Engineered for high-throughput streaming with sub-1s inference latency, enabling immediate moderation responses in simulated and live environments.

Hybrid Moderation Logic: Combines rule-based keyword filtering (for immediate high-speed blocks) with model-driven semantic analysis (for nuanced content understanding).

Scalable Architecture: Deployed via Streamlit, utilizing secret-managed API integration to ensure platform security and adherence to the Reddit Responsible Builder Policy.

Architecture Overview
The application follows a modular design pattern:

Ingestion Layer: Utilizes praw to stream real-time submissions from specified subreddits.

Processing Layer: A dual-stage filter that checks against hard-coded triggers before running text through the Transformer model.

Visualization Layer: A dynamic, real-time dashboard built with Streamlit that logs moderation status, latency metrics, and classification scores.

Project Setup
To run this project locally, ensure you have your Reddit API credentials and follow these steps:

Clone the repository:

Bash
git clone https://github.com/keeruchek/CleanTweets
cd CleanTweets
Install dependencies:

Bash
pip install -r requirements.txt
Configure Secrets: Create a file .streamlit/secrets.toml and add:

Ini, TOML
REDDIT_CLIENT_ID = "YOUR_ID"
REDDIT_CLIENT_SECRET = "YOUR_SECRET"
REDDIT_USERNAME = "YOUR_USERNAME"
Launch the App:

Bash
streamlit run app.py
Performance & Safety
This system improves platform safety by reducing exposure to harmful content. By automating moderation, CleanTweets demonstrates the ability to manage large-scale data streams efficiently while maintaining high safety standards.

Final Polish for your Repo:

Delete old files: As discussed, remove your venv, local data files, and any old API keys.

Commit the README.md: This file is the "face" of your repo for recruiters.

Link the Demo: If you deploy it on Streamlit Cloud, add the URL at the top of this README so visitors can click and see the app in action immediately.

Does this README.md accurately capture the professional engineering scope you want to highlight for your portfolio?
