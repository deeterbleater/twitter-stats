import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from wordcloud import WordCloud
import re
import base64
from io import BytesIO
import json
import os

# Function to generate CSV from tweets.js
def generate_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        # Remove the JavaScript assignment part
        json_content = content.replace('window.YTD.tweets.part0 = ', '', 1)
        data = json.loads(json_content)

    tweets = []
    for tweet_obj in data:
        tweet = tweet_obj['tweet']
        tweets.append(tweet)

    df = pd.DataFrame(tweets)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df.to_csv(output_file, index=False)
    return df

# Check if tweets.csv exists, if not, generate it
data_dir = 'data'
tweets_js = os.path.join(data_dir, 'tweets.js')
tweets_csv = os.path.join(data_dir, 'tweets.csv')

if not os.path.exists(tweets_csv):
    if os.path.exists(tweets_js):
        df = generate_csv(tweets_js, tweets_csv)
    else:
        raise FileNotFoundError("tweets.js file not found in the data directory")
else:
    df = pd.read_csv(tweets_csv)
    df['created_at'] = pd.to_datetime(df['created_at'])

# Preprocess data
df['year_month'] = df['created_at'].dt.to_period('M').astype(str)
df['hour'] = df['created_at'].dt.hour

# Filter data for word cloud
df_filtered = df[~df['full_text'].str.startswith('RT')]
df_filtered = df_filtered[~df_filtered['full_text'].str.startswith('https')]
df_filtered['full_text'] = df_filtered['full_text'].apply(lambda x: re.sub(r'https?://\S+|www\.\S+', '', x))
df_filtered['full_text'] = df_filtered['full_text'].apply(lambda x: re.sub(r'@', '@', x))
all_text = ' '.join(df_filtered['full_text'].astype(str))

# Create Dash app
app = Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Twitter Stats Dashboard"),
    
    dcc.Graph(id='tweets-over-time'),
    dcc.Graph(id='engagement-over-time'),
    dcc.Graph(id='tweeting-hours'),
    dcc.Graph(id='bangers-by-hour'),
    html.Img(id='wordcloud-image'),
])

# Callback for tweets over time
@app.callback(Output('tweets-over-time', 'figure'),
              Input('tweets-over-time', 'id'))
def update_tweets_over_time(_):
    tweets_per_month = df.groupby('year_month').size()
    
    # Convert index to strings
    tweets_per_month.index = tweets_per_month.index.astype(str)
    
    fig = px.line(x=tweets_per_month.index, y=tweets_per_month.values,
                  title="Tweet Activity Over Time")
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Number of Tweets")
    return fig

# Callback for engagement over time
@app.callback(Output('engagement-over-time', 'figure'),
              Input('engagement-over-time', 'id'))
def update_engagement_over_time(_):
    engagement_over_time = df.groupby('year_month').agg({'favorite_count': 'mean', 'retweet_count': 'mean'})
    
    # Convert index to strings
    engagement_over_time.index = engagement_over_time.index.astype(str)
    
    fig = px.line(engagement_over_time, title="Average Engagement Over Time")
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Average Count")
    return fig

# Callback for tweeting hours
@app.callback(Output('tweeting-hours', 'figure'),
              Input('tweeting-hours', 'id'))
def update_tweeting_hours(_):
    tweets_per_hour = df.groupby('hour').size()
    fig = px.bar(x=tweets_per_hour.index, y=tweets_per_hour.values,
                 title="Tweet Activity by Hour")
    fig.update_xaxes(title="Hour of the Day")
    fig.update_yaxes(title="Number of Tweets")
    return fig

# Callback for bangers by hour
@app.callback(Output('bangers-by-hour', 'figure'),
              Input('bangers-by-hour', 'id'))
def update_bangers_by_hour(_):
    Q1 = df['favorite_count'].quantile(0.25)
    Q3 = df['favorite_count'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 100.5 * IQR
    filtered_df = df[(df['favorite_count'] >= lower_bound) & (df['favorite_count'] <= upper_bound)]
    
    fig = px.scatter(filtered_df, x='hour', y='favorite_count',
                     title='Correlation Between Time of Tweet and Number of Likes (Without Outliers)')
    fig.update_xaxes(title="Hour of the Day")
    fig.update_yaxes(title="Number of Likes")
    return fig

# Callback for word cloud
@app.callback(Output('wordcloud-image', 'src'),
              Input('wordcloud-image', 'id'))
def update_wordcloud(_):
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(all_text)
    img = wordcloud.to_image()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded_image}"

if __name__ == '__main__':
    app.run_server(debug=True)