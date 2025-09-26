import praw
import pandas as pd
import sqlite3
import json
import time


class Executor:
    def __init__(self, client_id,client_secret,user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )


    def reddit_data(self,subreddit_input, total_limit=500):
        """
                Scrapes data from reddit using praw then paginate and store in dataframe
                """
        posts_data = []
        cleaned_subreddit_name = subreddit_input.strip().replace(' ', '')

        try:
            subreddit =self.reddit.subreddit(cleaned_subreddit_name)
            submissions = subreddit.hot(limit=total_limit)

            for submission in submissions:
                submission.comments.replace_more(limit=0)
                comments_data = []

                for comment in submission.comments.list():
                    if hasattr(comment, 'body') and comment.body:
                        comments_data.append({
                            "comment_text": comment.body,
                            "comment_score": comment.score,
                            "comment_created_utc": comment.created_utc
                        })

                post_info = {
                    "id": submission.id,
                    "post_title": submission.title,
                    "post_text": submission.selftext,
                    "post_score": submission.score,
                    "num_comments": submission.num_comments,
                    "post_created_utc": submission.created_utc,
                    "comments": comments_data
                }
                posts_data.append(post_info)

            df = pd.DataFrame(posts_data)
            print(f"Successfully fetched {len(df)} posts from r/{cleaned_subreddit_name}")
            return df

        except Exception as e:
            print(f"PRAW Error: Could not fetch r/{cleaned_subreddit_name}. {e}")
            return pd.DataFrame()


    def store_reddit_db(self,df, db_name='social_media_data.db', base_table_name='reddit_post'):
        """
        Stores DataFrame data into a uniquely named table, handling JSON serialization.
        Returns the name of the newly created table.
        """
        if df.empty:
            print("DataFrame is empty, nothing to store")
            return None

        df_copy = df.copy()
        df_copy['comments'] = df_copy['comments'].apply(json.dumps)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        dynamic_table_name = f"{base_table_name}_{timestamp}"

        try:
            with sqlite3.connect(db_name, timeout=20.0) as conn:
                conn.execute("PRAGMA journal_mode=WAL")

                df_copy.to_sql(dynamic_table_name, conn, if_exists='replace', index=False)

                print(f"Successfully stored {len(df_copy)} posts in table: {dynamic_table_name}")
                return dynamic_table_name

        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            return None