"""
Please install the following libraries before running the script:
`pip install requests matplotlib`

then run the script:
`python LanguagesPieChart.py`
"""

import requests
import matplotlib.pyplot as plt
from collections import Counter
import time

def fetch_language_distribution(max_repos=1000, min_stars=100):
    """
    Fetch top repositories by stars from GitHub API and count their languages
    """
    languages = []
    page = 1
    per_page = 100  # GitHub API max items per page
    repos_processed = 0
    
    base_url = "https://api.github.com/search/repositories"
    
    print(f"Fetching top {max_repos} repositories with at least {min_stars} stars...")
    
    while repos_processed < max_repos:
        # Construct query URL for repositories sorted by stars
        url = f"{base_url}?q=stars:>{min_stars}&sort=stars&order=desc&page={page}&per_page={per_page}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        try:
            r = requests.get(url, headers=headers)
            
            # Check for rate limiting
            if r.status_code == 403 and 'X-RateLimit-Remaining' in r.headers and int(r.headers['X-RateLimit-Remaining']) == 0:
                reset_time = int(r.headers['X-RateLimit-Reset'])
                sleep_time = max(reset_time - time.time(), 0) + 1
                print(f"Rate limit exceeded. Waiting for {sleep_time:.0f} seconds...")
                time.sleep(sleep_time)
                continue
                
            if r.status_code != 200:
                print(f"API request failed, status code: {r.status_code}")
                break
            
            response_dict = r.json()
            if 'items' not in response_dict or not response_dict['items']:
                print("No more repositories available")
                break
            
            repos_dicts = response_dict['items']
            for repo in repos_dicts:
                language = repo.get('language')
                if language:  # Some repos might not have a language specified
                    languages.append(language)
                repos_processed += 1
                
                # Stop if we've processed enough repos
                if repos_processed >= max_repos:
                    break
            
            print(f"Processed {repos_processed} repositories, current page: {page}")
            page += 1
            
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    return languages

def generate_pie_chart(languages, top_n=10):
    """
    Generate a pie chart of the most common programming languages
    """
    # Count language frequencies
    language_counts = Counter(languages)
    
    # Get the top N languages
    top_languages = language_counts.most_common(top_n)
    
    # Add an "Other" category for the rest
    other_count = sum(count for lang, count in language_counts.most_common()[top_n:])
    if other_count > 0:
        top_languages.append(("Other", other_count))
    
    # Extract labels and values for the pie chart
    labels = [lang for lang, count in top_languages]
    values = [count for lang, count in top_languages]
    
    # Calculate percentages for labels
    total = sum(values)
    percentages = [(count / total) * 100 for count in values]
    
    # Create labels with percentages
    labels_with_pct = [f"{label} ({pct:.1f}%)" for label, pct in zip(labels, percentages)]
    
    # Define colors for the pie chart
    colors = plt.cm.tab20.colors[:len(top_languages)]
    
    # Create the pie chart
    plt.figure(figsize=(12, 8))
    plt.pie(values, labels=labels_with_pct, colors=colors, autopct='', 
            shadow=False, startangle=140, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    plt.title('Programming Languages Distribution in Top GitHub Repositories', fontsize=16)
    
    # Add a legend
    plt.legend(labels, loc="best", bbox_to_anchor=(1, 0.5))
    
    # Save the chart to a file
    plt.savefig("github_languages_pie_chart.png", bbox_inches='tight')
    
    # Display the chart
    plt.show()
    
    # Print the data
    print("\nLanguage Distribution:")
    print("-" * 30)
    for lang, count in top_languages:
        percentage = (count / total) * 100
        print(f"{lang}: {count} repositories ({percentage:.1f}%)")

if __name__ == "__main__":
    print("Fetching data from GitHub API...")
    languages = fetch_language_distribution(max_repos=1000, min_stars=100)
    
    if languages:
        print(f"\nSuccessfully fetched language data for {len(languages)} repositories")
        generate_pie_chart(languages)
    else:
        print("No languages fetched, unable to generate pie chart.")