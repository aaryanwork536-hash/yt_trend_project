import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create directory structure
os.makedirs("Dataset", exist_ok=True)
os.makedirs("Cleaned_Data", exist_ok=True)

def generate_mock_csv(country_code, num_rows=1000):
    np.random.seed(42)
    
    video_ids = [f"vid_{i:04d}" for i in range(num_rows)]
    titles = [f"Amazing {country_code} Video Trend {i}" for i in range(num_rows)]
    channels = [f"Channel {np.random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Omega'])}" for _ in range(num_rows)]
    category_ids = np.random.choice([1, 10, 17, 20, 24], size=num_rows) # Music, Entertainment, Sports, Gaming etc.
    
    # Generate dates in 2026
    base_date = datetime(2026, 1, 1)
    publish_times = [base_date + timedelta(days=int(np.random.randint(0, 30)), hours=int(np.random.randint(0, 23))) for _ in range(num_rows)]
    trending_dates = [p + timedelta(days=int(np.random.randint(1, 7))) for p in publish_times]
    
    views = np.random.randint(10000, 5000000, size=num_rows)
    likes = (views * np.random.uniform(0.02, 0.10)).astype(int)
    dislikes = (views * np.random.uniform(0.001, 0.005)).astype(int)
    comment_counts = (likes * np.random.uniform(0.05, 0.20)).astype(int)
    
    tags = ["news|trending", "music|hit", "gaming|walkthrough", "sports|highlights", "funny|vlog"]
    chosen_tags = [np.random.choice(tags) for _ in range(num_rows)]
    descriptions = [f"This is a trending video in {country_code}!" for _ in range(num_rows)]
    
    df = pd.DataFrame({
        "video_id": video_ids,
        "title": titles,
        "channel_title": channels,
        "category_id": category_ids,
        "publish_time": [p.strftime("%Y-%m-%dT%H:%M:%S.000Z") for p in publish_times],
        "trending_date": [t.strftime("%y.%d.%m") for t in trending_dates],
        "views": views,
        "likes": likes,
        "dislikes": dislikes,
        "comment_count": comment_counts,
        "tags": chosen_tags,
        "thumbnail_link": [f"https://i.ytimg.com/vi/{vid}/default.jpg" for vid in video_ids],
        "comments_disabled": np.random.choice([False, True], p=[0.95, 0.05], size=num_rows),
        "ratings_disabled": np.random.choice([False, True], p=[0.98, 0.02], size=num_rows),
        "video_error_or_removed": np.random.choice([False, True], p=[0.99, 0.01], size=num_rows),
        "description": descriptions
    })
    
    # Introduce some artificial missing values to clean later
    df.loc[df.sample(frac=0.05).index, 'description'] = np.nan
    
    file_path = f"Dataset/{country_code}videos.csv"
    df.to_csv(file_path, index=False)
    print(f"Generated: {file_path}")

# Generate datasets
for country in ["US", "IN", "GB"]:
    generate_mock_csv(country)