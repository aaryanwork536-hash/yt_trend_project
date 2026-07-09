USE youtube_analytics;

-- 1. Identify Top 10 Most Viewed Channels Across All Regions
SELECT 
    channel_title, 
    COUNT(DISTINCT video_id) AS total_trending_videos,
    SUM(views) AS total_views
FROM trending_videos
GROUP BY channel_title
ORDER BY total_views DESC
LIMIT 10;

-- 2. Regional Audience Preference (Category breakdown per country)
SELECT 
    country, 
    category, 
    SUM(views) AS regional_views,
    RANK() OVER(PARTITION BY country ORDER BY SUM(views) DESC) as category_rank
FROM trending_videos
GROUP BY country, category;

-- 3. Optimal Publishing Window Analysis
SELECT 
    publish_hour, 
    AVG(Engagement) AS avg_engagement_rate,
    AVG(views) AS avg_views
FROM trending_videos
GROUP BY publish_hour
ORDER BY avg_engagement_rate DESC;