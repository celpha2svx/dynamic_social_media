import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from analyze_data import Analyser
from scrape_data import Executor
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT')

fetcher = Executor(client_id=client_id,client_secret=client_secret,user_agent=user_agent)
POST_LIMIT = 100
run = Analyser()

st.set_page_config(
    page_title="Dynamic Social Media Analyzer",
    layout="wide",
    page_icon="🔎"
)

st.sidebar.title("About This Analyzer")
st.sidebar.markdown(
    """
    This dynamic dashboard provides instant social media analysis based on *live Reddit data*. 

    It scrapes the top posts for a topic, performs sentiment analysis and keyword extraction, and displays the results in a clear, actionable format.

    ### *How to Use:*
    1. Enter a company or topic (subreddit name) in the input field.
    2. Click 'Generate Dashboard' to run the full pipeline.
    
    """
)

st.image("solvip.jpg", width=500)

st.title("Solvix Sentiments 📈")
st.markdown("### Enter a topic to generate a full analysis dashboard.")

st.header("Analysis Settings")

subreddit_input = st.text_input(
    "Enter Company/Topic Name (Subreddit)",
    value="smallbusiness"
)

st.info(f"Analysis will fetch the top {POST_LIMIT} posts.")
run_analysis = st.button("Generate Dashboard")

if run_analysis:
    cleaned_input = subreddit_input.strip().replace(' ', '')
    st.info(f"Running analysis for r/{cleaned_input}... This may take a moment.")

    with st.spinner('Step 1/4: Fetching data from Reddit...'):
        df_fetched = fetcher.reddit_data(cleaned_input, total_limit=POST_LIMIT)

        if df_fetched.empty:
            st.error("Could not fetch data. Check the subreddit name or API connection.")
            st.stop()

        dynamic_table_name = fetcher.store_reddit_db(df_fetched, base_table_name=cleaned_input)

        if dynamic_table_name is None:
            st.error("Failed to store data in the database.")
            st.stop()

    with st.spinner('Step 2/4: Performing sentiment and keyword analysis...'):
        df = run.load_data_from_db(dynamic_table_name)


    # Getting sentiment analysis
    df =run.clean_dataframe(df)
    df = run.apply_sentiment(df)
    df['overall_sentiments'] = df[['post_title_polarity','post_text_polarity','comments_polarity']].mean(axis=1)
    df['sentiments'] = df['overall_sentiments'].apply(run.category_sent)
    sentiment_count = df['sentiments'].value_counts()
    # The top keywords
    top_keywords = run.popular_key(df)

    # Total engagement and average engagements
    total_score = df['post_score'].sum()
    total_comments = df['num_comments'].sum()
    avg_score = df['post_score'].mean()
    avg_comments = df['num_comments'].mean()

    # Generating Ai report
    ai_report = ""
    with st.spinner('Step 3/4: Generating AI Analyst Report...'):
        try:
            ai_report = run.generate_langchain_analysis(df, top_keywords, total_score, total_comments)
        except Exception as e:
            st.error(f"AI Analysis Failed. Check API Key/Connection: {e}")
            ai_report = "Error: Could not generate AI report."

    tab1, tab2, tab3 = st.tabs(["Dashboard Visuals 📊", "AI Analyst Report 🤖", "Raw Data 🗃"])

    with tab1:
        # Display background
        st.title('Social Media Dashboard')
        st.header('Executive summary')

        col1,col2,col3,col4= st.columns(4)

        with col1:
            st.metric(label="Total upvotes",value=f"{total_score}")
        with col2:
            st.metric(label="Total comments",value=f"{total_comments}")
        with col3:
            st.metric(label="Average upvotes",value=f"{avg_score:.2f}")
        with col4:
            st.metric(label="Average comments",value=f"{avg_comments:.2f}")


        st.markdown("---")
        st.header("Thematic Insights")
        fig = px.pie(
                 values= sentiment_count.values,
                 names= sentiment_count.index,
                 title= "Sentiment Breakdown"
        )
        st.plotly_chart(fig)

        st.markdown("---")
        word_freq_dict = dict(top_keywords)
        wordcloud = WordCloud(width=800,height=400,background_color='white').generate_from_frequencies(word_freq_dict)
        st.header("Top 20 Keywords")
        fig,ax =plt.subplots()
        ax.imshow(wordcloud,interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    with tab2:
            st.subheader("Automated Analysis and Strategy")
            st.markdown(ai_report)

    with tab3:
        st.header("Raw Data Table")
        st.dataframe(df[['post_title', 'overall_sentiments', 'sentiments', 'post_score', 'num_comments']].head(200))