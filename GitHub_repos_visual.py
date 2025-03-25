import requests
import plotly.express as px

############### CHANGE THE LANGUAGE AND STARS HERE ###################
language = "Python"
stars = 5000
created = "2025-01-01"
######################################################################

##################### I M P L E M E N T A T I O N ####################
url = "https://api.github.com/search/repositories"
url += f"?q=language:{language}+sort:stars+stars:>{stars} + created:>{created}"

headers = {"headers" : "application/vnd.github.v3+json"}
r = requests.get(url, headers = headers)
print(f"Status Code: {r.status_code}")
response_dict = r.json()

repos_dicts = response_dict['items']

repos_links = []
repos_stars = []
repos_hover_texts = []

for repos_dict in repos_dicts:
    repos_name = repos_dict['name']
    repos_url  = repos_dict['html_url']
    repos_link = f"<a href='{repos_url}'>{repos_name}</a>"
    repos_links.append(repos_link)
    
    repos_stars.append(repos_dict['stargazers_count'])

    repos_description = repos_dict['description']
    repos_owner = repos_dict['owner']['login']
    repos_hover_text = f"{repos_owner}<br />{repos_description}"
    repos_hover_texts.append(repos_hover_text)

############################  Visualization ###########################
title = f"Most Starred {language} Projects in GitHub"
labels = {'x' : "Repositories", 'y' : "Stars"}
fig = px.bar(x = repos_links, y = repos_stars, title = title, labels = labels, hover_name = repos_hover_texts)


fig.update_layout(
    title_font=dict(size=30, family="Arial Black", color="#2C3E50"),
    xaxis_title_font=dict(size=18, family="Verdana", color="#34495E"),
    yaxis_title_font=dict(size=18, family="Verdana", color="#34495E"),
    xaxis=dict(tickfont=dict(size=14, family="Tahoma", color="#7F8C8D")),
    yaxis=dict(tickfont=dict(size=14, family="Tahoma", color="#7F8C8D")),
    paper_bgcolor="#FDFEFE",  
    plot_bgcolor="#ECF0F1",   
    margin=dict(l=50, r=50, t=80, b=50),  
)


fig.update_traces(
    marker_color=["#3498DB" if star > 10000 else "#9B59B6" for star in repos_stars],
    marker_opacity=0.85,
    marker_line=dict(width=1, color="#1C2833"), 
    hoverlabel=dict(font_size=14, font_family="Courier New", bgcolor="#D5DBDB", bordercolor="#34495E")
)

fig.show()

fig.write_html(f"Most Starred {language} Projects in GitHub.html")