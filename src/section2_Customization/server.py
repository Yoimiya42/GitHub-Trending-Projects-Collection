"""
To run this program, please install Flask and requests first:

Command:
`pip install flask flask-cors requests`

then run the server.py file:
`python server.py`

you will see the following output:
```
* Serving Flask app 'server' (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
open another terminal and type:

`python -m http.server 8001` 

and open the browser to access `http://localhost:8001/index.html`

"""

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RESULTS = 20  # Maximum number of results to return

def fetch_repositories(query):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        response_dict = r.json()

        repos = []
        for item in response_dict.get('items', [])[:RESULTS]:
            repo = {
                'name': item['name'],
                'stars': item['stargazers_count'],
                'forks': item['forks_count'],
                'url': item['html_url'],
                'description': item['description'] or 'No description',
                'owner': item['owner']['login'],
                'language': item['language'] or 'Unknown'
            }
            repos.append(repo)
        return repos
    except requests.exceptions.RequestException as e:
        return [{'error': str(e)}]

# 1. Programming Beginners/Entry-level Learners
@app.route('/api/search_beginner', methods=['GET'])
def search_beginner_repositories():
    # Hard-coded conditions:
    # - Keywords "tutorial" or "guide" in README or description
    # - At least 100 stars
    # - Has wiki
    # - More than 50 commits (using pushed date as proxy for activity)
    # - More than 10 open issues
    query = ("tutorial OR guide OR learn OR programming OR code OR beginner in:readme in:description "
             "stars:>100 "
             #"has_wiki:true "
             "pushed:>2022-01-01 "
             "open_issues:>10"
             )
    repos = fetch_repositories(query)
    return jsonify(repos)

# 2. Intermediate-level Students
@app.route('/api/search_intermediate', methods=['GET'])
def search_intermediate_repositories():
    # Hard-coded conditions:
    # - Keywords "good first issue" or "help wanted"
    # - At least 500 stars
    # - More than 20 open issues
    # - Active in last year (pushed date)
    # - At least 100 commits (using pushed date as proxy)
    query = ("good first issue OR help wanted OR programming OR code in:readme in:description "
             "stars:>500 "
             "has_wiki:true "
             "pushed:>2022-01-01 "
             "open_issues:>20"
             )
    repos = fetch_repositories(query)
    return jsonify(repos)

# 3. Software and Gaming Enthusiasts
@app.route('/api/search_gaming', methods=['GET'])
def search_gaming_repositories():
    # Hard-coded conditions:
    # - Keywords "game" or "mod" in README or description
    # - At least 200 stars
    # - More than 10 open issues
    # - Active in last 6 months (pushed date)
    # - Topics include "game" or "plugin"
    #query = "game mod in:readme in:description stars:>200 open_issues:>10 pushed:>2024-01-01 topic:game topic:plugin"
    query = ("game AND gaming in:readme in:description "
             "stars:>200 "
             "pushed:>2024-09-01 "
             "open_issues:>10"
             )
    repos = fetch_repositories(query)
    return jsonify(repos)

if __name__ == '__main__':
    app.run(debug=True, port=5001)