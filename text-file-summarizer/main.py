import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from textblob import TextBlob
from gensim.summarization.summarizer import summarize
from gensim.parsing.preprocessing import preprocess_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import pandas as pd

def scrape_news(url, keyword):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    relevant_articles = []
    for article in articles:
        if keyword.lower() in article.text.lower():
            relevant_articles.append(article)
    return relevant_articles

def analyze_articles(articles):
    summaries = []
    sentiments = []
    for article in articles:
        text = article.get_text()
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 5)
        summaries.append(" ".join([str(sentence) for sentence in summary]))
        sentiment = TextBlob(text).sentiment.polarity
        sentiments.append(sentiment)
    
    preprocessed_texts = [" ".join(preprocess_string(text)) for text in summaries]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(preprocessed_texts)
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(vectors)
    clusters = kmeans.labels_.tolist()

    generate_wordcloud(summaries)
    generate_sentiment_distribution(sentiments)
    generate_topic_heatmap(clusters, summaries)
    generate_report(summaries, sentiments, clusters)

def generate_wordcloud(summaries):
    text = " ".join(summaries)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Summarized Articles')
    plt.show()

def generate_sentiment_distribution(sentiments):
    plt.figure(figsize=(10, 5))
    plt.hist(sentiments, bins=20, color='blue', edgecolor='black')
    plt.title('Sentiment Distribution of Articles')
    plt.xlabel('Sentiment Polarity')
    plt.ylabel('Frequency')
    plt.show()

def generate_topic_heatmap(clusters, summaries):
    df = pd.DataFrame({'Cluster': clusters, 'Summary': summaries})
    cluster_counts = df['Cluster'].value_counts().sort_index()
    heatmap_data = np.array(cluster_counts).reshape(1, -1)
    plt.figure(figsize=(10, 1))
    plt.imshow(heatmap_data, cmap='viridis', aspect='auto')
    plt.colorbar()
    plt.title('Topic Heatmap')
    plt.yticks([])
    plt.xticks(ticks=np.arange(len(cluster_counts)), labels=[f'Cluster {i}' for i in range(len(cluster_counts))])
    plt.show()

def generate_report(summaries, sentiments, clusters):
    report = pd.DataFrame({
        'Summary': summaries,
        'Sentiment': sentiments,
        'Cluster': clusters
    })
    print(report)

if __name__ == "__main__":
    keyword = "climate change"
    url = "https://www.nytimes.com/section/world/environment"
    articles = scrape_news(url, keyword)
    analyze_articles(articles)
