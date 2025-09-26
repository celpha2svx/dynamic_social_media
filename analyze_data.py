import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import pandas as pd
import sqlite3
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import re
import json

class Analyser:

    def load_data_from_db(self,table_name, db_name='social_media_data.db'):
        """
        Loads data from a specified dynamic table and converts the 'comments'
        column back from a JSON string to a list of Python objects.
        """
        try:
            conn = sqlite3.connect(db_name)
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            conn.close()

            df['comments'] = df['comments'].apply(json.loads)

            return df
        except sqlite3.OperationalError as e:
            print(f"Error loading data from table {table_name}: {e}")
            return pd.DataFrame()


    def generate_langchain_analysis(self,df, top_keywords, total_score, total_comments):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except KeyError:
            raise ValueError("GEMINI_API_KEY not found in .streamlit/secrets.toml. Please set it.")

        sentiment_counts = df['sentiments'].value_counts(normalize=True) * 100

        analysis_data = f"""
        Overall Engagement Metrics:
        - Total Upvotes (Score): {total_score:,}
        - Total Comments: {total_comments:,}
    
        Sentiment Breakdown (Percentage of Posts):
        - Positive: {sentiment_counts.get('positive', 0):.2f}%
        - Negative: {sentiment_counts.get('negative', 0):.2f}%
        - Neutral: {sentiment_counts.get('neutral', 0):.2f}%
    
        Top 20 Keywords and Frequencies:
        {top_keywords[:20]}
        """

        template = ChatPromptTemplate.from_messages([
            ("system",
             "You are a highly skilled *Social Media Business Analyst*. Your response must be professional, insightful, and clearly structured into two sections: 'Executive Summary' and 'Actionable Recommendations'."),
            ("human",
             f"""
             Analyze the social media data provided below and generate a detailed report.
    
             *DATA FOR ANALYSIS:*
             ---
             {analysis_data}
             ---
    
             Provide a concise summary of the sentiment, topics, and engagement. Then, provide three specific, actionable recommendations for the company's strategy based on the negative sentiment and popular keywords.
             """)
        ])

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2,google_api_key=api_key)
        chain = template | llm
        response = chain.invoke({})

        return response.content

    def clean_data_sentiment(self,text=''):
        text = str(text).lower()
        text = re.sub(r'https?//s+','',text)
        text = re.sub(r'u/\w+','',text)
        text = re.sub(r'[^a-z\s]',"",text)
        text = re.sub(r'\s+'," ",text)
        return text

    def get_clean_keywords(self,text):
        text = str(text).lower()
        text = re.sub(r'https?//s+','',text)
        text = re.sub(r'u/\w+','',text)
        text = re.sub(r'[^a-z\s]','',text)
        words = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        return filtered_words


    def clean_comments(self,comment_list_json):
        try:
            comments = json.loads(comment_list_json)
            cleaned_texts = []
            for comment in comments:
                text = comment.get('comment_text', '').lower()

                # Ignore repeated Reddit reminders or bot messages
                if "this is a friendly reminder" in text:
                    continue

                cleaned = self.clean_data_sentiment(text)
                if cleaned:
                    cleaned_texts.append(cleaned)
            return " ".join(cleaned_texts)
        except Exception as e:
            return ""

    # Apply these cleaning functions on DataFrame columns
    def clean_dataframe(self,df):
        df['post_title_clean'] = df['post_title'].apply(self.clean_data_sentiment)
        df['post_text_clean'] = df['post_text'].apply(self.clean_data_sentiment)
        df['comments_clean'] = df['comments'].apply(self.clean_comments)
        return df

    def popular_key(self,df):
        all_words= []
        text_column= ['post_title','post_text','comments']

        for col in text_column:
            word_lists = df[col].apply(self.get_clean_keywords)
            all_words.extend([word for sublist in word_lists for word in sublist])

            word_count = Counter(all_words)
            most_common = word_count.most_common(20)
            return most_common

    def apply_sentiment(self,df):
        df['post_title_polarity'] = df['post_title_clean'].apply(lambda text: TextBlob(text).sentiment.polarity)
        df['post_text_polarity'] = df['post_text_clean'].apply(lambda text: TextBlob(text).sentiment.polarity)
        df['comments_polarity'] = df['comments_clean'].apply(lambda text: TextBlob(text).sentiment.polarity)
        return df
    def category_sent(self,score):
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        else:
            return 'neutral'

