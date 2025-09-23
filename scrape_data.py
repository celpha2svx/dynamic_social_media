import praw
import pandas as pd
import sqlite3
import json
import time

reddit = praw.Reddit(
    client_id="rlYqmsdFxQZEFuks80TNew",
    client_secret="MUALBS4NIRWWbmveY1tKqHPtdS-UIw",
    user_agent="SolvixT"
)


def fetch_reddit_data(subreddit_name, total_limit=500, batch_size=100, delay_secs=30):
    posts_data = []
    subreddit = reddit.subreddit(subreddit_name)
    last_fullname = None

    while len(posts_data) < total_limit:
        remaining = total_limit - len(posts_data)
        limit = min(batch_size, remaining)

        submissions = subreddit.hot(limit=None)
        batch = []
        count = 0

        for submission in submissions:
            if last_fullname and submission.fullname <= last_fullname:
                continue

            submission.comments.replace_more(limit=0)
            comments_data = []
            for comment in submission.comments.list():
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
            batch.append(post_info)
            count += 1

            if count == 1:
                last_fullname = submission.fullname

            if count >= limit:
                break

        if not batch:
            print("No new posts fetched, ending pagination.")
            break

        posts_data.extend(batch)

        if len(posts_data) < total_limit:
            print(f"Fetched {len(posts_data)} posts so far, sleeping for {delay_secs} seconds...")
            time.sleep(delay_secs)

    df = pd.DataFrame(posts_data)
    return df


def store_reddit_data_to_db(df, db_name='social_media_data.db', table_name='reddit_post'):
    if df.empty:
        print("DataFrame is empty, nothing to store")
        return False

    df_copy = df.copy()
    df_copy['comments'] = df_copy['comments'].apply(json.dumps)

    try:
        with sqlite3.connect(db_name, timeout=20.0) as conn:
            conn.execute("PRAGMA journal_mode=WAL")

            # Create table with unique 'id'
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id TEXT PRIMARY KEY,
                    post_title TEXT,
                    post_text TEXT,
                    post_score INTEGER,
                    num_comments INTEGER,
                    post_created_utc REAL,
                    comments TEXT
                )
            ''')

            # Get existing post IDs
            try:
                existing_ids = pd.read_sql(f"SELECT id FROM {table_name}", conn)['id'].tolist()
            except:
                existing_ids = []

            # Filter out duplicates
            new_posts = df_copy[~df_copy['id'].isin(existing_ids)]

            if len(new_posts) > 0:
                # Insert new posts row by row to respect primary key uniqueness
                cursor = conn.cursor()
                for _, row in new_posts.iterrows():
                    cursor.execute(f'''
                        INSERT OR IGNORE INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['id'],
                        row['post_title'],
                        row['post_text'],
                        row['post_score'],
                        row['num_comments'],
                        row['post_created_utc'],
                        row['comments']
                    ))
                conn.commit()
                print(f"Added {len(new_posts)} new posts (skipped {len(df_copy) - len(new_posts)} duplicates)")
            else:
                print("All posts were duplicates")
            return True
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return False


if __name__ == "__main__":
    subreddit = "smallbusiness"
    df = fetch_reddit_data(subreddit, total_limit=500,batch_size=100,delay_secs=30)
    print(df.head())
    success = store_reddit_data_to_db(df)