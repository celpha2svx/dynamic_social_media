# 📊 DYNAMIC_SOCIAL_MEDIA_ANALYZER

*Real-Time Reddit Sentiment & Trend Analysis with AI-Powered Insights*

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?logo=chainlink&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![Reddit](https://img.shields.io/badge/Reddit-FF4500?logo=reddit&logoColor=white)

---

## 📘 Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [API Configuration](#api-configuration)
  - [Usage](#usage)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🧠 Overview

Dynamic Social Media Analyzer Dashboard is a powerful, interactive platform built with Streamlit that performs real-time sentiment and trend analysis on user-specified Reddit communities. Leveraging PRAW for data collection, Google's Gemini 2.5 Flash for AI-powered insights, and SQLite for historical tracking, it transforms raw social media data into actionable business intelligence.

## Why Dynamic Social Media Analyzer?

Understanding community sentiment and emerging trends is critical for modern businesses and researchers. This analyzer addresses these needs through:

- **Real-Time Data Collection**: Dynamically scrapes top posts and comments from any Reddit community using PRAW's robust API integration.

- **AI-Powered Analysis**: Utilizes Gemini 2.5 Flash via LangChain to generate structured reports with sentiment scores, key trends, and actionable recommendations.

- **Historical Intelligence**: Stores all fetched data in timestamped SQLite tables, enabling trend tracking and longitudinal analysis across multiple runs.

- **Interactive Visualization**: Beautiful Streamlit dashboard displays key metrics, post scores, and keyword clouds for instant insights.

- **Flexible Community Tracking**: Monitor any subreddit from niche communities to major forums, adapting analysis to specific business needs.

- **Structured Reporting**: Generates comprehensive reports with sentiment scores, trend identification, and strategic recommendations for decision-making.

---

## 🚀 Getting Started

### ✅ Prerequisites

This project requires the following dependencies:

- **Programming Language**: Python 3.9+
- **Package Manager**: Pip
- **API Access**: Google Gemini API Key, Reddit API Credentials

---

### 🛠 Installation

Build the Dynamic Social Media Analyzer from source and install dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/dynamic_social_media_analyzer

# Navigate to the project directory
cd dynamic_social_media_analyzer

# Install the dependencies
pip install -r requirements.txt
```

---

### 🔑 API Configuration

This application requires API keys for both Google Gemini and Reddit. Follow these steps carefully:

**Step 1: Get Your Gemini API Key**

Visit [Google AI Studio](https://ai.google.dev/) to obtain your Gemini API key.

**Step 2: Configure Streamlit Secrets**

Create a `.streamlit` folder in the root of your project directory:

```bash
mkdir .streamlit
```

Inside the `.streamlit` folder, create a file named `secrets.toml`:

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_KEY_GOES_HERE"

# Add Reddit API credentials (if required)
REDDIT_CLIENT_ID = "your_reddit_client_id"
REDDIT_CLIENT_SECRET = "your_reddit_client_secret"
REDDIT_USER_AGENT = "your_app_name"
```

⚠️ **Important**: Never commit the `secrets.toml` file to version control. Add `.streamlit/secrets.toml` to your `.gitignore`.

---

### ▶ Usage

Launch the dashboard with:

```bash
streamlit run dashboard.py
```

The application will automatically open in your web browser. Enter any subreddit name (e.g., `r/smallbusiness`, `r/technology`) to begin analysis.

---

## ✨ Features

- **Dynamic Data Fetching**: Scrapes top posts and comments from any user-defined subreddit in real-time
- **Agentic AI Analysis**: Leverages Gemini 2.5 Flash to analyze content and generate structured reports with sentiment scores, key trends, and actionable recommendations
- **Historical Data Storage**: Automatically stores all fetched posts in local SQLite database with timestamped tables for each analysis run
- **Interactive Visualization**: Displays key metrics, post scores, and keyword clouds using modern Streamlit components
- **Flexible Community Monitoring**: Track any Reddit community from niche forums to major subreddits
- **Structured Reporting**: Comprehensive analysis output with sentiment scoring and strategic insights

---

## 📁 Project Structure

```
social_media_analyzer/
├── dashboard.py            # Main Streamlit UI and orchestration logic
├── scrape_data.py          # Reddit data scraping using PRAW
├── analyze_data.py         # AI analysis pipeline with LangChain
├── .streamlit/
│   └── secrets.toml        # API keys (DO NOT COMMIT)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

### Component Breakdown

| File/Folder | Purpose |
|------------|---------|
| `dashboard.py` | Main Streamlit application handling UI, user input, and orchestration |
| `scrape_data.py` | Contains the Executor class using PRAW for data collection and cleaning |
| `analyze_data.py` | Handles AI analysis, prompt engineering, LangChain pipeline, and database I/O |
| `.streamlit/secrets.toml` | Securely stores API keys and credentials (⚠️ DO NOT COMMIT) |
| `requirements.txt` | Lists all Python dependencies (Streamlit, PRAW, LangChain, pandas, etc.) |

---

## 🔧 Technology Stack

- **Frontend**: Streamlit
- **Data Collection**: PRAW (Python Reddit API Wrapper)
- **AI Analysis**: Google Gemini 2.5 Flash via LangChain
- **Data Storage**: SQLite, Pandas
- **Visualization**: Streamlit Charts, Keyword Clouds

---

## 📈 Future Enhancements

Planned features and improvements for upcoming releases:

- **Historical Comparison**: Compare current analysis with previous database runs to identify trend shifts
- **Sentiment Indicators**: Visual color-coded emojis and indicators based on AI sentiment scores
- **Advanced Filtering**: Date range and score-based filtering options within the dashboard
- **Multi-Platform Support**: Expand data extraction pipelines to include Twitter, Facebook, news websites, and other social platforms
- **Export Capabilities**: Download analysis reports in PDF or Excel formats
- **Real-Time Monitoring**: Automated scheduling for continuous community tracking

---

## 📜 License

This project is licensed under the MIT License – Free for educational and commercial use

---

## 🎓 Project Background

This project was completed as part of an advanced Python/AI and Data Science development training curriculum, demonstrating proficiency in:
- API integration and data extraction
- AI-powered analysis and natural language processing
- Database design and management
- Interactive dashboard development
- Production-ready application architecture

---

## 👨‍💻 Author

**Developed by Ademuyiwa Afeez** ✨

*Data Scientist | Building AI-Powered Analytics Solutions*

For contributions, issues, or feature requests, please open a GitHub issue or pull request.

---

## 🔗 Quick Links

- [Streamlit Documentation](https://docs.streamlit.io/)
- [PRAW Documentation](https://praw.readthedocs.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs/)

---
