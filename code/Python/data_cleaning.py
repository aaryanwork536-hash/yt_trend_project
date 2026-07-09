import pandas as pd
import numpy as np
import glob
import os

def clean_and_engineer():
    path = 'Dataset/'
    all_files = glob.glob(os.path.join(path, "*videos.csv"))
    
    combined_list = []
    category_map = {1: "Film & Animation", 10: "Music", 17: "Sports", 20: "Gaming", 24: "Entertainment"}

    for filename in all_files:
        country_code = os.path.basename(filename)[:2]
        df = pd.read_csv(filename)
        df['country'] = country_code
        combined_list.append(df)
        
    df = pd.concat(combined_list, ignore_index=True)
    
    # 1. Clean Data (Fixed the inplace=True warning for Copy-on-Write)
    df = df.drop_duplicates(subset=['video_id', 'trending_date'])
    df['description'] = df['description'].fillna('No Description')
    df = df.drop(columns=['thumbnail_link'], errors='ignore')
    
    # 2. Standardize Dates & Strip Timezones (Fixed the TypeError)
    # .dt.tz_localize(None) strips the UTC 'Z' offset so we can do math safely
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.tz_localize(None)
    df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m', errors='coerce')
    
    # Drop rows with broken dates
    df = df.dropna(subset=['publish_time', 'trending_date'])
    
    # Map category names
    df['category'] = df['category_id'].map(category_map).fillna('Other')
    
    # 3. Feature Engineering (Math will work perfectly now!)
    df['views_safe'] = df['views'].replace(0, np.nan)
    
    df['Engagement'] = ((df['likes'] + df['comment_count']) / df['views_safe'] * 100).fillna(0)
    df['Like Ratio'] = (df['likes'] / df['views_safe'] * 100).fillna(0)
    df['Comment Ratio'] = (df['comment_count'] / df['views_safe'] * 100).fillna(0)
    
    # Video Age subtraction works flawlessly because both sides are now timezone-naive
    df['Video Age'] = (df['trending_date'] - df['publish_time']).dt.days
    df['Day'] = df['publish_time'].dt.day_name()
    df['Month'] = df['publish_time'].dt.month_name()
    df['Hour'] = df['publish_time'].dt.hour
    
    df = df.drop(columns=['views_safe'])
    
    output_path = 'Cleaned_Data/youtube_cleaned.csv'
    df.to_csv(output_path, index=False)
    print(f"Data pipeline complete! Cleaned dataset saved to: {output_path}")

if __name__ == "__main__":
    clean_and_engineer()