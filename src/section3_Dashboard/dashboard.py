import dash
from dash import dcc, html
import requests
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)

base_url = "http://127.0.0.1:5000"

def get_data(endpoint):
    try:
        response = requests.get(f"{base_url}{endpoint}")
        return response.json() if response.status_code == 200 else {}
    except requests.exceptions.RequestException as e:
        return {}

trending_repos = get_data("/api/trending_repos")
most_forked = get_data("/api/most_forked")
language_trends = get_data("/api/language_trends")
popular_by_lang = get_data("/api/popular_by_language")


df_trending = pd.DataFrame(trending_repos if isinstance(trending_repos, list) else []) if trending_repos else pd.DataFrame(columns=["name", "stars", "url"])
df_forked = pd.DataFrame(most_forked if isinstance(most_forked, list) else []) if most_forked else pd.DataFrame(columns=["name", "forks", "url"])

lang_trends_data = []
if language_trends and isinstance(language_trends, dict):
    for lang, years in language_trends.items():
        for year, count in years.items():
            lang_trends_data.append({"language": lang, "year": int(year), "repositories": count})
df_lang_trends = pd.DataFrame(lang_trends_data) if lang_trends_data else pd.DataFrame(columns=["language", "year", "repositories"])


popular_data = []
if popular_by_lang and isinstance(popular_by_lang, dict):
    for lang, repos in popular_by_lang.items():
        if isinstance(repos, list):
            for repo in repos:
                popular_data.append({"language": lang, "name": repo.get("name", ""), "stars": repo.get("stars", 0), "url": repo.get("url", "")})
df_popular = pd.DataFrame(popular_data) if popular_data else pd.DataFrame(columns=["language", "name", "stars", "url"])

#links to the respective repositories
for df in [df_trending, df_forked, df_popular]:
    if 'url' in df.columns and not df.empty:
        df['name'] = df.apply(lambda row: f'<a href="{row["url"]}" target="_blank">{row["name"]}</a>', axis=1)


#plotting
fig_trending = px.bar(df_trending, x="name", y="stars", title="Top Starred Repositories (Last 7 Days)") if not df_trending.empty else px.bar(title="Top Starred Repositories (No Data)")
fig_trending.update_traces(hovertemplate='<b>%{x}</b><extra></extra>', hoverlabel=dict(bgcolor="white", font=dict(color="black")))

fig_forked = px.bar(df_forked, x="name", y="forks", title="Most Forked Repositories (Last 30 Days)") if not df_forked.empty else px.bar(title="Most Forked Repositories (No Data)")
fig_forked.update_traces(hovertemplate='<b>%{x}</b><extra></extra>', hoverlabel=dict(bgcolor="white", font=dict(color="black")))

fig_lang_trends = px.line(
    df_lang_trends,
    x="year",
    y="repositories",
    color="language",
    title="Language Popularity Over Last 5 Years",
    markers=True
) if not df_lang_trends.empty else px.line(title="Language Trends (No Data)")
fig_lang_trends.update_traces(hovertemplate='<b>%{x}</b>: %{y} repositories<extra></extra>')


fig_popular = px.bar(df_popular, x="name", y="stars", color="language", title="Most Popular Projects by Language (Last 90 Days)",
                      barmode="group", height=600) if not df_popular.empty else px.bar(title="Most Popular Projects by Language (No Data)")
fig_popular.update_traces(hovertemplate='<b>%{x}</b><extra></extra>')

app.layout = html.Div(children=[
    html.H1("GitHub Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig_trending),
    dcc.Graph(figure=fig_forked),
    dcc.Graph(figure=fig_lang_trends),
    dcc.Graph(figure=fig_popular),
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)