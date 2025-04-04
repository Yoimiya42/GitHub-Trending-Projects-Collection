
"""
Please install the following libraries before running the script:
`pip install requests wordcloud matplotlib`

then run the script:
`python WordCloud.py`
"""


import requests
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Fetch top repositories by stars from GitHub API
def fetch_top_repos(max_repos=1000, min_stars=5000):
    all_topics = []
    page = 1
    per_page = 100  # GitHub API max items per page
    
    base_url = "https://api.github.com/search/repositories"
    
    while len(all_topics) < max_repos:
        # Construct query URL for repositories sorted by stars
        url = f"{base_url}?q=stars:>{min_stars}&sort=stars&order=desc&page={page}&per_page={per_page}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        try:
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                print(f"API request failed, status code: {r.status_code}")
                break
            
            response_dict = r.json()
            if 'items' not in response_dict or not response_dict['items']:
                print("No more repositories available")
                break
            
            repos_dicts = response_dict['items']
            for repo in repos_dicts:
                topics = repo.get('topics', [])  # Get topics for each repo
                all_topics.extend(topics)
            
            print(f"Fetched {len(all_topics)} topics, current page: {page}")
            page += 1
            
            # Stop if we’ve collected enough topics
            if len(all_topics) >= max_repos:
                break
                
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    # Limit to max_repos topics
    return all_topics[:max_repos]

# Generate word cloud from topics
def generate_wordcloud(topics):
    # Count topic frequencies
    topic_counts = Counter(topics)
    
    # Create word cloud
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        min_font_size=10,
        max_font_size=150,
        colormap="plasma"  # Color scheme
    ).generate_from_frequencies(topic_counts)
    
    # Display word cloud
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Most Popular Topics in Top GitHub Repositories", fontsize=20, pad=20)
    plt.show()
    
    # Save word cloud to file
    wordcloud.to_file("github_topics_wordcloud.png")

# Main execution
if __name__ == "__main__":
    print("Fetching data from GitHub API...")
    topics = fetch_top_repos(max_repos=1000, min_stars=5000)
    
    if topics:
        print(f"Successfully fetched {len(topics)} topics, generating word cloud...")
        generate_wordcloud(topics)
    else:
        print("No topics fetched, unable to generate word cloud.")