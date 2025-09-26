​📊 Dynamic Social Media Analyzer Dashboard

​This project is a powerful, interactive dashboard built using Streamlit that performs real-time sentiment and trend analysis on a user-specified Reddit community (subreddit). It fetches data using PRAW, performs advanced analysis using Gemini 2.5 Flash via LangChain, and stores historical results using Pandas and SQLite.
​

✨ Key Features

​Dynamic Data Fetching:  Scrapes the top posts from any user-defined subreddit (e.g., r/small business, r/technology).
​Agentic AI Analysis: Uses the Gemini 2.5 Flash model to analyze fetched post titles and comments, generating a structured report with a Score, Key Trends, and Actionable Recommendations.
​Historical Data Storage: Stores all fetched posts in a local SQLite database, creating a new, timestamped table for each run.
​Interactive Visualization: Displays key metrics, post scores, and a keyword cloud using Streamlit components.

​⚙ How to Run the App Locally  
​Follow these steps to set up and run the application on your local machine.
​
1. Prerequisites
​You must have Python 3.9+ installed. This project relies on a virtual environment for dependency isolation.

2. Clone the Repository

       git cloneYOUR_GITHUB_REPO_URL
       cd social_media_dashboard # Change to your project directory
3. Install Dependencies
​You should have a requirements.txt file (created with pip freeze > requirements.txt). Install all required packages:

         pip install -r requirements.txt
4. Set Up API Keys (Crucial Step)
​This application requires API keys for both Google Gemini (AI Analysis) and Reddit (Data Scraping).

   A.Get your Gemini API Key from Google AI Studio.

      i. Create a folder named .streamlit in the root of your project directory.

      ii. Inside the .streamlit folder, create a file named secrets.toml.

      iii. Add your key to the file using the following format: 

               #.streamlit/secrets.toml 
               GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_KEY_GOES_HERE"
5. Launch the Dashboard
​Run the main Streamlit script from your project directory:

         Cmd:streamlit run dashboard.py 
The app will open automatically in your web browser.

​🛠Project Structure

​The project is divided into logical components:

            File/Folder                purpose
           
            dashboard.py              The main Streamlit file.
                                      Handles the UI,user input,
                                      and orchestrates calls to the 
                                      analysis pipeline.

            scrape_data.py            Contains the
                                      Executor Class  using PRAW,
                                      including logic to clean user input 
                                      and scrape posts/comments.

            analyze_data.py           Contains the 
                                      handling prompt engineering,
                                      the LangChain pipeline, and databaseI/O.

            .streamlit/secrets.toml   DO NOT COMMIT THIS FILE
                                      Securely stores API keys and credentials.

            requirements.txt          Lists all necessary Python 
                                      dependencies (Streamlit, PRAW,
                                       LangChain,pandas,etc.).

🤝 Next Steps & Future Enhancements

1. Add a feature to compare the current analysis with previous database runs.

2. Integrate visual indicators (e.g., color-coded emojis) based on the AI's "Sentiment Score."

3. Implement data filtering options by date or score within the dashboard.

4. create more pipelines for data extractions like(Twitter,website news base, facebook etc.)

This project was completed as part of an advanced Python/AI and Datascience development training curriculum.