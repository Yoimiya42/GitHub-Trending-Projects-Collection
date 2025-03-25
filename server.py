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

`python -m http.server 8000` 

and open the browser to access `http://localhost:8000/index.html`

"""



from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/search', methods=['GET'])
def search_repositories():
    language = request.args.get('language', 'ALL')
    topic = request.args.get('topic', '')
    stars = request.args.get('stars', '0')
    forks = request.args.get('forks', '0')
    org = request.args.get('org', '')
    start_date = request.args.get('created:>', '')
    end_date = request.args.get('created:<', '')

    query = []
    if language != 'ALL':
        query.append(f"language:{language}")
    if topic:
        query.append(topic)
    if stars:
        query.append(f"stars:>{stars}")
    if forks:
        query.append(f"forks:>{forks}")
    if org:
        query.append(f"org:{org}")
    if start_date:
        query.append(f"created:>{start_date}")
    if end_date:
        query.append(f"created:<{end_date}")

    url = "https://api.github.com/search/repositories"
    url += f"?q={' '.join(query)}&sort=stars&order=desc"
    print(f"GitHub API URL: {url}")

    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        response_dict = r.json()
        
        repos = []
        min_stars = int(stars) if stars else 0
        min_forks = int(forks) if forks else 0
        
        for item in response_dict.get('items', [])[:10]:
            stars_count = item['stargazers_count']
            forks_count = item['forks_count']
            
            if stars_count <= min_stars or forks_count <= min_forks:
                print(f"Skipping {item['name']}: stars={stars_count}, forks={forks_count}")
                continue
                
            repo = {
                'name': item['name'],
                'stars': stars_count,
                'forks': forks_count,
                'url': item['html_url'],
                'description': item['description'] or 'No description',
                'owner': item['owner']['login']
            }
            repos.append(repo)
        
        print(f"Returning {len(repos)} repositories")
        print()
        return jsonify(repos)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)