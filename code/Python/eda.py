import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Cleaned Data
df = pd.read_csv('Cleaned_Data/youtube_cleaned.csv')
os.makedirs("Dashboard Images", exist_ok=True)

# Set visual styles
sns.set_theme(style="whitegrid")

# 1. Top Categories by Views
plt.figure(figsize=(10,5))
cat_views = df.groupby("category")["views"].sum().sort_values(ascending=False)
sns.barplot(x=cat_views.values, y=cat_views.index, palette="viridis")
plt.title("Total Views by Category")
plt.xlabel("Views (in Billions)")
plt.tight_layout()
plt.savefig("Dashboard Images/category_views.png")
plt.close()

# 2. Engagement Correlation Matrix
plt.figure(figsize=(8,6))
numerical_cols = ['views', 'likes', 'dislikes', 'comment_count', 'Engagement', 'Video Age']
corr_matrix = df[numerical_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix Matrix of Key Metrics")
plt.tight_layout()
plt.savefig("Dashboard Images/correlation_heatmap.png")
plt.close()

# 3. Views vs Likes Scatter Plot
plt.figure(figsize=(8,5))
sns.scatterplot(data=df, x='views', y='likes', hue='country', alpha=0.6)
plt.title("Relationship Between Views & Likes")
plt.xlabel("Views")
plt.ylabel("Likes")
plt.tight_layout()
plt.savefig("Dashboard Images/views_likes_scatter.png")
plt.close()

print("EDA charts generated and saved successfully in 'Dashboard Images/'!")