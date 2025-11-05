import pandas as pd
import re
from collections import Counter
import openpyxl
from openpyxl.styles import PatternFill, Font
from datetime import datetime

print("="*60)
print("THEMATIC CODING ANALYSIS")
print("="*60)

# ============================================
# LOAD DATA
# ============================================
print("\n1. Loading data...")
df = pd.read_excel('themed_posts_for_analysis.xlsx')
print(f"   Loaded {len(df)} themed posts")

# Combine title and text for analysis
df['full_text'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
df['full_text_lower'] = df['full_text'].str.lower()

# ============================================
# DEFINE CODING CATEGORIES
# ============================================

categories = {
    'wellness_app_mentioned': {
        'keywords': ['calm', 'headspace', 'meditation app', 'betterhelp', 'talkspace', 
                     'mindfulness', 'wellness app', 'self-care app', 'therapy app',
                     'insight timer', 'gratitude journal', 'mental health app'],
        'description': 'Mentions wellness/mental health apps'
    },
    'wellness_app_abandoned': {
        'keywords': ['never use', 'never open', 'don\'t use', 'downloaded but', 
                     'sitting on my phone', 'never log in', 'forgot about',
                     'too tired to use', 'no time to use', 'haven\'t opened'],
        'description': 'Discusses not using wellness apps',
        'requires': 'wellness_app_mentioned'  # Only flag if app is mentioned
    },
    'job_search_tech': {
        'keywords': ['indeed', 'job search', 'looking for another job', 'applying',
                     'job application', 'resume', 'interview', 'better paying',
                     'new job', 'quit', 'leaving this job'],
        'description': 'Technology use for job searching'
    },
    'scheduling_issues': {
        'keywords': ['schedule', 'scheduling', 'shift', 'overtime', 'mandatory',
                     'call in', 'call out', 'short staffed', 'understaffed',
                     'double shift', 'no break', 'can\'t take break'],
        'description': 'Work schedule and time issues'
    },
    'pay_financial_stress': {
        'keywords': ['pay', 'wage', 'salary', 'money', 'afford', 'bills', 'rent',
                     'broke', 'underpaid', 'minimum wage', 'low pay', 'poor',
                     'financial', 'second job', 'side gig'],
        'description': 'Financial stress and low wages'
    },
    'burnout_exhaustion': {
        'keywords': ['burnout', 'burned out', 'exhausted', 'tired', 'drained',
                     'can\'t do this', 'overwhelming', 'too much', 'breaking down',
                     'mental health', 'depressed', 'anxiety', 'stressed'],
        'description': 'Expressions of burnout and exhaustion'
    },
    'peer_support_seeking': {
        'keywords': ['does anyone else', 'am i the only', 'how do you', 'anyone have',
                     'need advice', 'what should i do', 'help', 'is this normal'],
        'description': 'Seeking support from community'
    },
    'employer_program': {
        'keywords': ['eap', 'employee assistance', 'wellness program', 
                     'company offered', 'employer provided', 'work program',
                     'benefits', 'mental health benefit'],
        'description': 'Mentions employer wellness programs'
    }
}

# ============================================
# AUTOMATED CATEGORIZATION
# ============================================
print("\n2. Categorizing posts...")

for category_name, category_info in categories.items():
    df[category_name] = False
    
    for keyword in category_info['keywords']:
        # Case-insensitive search
        mask = df['full_text_lower'].str.contains(keyword, na=False, regex=False)
        df.loc[mask, category_name] = True
    
    # Check for dependency
    if 'requires' in category_info:
        required_category = category_info['requires']
        # Only mark as True if the required category is also True
        df.loc[~df[required_category], category_name] = False
    
    count = df[category_name].sum()
    percentage = (count / len(df)) * 100
    print(f"   {category_name}: {count} posts ({percentage:.1f}%)")

# ============================================
# EXTRACT POTENTIAL QUOTES
# ============================================
print("\n3. Extracting potential quotes...")

def extract_sentences(text, max_length=200):
    """Extract sentences that might be good quotes"""
    if pd.isna(text) or text == '':
        return []
    
    # Split into sentences (rough)
    sentences = re.split(r'[.!?]+', text)
    
    # Clean and filter
    good_sentences = []
    for sent in sentences:
        sent = sent.strip()
        # Keep sentences that are 20-200 chars and contain meaningful content
        if 20 < len(sent) < max_length and not sent.lower().startswith(('http', 'www')):
            good_sentences.append(sent)
    
    return good_sentences

# Extract quotes for posts with wellness app mentions
df['potential_quotes'] = df['full_text'].apply(extract_sentences)

# ============================================
# IDENTIFY KEY PATTERNS
# ============================================
print("\n4. Identifying key patterns...")

# Pattern 1: App Adoption-Abandonment
apps_mentioned = df['wellness_app_mentioned'].sum()
apps_abandoned = df['wellness_app_abandoned'].sum()
if apps_mentioned > 0:
    abandonment_rate = (apps_abandoned / apps_mentioned) * 100
    print(f"\n   PATTERN 1: App Adoption-Abandonment Gap")
    print(f"   - Apps mentioned: {apps_mentioned} posts")
    print(f"   - Apps abandoned: {apps_abandoned} posts")
    print(f"   - Abandonment rate: {abandonment_rate:.0f}%")

# Pattern 2: Job Search vs Wellness Apps
job_search = df['job_search_tech'].sum()
print(f"\n   PATTERN 2: Job Search as Active Tech Use")
print(f"   - Job search mentions: {job_search} posts")
print(f"   - Ratio (job search / wellness apps): {job_search/apps_mentioned:.1f}x" if apps_mentioned > 0 else "")

# Pattern 3: Peer Support
peer_support = df['peer_support_seeking'].sum()
print(f"\n   PATTERN 3: Peer Support Seeking")
print(f"   - Support-seeking posts: {peer_support} posts")
print(f"   - Percentage of sample: {(peer_support/len(df))*100:.1f}%")

# Pattern 4: Economic Precarity
financial = df['pay_financial_stress'].sum()
print(f"\n   PATTERN 4: Economic Precarity")
print(f"   - Financial stress mentions: {financial} posts")

# Pattern 5: Time Poverty
scheduling = df['scheduling_issues'].sum()
burnout = df['burnout_exhaustion'].sum()
print(f"\n   PATTERN 5: Time Poverty & Burnout")
print(f"   - Scheduling issues: {scheduling} posts")
print(f"   - Burnout/exhaustion: {burnout} posts")

# ============================================
# CREATE PRIORITY REVIEW LIST
# ============================================
print("\n5. Creating priority review lists...")

# High-priority posts for manual review
priority_posts = []

# Posts with wellness app abandonment (key pattern)
abandonment_posts = df[df['wellness_app_abandoned']].copy()
abandonment_posts['priority_reason'] = 'Wellness app abandonment'
priority_posts.append(abandonment_posts)

# Posts mentioning both job search AND wellness topics
both_posts = df[df['job_search_tech'] & (df['wellness_app_mentioned'] | df['burnout_exhaustion'])].copy()
both_posts['priority_reason'] = 'Job search + wellness/burnout'
priority_posts.append(both_posts)

# High-engagement peer support posts
high_engagement = df[df['peer_support_seeking'] & (df['score'] + df['num_comments'] > 20)].copy()
high_engagement['priority_reason'] = 'High-engagement peer support'
priority_posts.append(high_engagement)

# Posts mentioning employer programs (rare but interesting)
employer_posts = df[df['employer_program']].copy()
employer_posts['priority_reason'] = 'Employer program mentioned'
priority_posts.append(employer_posts)

# Combine priority posts
priority_df = pd.concat(priority_posts, ignore_index=True)
priority_df = priority_df.drop_duplicates(subset=['id'])
priority_df = priority_df.sort_values('engagement', ascending=False)

print(f"   Created priority review list: {len(priority_df)} posts")

# ============================================
# EXPORT RESULTS
# ============================================
print("\n6. Exporting results...")

# Create Excel workbook with multiple sheets
output_file = 'thematic_coding_results.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Sheet 1: Summary Statistics
    summary_data = []
    for cat_name, cat_info in categories.items():
        count = df[cat_name].sum()
        percentage = (count / len(df)) * 100
        summary_data.append({
            'Category': cat_name,
            'Description': cat_info['description'],
            'Count': count,
            'Percentage': f"{percentage:.1f}%"
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Sheet 2: Pattern Analysis
    patterns_data = [
        {'Pattern': 'App Adoption-Abandonment Gap', 
         'Mentions': apps_mentioned, 
         'Abandoned': apps_abandoned,
         'Rate': f"{abandonment_rate:.0f}%" if apps_mentioned > 0 else "N/A"},
        {'Pattern': 'Job Search as Active Tech', 
         'Count': job_search,
         'Vs_Wellness': f"{job_search/apps_mentioned:.1f}x more" if apps_mentioned > 0 else "N/A"},
        {'Pattern': 'Peer Support Seeking',
         'Count': peer_support,
         'Percentage': f"{(peer_support/len(df))*100:.1f}%"},
        {'Pattern': 'Economic Precarity Focus',
         'Count': financial,
         'Percentage': f"{(financial/len(df))*100:.1f}%"},
        {'Pattern': 'Time Poverty & Burnout',
         'Scheduling': scheduling,
         'Burnout': burnout}
    ]
    patterns_df = pd.DataFrame(patterns_data)
    patterns_df.to_excel(writer, sheet_name='Patterns', index=False)
    
    # Sheet 3: Priority Posts for Manual Review
    review_columns = ['id', 'title', 'text', 'score', 'num_comments', 'engagement',
                     'priority_reason', 'wellness_app_mentioned', 'wellness_app_abandoned',
                     'job_search_tech', 'burnout_exhaustion', 'peer_support_seeking']
    priority_df[review_columns].to_excel(writer, sheet_name='Priority_Review', index=False)
    
    # Sheet 4: Wellness App Posts (for quote extraction)
    wellness_posts = df[df['wellness_app_mentioned']].copy()
    wellness_columns = ['id', 'title', 'text', 'score', 'num_comments',
                       'wellness_app_abandoned', 'job_search_tech', 'burnout_exhaustion']
    wellness_posts[wellness_columns].to_excel(writer, sheet_name='Wellness_App_Posts', index=False)
    
    # Sheet 5: Job Search Posts
    job_posts = df[df['job_search_tech']].copy()
    job_columns = ['id', 'title', 'text', 'score', 'num_comments', 'burnout_exhaustion']
    job_posts[job_columns].to_excel(writer, sheet_name='Job_Search_Posts', index=False)
    
    # Sheet 6: All Posts with Categories
    export_columns = ['id', 'title', 'text', 'score', 'num_comments', 'created_date'] + list(categories.keys())
    df[export_columns].to_excel(writer, sheet_name='All_Coded_Posts', index=False)

print(f"   ✓ Results saved to: {output_file}")

# ============================================
# GENERATE QUOTE CANDIDATES
# ============================================
print("\n7. Extracting quote candidates...")

quote_candidates = []

# From wellness app abandonment posts
for idx, row in df[df['wellness_app_abandoned']].iterrows():
    sentences = extract_sentences(row['full_text'])
    for sent in sentences:
        sent_lower = sent.lower()
        # Look for sentences that mention both apps and non-use
        if any(word in sent_lower for word in ['calm', 'headspace', 'app']) and \
           any(word in sent_lower for word in ['never', 'don\'t', 'haven\'t', 'tired', 'time']):
            quote_candidates.append({
                'post_id': row['id'],
                'category': 'wellness_app_abandoned',
                'quote': sent,
                'score': row['score'],
                'engagement': row['score'] + row['num_comments']
            })

# From job search posts
for idx, row in df[df['job_search_tech']].iterrows():
    sentences = extract_sentences(row['full_text'])
    for sent in sentences:
        sent_lower = sent.lower()
        if 'indeed' in sent_lower or 'job' in sent_lower or 'pay' in sent_lower:
            quote_candidates.append({
                'post_id': row['id'],
                'category': 'job_search',
                'quote': sent,
                'score': row['score'],
                'engagement': row['score'] + row['num_comments']
            })

# From burnout posts
for idx, row in df[df['burnout_exhaustion']].head(50).iterrows():
    sentences = extract_sentences(row['full_text'])
    for sent in sentences[:2]:  # Just first 2 sentences
        sent_lower = sent.lower()
        if any(word in sent_lower for word in ['tired', 'exhausted', 'burnout', 'can\'t']):
            quote_candidates.append({
                'post_id': row['id'],
                'category': 'burnout',
                'quote': sent,
                'score': row['score'],
                'engagement': row['score'] + row['num_comments']
            })

# Save quote candidates
quotes_df = pd.DataFrame(quote_candidates)
quotes_df = quotes_df.sort_values('engagement', ascending=False)
quotes_df = quotes_df.drop_duplicates(subset=['quote'])
quotes_df.to_excel('quote_candidates.xlsx', index=False)

print(f"   ✓ Extracted {len(quotes_df)} quote candidates")
print(f"   ✓ Saved to: quote_candidates.xlsx")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)
print(f"\nDataset: {len(df)} posts analyzed")
print(f"\nKey Files Created:")
print(f"  1. thematic_coding_results.xlsx - Full analysis with 6 sheets")
print(f"  2. quote_candidates.xlsx - {len(quotes_df)} potential quotes")
print(f"\nNext Steps:")
print(f"  1. Review 'Priority_Review' sheet ({len(priority_df)} posts)")
print(f"  2. Select best quotes from 'quote_candidates.xlsx'")
print(f"  3. Read high-engagement posts for context")
print(f"  4. Document patterns in your preliminary findings")
print("\n" + "="*60)