import pandas as pd
import sqlite3

conn = sqlite3.connect('../db.sqlite3')
users = pd.read_csv('../static/data/users.csv')
users.to_sql('users', conn, if_exists='append', index=False)

category = pd.read_csv('../static/data/category.csv')
category.to_sql('category', conn, if_exists='append', index=False)

genre = pd.read_csv('../static/data/genre.csv')
genre.to_sql('genre', conn, if_exists='append', index=False)

comments = pd.read_csv('../static/data/comments.csv')
comments.to_sql('comments', conn, if_exists='append', index=False)

genre_title = pd.read_csv('../static/data/genre_title.csv')
genre_title.to_sql('genre_title', conn, if_exists='append', index=False)

review = pd.read_csv('../static/data/review.csv')
review.to_sql('review', conn, if_exists='append', index=False)

titles = pd.read_csv('../static/data/titles.csv')
titles.to_sql('titles', conn, if_exists='append', index=False)
