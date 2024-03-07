import newsapi
import requests
import pandas as pd
import random
import csv
from datetime import datetime, timedelta
import os

api_key = os.getenv('NEWSAPI_API_KEY')

def get_news_headlines(domains='cnn.com, foxnews.com, dailymail.co.uk, theguardian.com, reuters.com, finance.yahoo.com, forbes.com, bbc.co.uk, bbc.com, nytimes.com, news.google.com', 
                      language='en', 
                      from_param=(datetime.now()- timedelta(hours = 24)).strftime('%Y-%m-%d'+'T00:00:00'), 
                      to_param=datetime.now().strftime('%Y-%m-%d'+'T00:00:00'),
                      sort_by='popularity',
                      page_size=100,
                      api_key=api_key
                      ):
    api_query = f'https://newsapi.org/v2/everything?domains={domains}&language={language}&from={from_param}&to={to_param}&sortBy={sort_by}&pageSize={page_size}&apiKey={api_key}'

    response = requests.get(api_query)
    
    if response.status_code == 200:
        data_return = response.json()
        # Reverse from least popular to most popular among the {page_size} articles
        data_return['articles'] = list(reversed(data_return['articles']))

        total_results = data_return.get('totalResults', 0)
        print(f"Total results: {total_results}")
        
        # Select four random articles
        four_random_articles = random.sample(data_return['articles'], 4)

        return four_random_articles

game_articles = get_news_headlines()
#print(game_articles)
csv_filename = 'main.csv'


def write_game_articles_to_csv(game_articles, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        column_names = ['group_id', 'title', 'published_at', 'url_to_image', 'url', 'keywords']
        writer = csv.DictWriter(csvfile, fieldnames=column_names)

        writer.writeheader()

        group_ids = [1, 2, 3, 4]
        for i, article in enumerate(game_articles):
            writer.writerow({
                'group_id': group_ids[i],
                'title': article['title'],
                'published_at': article['publishedAt'],
                'url_to_image': article.get('urlToImage'),
                'url': article['url']
            })
    
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)

write_game_articles_to_csv(game_articles, csv_filename)
