"""
    Reddit Data Collection Script for Care Worker Discourse Analysis

This script collects publicly available posts from r/CNA to analyze
care worker discussions about stress, technology use, and coping strategies.

"""

import praw
import pandas as pd
from datetime import datetime
from collections import Counter
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USER_AGENT = os.getenv('REDDIT_USER_AGENT')

# Verify credentials are loaded
if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: Reddit API credentials not found!")
    print("Make sure you have a .env file in the repo root with:")
    print("  REDDIT_CLIENT_ID=your_id")
    print("  REDDIT_CLIENT_SECRET=your_secret")
    print("  REDDIT_USER_AGENT=your_user_agent")
    print("\nSee .env.example for template")
    exit(1)

print("OK - Credentials loaded from environment")

# Initialize Reddit connection
print("Connecting to Reddit...")
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# DATA COLLECTION

print("Collecting posts from r/CNA...")
subreddit = reddit.subreddit('CNA')
posts_data = []

# Collect posts from multiple time filters to maximize coverage
time_filters = ['all', 'year']
collected_ids = set()

for time_filter in time_filters:
    print(f"  Fetching {time_filter} posts...")
    for post in subreddit.top(time_filter=time_filter, limit=1000):
        # Avoid duplicates
        if post.id in collected_ids:
            continue
        
        collected_ids.add(post.id)
        post_date = datetime.fromtimestamp(post.created_utc)
        
        # Filter for 2022-2024 (adjust as needed)
        if post_date.year >= 2022:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'text': post.selftext,
                'score': post.score,
                'num_comments': post.num_comments,
                'created_date': post_date,
                'year': post_date.year,
                'url': f"https://reddit.com{post.permalink}"
            })

# Also get recent posts
print("  Fetching new posts...")
for post in subreddit.new(limit=500):
    if post.id not in collected_ids:
        collected_ids.add(post.id)
        post_date = datetime.fromtimestamp(post.created_utc)
        
        if post_date.year >= 2022:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'text': post.selftext,
                'score': post.score,
                'num_comments': post.num_comments,
                'created_date': post_date,
                'year': post_date.year,
                'url': f"https://reddit.com{post.permalink}"
            })

# Create DataFrame
df = pd.DataFrame(posts_data)
df = df.sort_values('created_date', ascending=False)

print(f"\nOK - Collected {len(df)} posts")
print(f"  Date range: {df['created_date'].min().date()} to {df['created_date'].max().date()}")
print(f"  Breakdown by year:")
print(df['year'].value_counts().sort_index())


# WORD FREQUENCY ANALYSIS

print("\n" + "="*50)
print("WORD FREQUENCY ANALYSIS")
print("="*50)

# Combine all text
all_text = ' '.join(
    df['title'].fillna('') + ' ' + df['text'].fillna('')
).lower()

# Define target terms
terms_categories = {
    'Technology General': ['app', 'apps', 'phone', 'smartphone', 'software', 'digital', 'online', 'website', 'tech'],
    'Wellness Apps': ['calm', 'headspace', 'meditation', 'mindfulness', 'betterhelp', 'talkspace', 'therapy app'],
    'Job Search': ['indeed', 'hiring', 'job search', 'apply', 'application', 'resume', 'interview'],
    'Work/Pay': ['wage', 'wages', 'pay', 'salary', 'hours', 'shift', 'schedule', 'scheduling', 'overtime'],
    'Stress/Burnout': ['stress', 'stressed', 'burnout', 'exhausted', 'tired', 'overwhelmed', 'anxiety', 'anxious', 'depressed', 'depression'],
    'Quit/Leave': ['quit', 'quitting', 'leave', 'leaving', 'resign', 'walk out']
}

def count_term(text, term):
    """Count occurrences of a term (handles multi-word phrases)"""
    if ' ' in term:
        # Multi-word phrase
        return text.count(term)
    else:
        # Single word - use word boundaries
        pattern = r'\b' + re.escape(term) + r'\b'
        return len(re.findall(pattern, text))

# Count all terms
for category, terms in terms_categories.items():
    print(f"\n{category}:")
    for term in terms:
        count = count_term(all_text, term)
        if count > 0:
            print(f"  '{term}': {count}")


# IDENTIFY HIGH-ENGAGEMENT POSTS FOR MANUAL REVIEW

print("\n" + "="*50)
print("PREPARING FOR MANUAL ANALYSIS")
print("="*50)

# Filter for posts with substance (not just title)
substantive = df[df['text'].str.len() > 50].copy()

# Sort by engagement (score + comments)
substantive['engagement'] = substantive['score'] + substantive['num_comments']
substantive = substantive.sort_values('engagement', ascending=False)

# Save different cuts for analysis
# Top 150 most engaging posts
top_posts = substantive.head(150)
top_posts.to_excel('top_150_cna_posts.xlsx', index=False)
print(f"OK - Saved top 150 most-engaged posts to 'top_150_cna_posts.xlsx'")

# All substantive posts
substantive.to_excel('all_cna_posts_substantive.xlsx', index=False)
print(f"OK - Saved {len(substantive)} substantive posts to 'all_cna_posts_substantive.xlsx'")

# Create a filtered set for specific themes
keywords = ['app', 'stress', 'burnout', 'quit', 'wage', 'indeed', 'schedule', 'tired', 'overwhelmed']
pattern = '|'.join(keywords)

themed = substantive[
    substantive['title'].str.contains(pattern, case=False, na=False) |
    substantive['text'].str.contains(pattern, case=False, na=False)
]
themed.to_excel('themed_posts_for_analysis.xlsx', index=False)
print(f"OK - Saved {len(themed)} theme-relevant posts to 'themed_posts_for_analysis.xlsx'")

print("\n" + "="*50)
print("COLLECTION COMPLETE!")
print("="*50)
print("\nNext steps:")
print("1. Open 'top_150_cna_posts.xlsx' in Excel/Google Sheets")
print("2. Read through posts and look for patterns")
print("3. Copy interesting quotes (will anonymize later)")
print("4. Note recurring themes")
print("\nRecommended: Read at least 100-120 posts for thematic analysis")