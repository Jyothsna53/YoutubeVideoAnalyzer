from flask import Flask, render_template, request
import pandas as pd
from youtube_video_trends_analyzer import fetch_video_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Shows styled input form

@app.route('/analyze', methods=['POST'])
def analyze():
    video_links = request.form['video_links']
    
    # Extract video IDs from links
    video_ids = [link.strip().split('v=')[-1] for link in video_links.split(',')]

    # Fetch data using your helper function
    df = fetch_video_data(video_ids)

    if df.empty:
        return "⚠️ No data found. Please check the video links and your API key."

    # Calculate engagement score
    df['engagement_score'] = (df['likes'] + df['comments']) / df['views']
    df['engagement_score'] = df['engagement_score'].round(4)

    # Shorten description to ~200 chars
    df['short_description'] = df['description'].apply(lambda x: x[:200] + "..." if len(x) > 200 else x)

    # Format numbers for readability
    df['views'] = df['views'].apply(lambda x: f"{x:,}")
    df['likes'] = df['likes'].apply(lambda x: f"{x:,}")
    df['comments'] = df['comments'].apply(lambda x: f"{x:,}")

    # Identify best performing video
    df['eng_raw'] = df['engagement_score']  # Raw for comparison
    best_idx = df['eng_raw'].astype(float).idxmax()
    best_video = df.loc[best_idx]

    best_video_summary = {
        "title": best_video['title'],
        "channel": best_video['channel'],
        "engagement_score": best_video['eng_raw'],
        "description": best_video['description'][:500] + '...' if len(best_video['description']) > 500 else best_video['description']
    }

    # Prepare display DataFrame
    display_df = df[['title', 'channel', 'views', 'likes', 'comments', 'engagement_score', 'short_description']]
    display_df.rename(columns={'short_description': 'description'}, inplace=True)

    return render_template(
        "dashboard.html",
        tables=[display_df.to_html(classes='data', index=False)],
        best_video=best_video_summary
    )

if __name__ == '__main__':
    app.run(debug=True)
