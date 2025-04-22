from googleapiclient.discovery import build
import pandas as pd

API_KEY = "AIzaSyCrOujCpBdnw1Q6m-WGGpntMswtx3gw-Mo"  

youtube = build("youtube", "v3", developerKey=API_KEY)

def fetch_video_data(video_ids):
    data = []

    for vid in video_ids:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=vid
        )
        response = request.execute()

        for item in response.get("items", []):
            snippet = item["snippet"]
            stats = item["statistics"]

            title = snippet["title"]
            description = snippet.get("description", "")
            channel_title = snippet["channelTitle"]

            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))

            data.append({
                "video_id": vid,
                "title": title,
                "channel": channel_title,
                "description": description,
                "views": views,
                "likes": likes,
                "comments": comments
            })

    return pd.DataFrame(data)
