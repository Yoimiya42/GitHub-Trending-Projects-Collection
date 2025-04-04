from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from datetime import datetime, timedelta
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
CORS(app)

logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/search/repositories"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",

    #needs token, otherwise reaches API rate limit
}

#try again if it reaches the rate limit
session = requests.Session()
retry_strategy = Retry(total=3, backoff_factor=2, status_forcelist=[403, 429])
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

def get_date_days_ago(days):
    date = datetime.now() - timedelta(days=days)
    return date.strftime("%Y-%m-%d")

def fetch_github(url):
    response = session.get(url, headers=HEADERS)
    #sleep to prevent rate limit issues
    time.sleep(2)  
    return response

@app.route('/api/trending_repos', methods=['GET'])
def get_trending_repos():
    date = get_date_days_ago(7)
    url = f"{GITHUB_API_URL}?q=created:>{date}&sort=stars&order=desc"
    response = fetch_github(url)

    if response.status_code != 200:
        logger.error(f"Failed to fetch trending repos: {response.status_code} - {response.text}")
        return jsonify({"error": "Failed to fetch trending repositories", "status": response.status_code}), 500
    
    data = response.json()
    repos = data.get('items', [])[:10]
    result = [{"name": repo["name"], "stars": repo["stargazers_count"], "forks": repo["forks_count"], 
               "language": repo["language"], "url": repo["html_url"], "owner": repo["owner"]["login"]} for repo in repos]
    
    return jsonify(result)

@app.route('/api/most_forked', methods=['GET'])
def get_most_forked():
    date = get_date_days_ago(30)
    url = f"{GITHUB_API_URL}?q=created:>{date}&sort=forks&order=desc"
    response = fetch_github(url)

    if response.status_code != 200:
        logger.error(f"Failed to fetch forked repos: {response.status_code} - {response.text}")
        return jsonify({"error": "Failed to fetch forked repositories", "status": response.status_code}), 500
    
    data = response.json()
    repos = data.get('items', [])[:10]
    result = [{"name": repo["name"], "forks": repo["forks_count"], "url": repo["html_url"]} for repo in repos]

    return jsonify(result)

@app.route('/api/language_trends', methods=['GET'])
def get_language_trends():
    #can add or remove languages
    languages = ["Python", "JavaScript", "Java", "C++"]
    years = [2020, 2021, 2022, 2023, 2024]
    trends = {lang: {} for lang in languages}

    for year in years:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31" if year < 2025 else get_date_days_ago(0)
        for lang in languages:
            url = f"{GITHUB_API_URL}?q=language:{lang}+created:{start_date}..{end_date}&sort=stars&order=desc"
            response = fetch_github(url)

            if response.status_code == 200:
                trends[lang][year] = response.json().get('total_count', 0)
            else:
                logger.error(f"Failed to fetch trends for {lang} in {year}: {response.status_code} - {response.text}")
                trends[lang][year] = 0

    return jsonify(trends)

@app.route('/api/popular_by_language', methods=['GET'])
def get_popular_by_language():
    #similarly, can add or remove languages
    languages = ["Python", "JavaScript", "Java", "C++"]
    result = {}
    date = get_date_days_ago(90)
    for lang in languages:
        url = f"{GITHUB_API_URL}?q=language:{lang}+created:>{date}&sort=stars&order=desc"
        response = fetch_github(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch popular repos for {lang}: {response.status_code} - {response.text}")
            result[lang] = []
            continue

        data = response.json()
        repos = data.get('items', [])[:3]
        result[lang] = [{"name": repo["name"], "stars": repo["stargazers_count"], 
                         "url": repo["html_url"], "owner": repo["owner"]["login"]} for repo in repos]
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)