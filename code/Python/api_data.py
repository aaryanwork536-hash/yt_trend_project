import os
from googleapiclient.discovery import build
import pandas as pd

def fetch_live_trending(api_key, region_code="US"):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        request = youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            maxResults=10,
            regionCode=region_code
        )
        response = request.execute()
        
        extracted_data = []
        for item in response.get('items', []):
            data = {
                "video_id": item['id'],
                "title": item['snippet']['title'],
                "channel_title": item['snippet']['channelTitle'],
                "category_id": item['snippet']['categoryId'],
                "views": int(item['statistics'].get('viewCount', 0)),
                "likes": int(item['statistics'].get('likeCount', 0)),
                "comment_count": int(item['statistics'].get('commentCount', 0)),
                "country": region_code
            }
            extracted_data.append(data)
            
        df = pd.DataFrame(extracted_data)
        df.to_csv(f"Cleaned_Data/live_api_trending_{region_code}.csv", index=False)
        print(f"Successfully harvested live API trends for region: {region_code}")
        
    except Exception as e:
        print(f"API Connection Failed: {e}. Please ensure your API Key is active and valid.")

if __name__ == "__main__":
   
    API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_GOOGLE_API_KEY")
    if API_KEY != "YOUR_GOOGLE_API_KEY":
        fetch_live_trending(API_KEY, region_code="US")
    else:
        print("Skipping Live API pull: Default mock key detected. Add a real API key to pull live records.")
