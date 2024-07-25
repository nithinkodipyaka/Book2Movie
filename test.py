from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load and process data
movies = pd.read_csv("C:\Akila\VIT\Summer_Semester\CSE4077 - Recommender Systems\Project\Dataset\movies\movies_metadata.csv")
movies['genres'] = movies['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
keywords = pd.read_csv('C:\Akila\VIT\Summer_Semester\CSE4077 - Recommender Systems\Project\Dataset\movies\keywords.csv')
movies['id'] = movies['id'].apply(lambda x: int(x) if str(x).isdigit() else np.nan)
movies = movies[movies['id'].notnull()]
movies['id'] = movies['id'].astype('int')
keywords['id'] = keywords['id'].astype('int')
movies = movies.merge(keywords, on='id')
movies["keywords"] = movies["keywords"].apply(literal_eval)
movies['keywords'] = movies['keywords'].apply(lambda x: [i['name'] for i in x][:10] if isinstance(x, list) else [])
movies['genres'] = movies['genres'].apply(lambda x: x[:10])
movies['overview'] = movies['overview'].fillna('')
movies['title'] = movies['title'].fillna('')
movies['soup'] = movies.apply(lambda x: x["title"] + " " + " ".join(x['genres']) + " "+x['overview']+" "+" ".join(x['keywords']), axis=1)

books = pd.read_csv("top2k_book_descriptions.csv", index_col=0)
books['tag_name'] = books['tag_name'].apply(lambda x: literal_eval(x) if literal_eval(x) else np.nan)
books = books[books['description'].notnull() | books['tag_name'].notnull()].fillna('')
books["soup"] = books.apply(lambda x: x["original_title"]+" "+x["description"]+" "+" ".join(x['tag_name'])+" "+x["authors"], axis=1)

soups = pd.concat([books['soup'], movies['soup']], ignore_index=True)
count = CountVectorizer(stop_words="english")
count.fit(soups)
books_matrix = count.transform(books['soup'])
movies_matrix = count.transform(movies['soup'])
cosine_sim = cosine_similarity(books_matrix, movies_matrix)
books = books.reset_index()
indices = pd.Series(books.index, index=books['original_title'].apply(lambda x: x.lower() if x is not np.nan else "")).drop_duplicates()

def content_recommender(title):
    idx = indices[title.lower()]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:10]
    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices]

