import pandas as pd
import re
from collections import Counter

print("="*60)
print("DEEP DIVE: STRESS & MENTAL HEALTH DISCOURSE")
print("="*60)

# ============================================
# LOAD DATA
# ============================================
print("\n1. Loading data...")
df = pd.read_excel('themed_posts_for_analysis.xlsx')
print(f"   Loaded {len(df)} themed posts")

df['full_text'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
df['full_text_lower'] = df['full_text'].str.lower()

# ============================================
# DEFINE SEARCH PATTERNS
# ============================================

search_patterns = {
    'stress_general': {
        'keywords': ['stress', 'stressed', 'stressful', 'stress out', 'so stressed'],
        'description': 'General stress mentions'
    },
    'mental_health_explicit': {
        'keywords': ['mental health', 'mental illness', 'therapy', 'therapist', 
                     'counseling', 'counselor', 'psychiatrist', 'medication',
                     'antidepressant', 'anxiety medication'],
        'description': 'Explicit mental health / professional help'
    },
    'mental_health_conditions': {
        'keywords': ['depression', 'depressed', 'anxiety', 'anxious', 'panic attack',
                     'ptsd', 'trauma', 'suicidal', 'mental breakdown'],
        'description': 'Mental health conditions mentioned'
    },
    'emotional_exhaustion': {
        'keywords': ['exhausted', 'drained', 'can\'t do this', 'breaking down',
                     'falling apart', 'losing it', 'at my limit', 'can\'t take it'],
        'description': 'Emotional/psychological exhaustion'
    },
    'physical_symptoms': {
        'keywords': ['can\'t sleep', 'insomnia', 'nightmares', 'crying',
                     'panic', 'shaking', 'heart racing', 'nausea'],
        'description': 'Physical manifestations of stress'
    },
    'coping_mentioned': {
        'keywords': ['cope', 'coping', 'deal with', 'handle', 'manage',
                     'get through', 'survive', 'make it through'],
        'description': 'Discussing coping strategies'
    },
    'self_care_language': {
        'keywords': ['self care', 'self-care', 'take care of myself', 
                     'need to relax', 'need a break', 'time for myself'],
        'description': 'Self-care language (not app-specific)'
    },
    'social_support': {
        'keywords': ['talk to', 'vent', 'rant', 'need to talk', 'listening',
                     'support', 'relate', 'same', 'me too', 'you\'re not alone'],
        'description': 'Social support seeking/giving'
    },
    'substance_coping': {
        'keywords': ['drink', 'drinking', 'alcohol', 'wine', 'beer', 'weed', 
                     'marijuana', 'smoke', 'vape'],
        'description': 'Substance use as coping'
    },
    'exercise_hobbies': {
        'keywords': ['exercise', 'workout', 'gym', 'run', 'running', 'walk',
                     'yoga', 'hobby', 'hobbies', 'netflix', 'music', 'reading'],
        'description': 'Exercise and hobbies as coping'
    },
    'leave_quit': {
        'keywords': ['quit', 'quitting', 'leave', 'leaving', 'resign',
                     'last day', 'walked out', 'new job', 'better job'],
        'description': 'Leaving as stress response'
    },
    'no_solution': {
        'keywords': ['nothing helps', 'tried everything', 'no point',
                     'what\'s the point', 'hopeless', 'giving up'],
        'description': 'Expressions of hopelessness'
    }
}

# ============================================
# SEARCH AND CATEGORIZE
# ============================================
print("\n2. Searching for stress & mental health patterns...")

results = {}

for pattern_name, pattern_info in search_patterns.items():
    df[pattern_name] = False
    
    for keyword in pattern_info['keywords']:
        mask = df['full_text_lower'].str.contains(keyword, na=False, regex=False)
        df.loc[mask, pattern_name] = True
    
    count = df[pattern_name].sum()
    percentage = (count / len(df)) * 100
    results[pattern_name] = {
        'count': count,
        'percentage': percentage,
        'description': pattern_info['description']
    }
    print(f"   {pattern_name}: {count} ({percentage:.1f}%)")

# ============================================
# ANALYZE CO-OCCURRENCE
# ============================================
print("\n3. Analyzing what stress discourse co-occurs with...")

stress_posts = df[df['stress_general'] == True].copy()
print(f"\n   Found {len(stress_posts)} posts mentioning 'stress'")

if len(stress_posts) > 0:
    print("\n   What do stress-mentioning posts also discuss?")
    
    co_occurrence = {}
    for pattern_name in search_patterns.keys():
        if pattern_name != 'stress_general':
            co_count = stress_posts[pattern_name].sum()
            co_pct = (co_count / len(stress_posts)) * 100 if len(stress_posts) > 0 else 0
            co_occurrence[pattern_name] = {
                'count': co_count,
                'percentage': co_pct
            }
            if co_count > 0:
                print(f"      {pattern_name}: {co_count} ({co_pct:.1f}%)")
    
    # Sort by frequency
    sorted_co = sorted(co_occurrence.items(), key=lambda x: x[1]['count'], reverse=True)
    
    print("\n   Top co-occurring themes with stress:")
    for pattern, data in sorted_co[:5]:
        if data['count'] > 0:
            print(f"      {pattern}: {data['count']} posts")

# ============================================
# WHAT DO THEY DO ABOUT STRESS?
# ============================================
print("\n4. What coping strategies are mentioned?")

coping_categories = ['coping_mentioned', 'social_support', 'substance_coping', 
                    'exercise_hobbies', 'leave_quit', 'mental_health_explicit']

coping_data = []
for cat in coping_categories:
    count = df[cat].sum()
    pct = (count / len(df)) * 100
    coping_data.append({'strategy': cat, 'count': count, 'percentage': pct})

coping_df = pd.DataFrame(coping_data).sort_values('count', ascending=False)
print("\n   Coping strategies by frequency:")
for _, row in coping_df.iterrows():
    if row['count'] > 0:
        print(f"      {row['strategy']}: {row['count']} ({row['percentage']:.1f}%)")

# ============================================
# EXTRACT QUOTES
# ============================================
print("\n5. Extracting quotes about stress and coping...")

def extract_context_quote(text, keywords, context_words=50):
    """Extract quote with context around keywords"""
    text_lower = text.lower()
    
    for keyword in keywords:
        idx = text_lower.find(keyword)
        if idx != -1:
            # Get surrounding context
            start = max(0, idx - context_words*5)
            end = min(len(text), idx + context_words*5)
            
            snippet = text[start:end].strip()
            
            # Clean up
            if start > 0:
                snippet = '...' + snippet
            if end < len(text):
                snippet = snippet + '...'
            
            # Try to get complete sentences
            sentences = re.split(r'[.!?]+', snippet)
            if len(sentences) >= 2:
                return '. '.join(sentences[1:-1]).strip()
            else:
                return snippet
    
    return None

quotes_collection = {
    'stress_and_coping': [],
    'mental_health': [],
    'peer_support': [],
    'leaving_quitting': [],
    'hopelessness': []
}

# Stress and coping
for idx, row in df[df['stress_general'] & df['coping_mentioned']].iterrows():
    quote = extract_context_quote(row['full_text'], ['stress', 'cope', 'deal with'])
    if quote and 50 < len(quote) < 300:
        quotes_collection['stress_and_coping'].append({
            'post_id': row['id'],
            'quote': quote,
            'engagement': row['score'] + row['num_comments']
        })

# Mental health
for idx, row in df[df['mental_health_explicit'] | df['mental_health_conditions']].iterrows():
    quote = extract_context_quote(row['full_text'], 
                                  ['mental health', 'therapy', 'depression', 'anxiety'])
    if quote and 50 < len(quote) < 300:
        quotes_collection['mental_health'].append({
            'post_id': row['id'],
            'quote': quote,
            'engagement': row['score'] + row['num_comments']
        })

# Peer support
for idx, row in df[df['social_support']].head(30).iterrows():
    quote = extract_context_quote(row['full_text'], 
                                  ['support', 'relate', 'you\'re not alone', 'me too'])
    if quote and 50 < len(quote) < 300:
        quotes_collection['peer_support'].append({
            'post_id': row['id'],
            'quote': quote,
            'engagement': row['score'] + row['num_comments']
        })

# Leaving/quitting
for idx, row in df[df['leave_quit']].head(30).iterrows():
    quote = extract_context_quote(row['full_text'], ['quit', 'leaving', 'last day'])
    if quote and 50 < len(quote) < 300:
        quotes_collection['leaving_quitting'].append({
            'post_id': row['id'],
            'quote': quote,
            'engagement': row['score'] + row['num_comments']
        })

# Hopelessness
for idx, row in df[df['no_solution']].iterrows():
    quote = extract_context_quote(row['full_text'], 
                                  ['nothing helps', 'hopeless', 'no point'])
    if quote and 50 < len(quote) < 300:
        quotes_collection['hopelessness'].append({
            'post_id': row['id'],
            'quote': quote,
            'engagement': row['score'] + row['num_comments']
        })

print(f"\n   Extracted quotes:")
for category, quotes in quotes_collection.items():
    print(f"      {category}: {len(quotes)} quotes")

# ============================================
# SAVE RESULTS
# ============================================
print("\n6. Saving detailed results...")

# Create comprehensive output
with pd.ExcelWriter('stress_mental_health_analysis.xlsx', engine='openpyxl') as writer:
    # Sheet 1: Summary statistics
    summary_data = []
    for pattern, data in results.items():
        summary_data.append({
            'Pattern': pattern,
            'Description': data['description'],
            'Count': data['count'],
            'Percentage': f"{data['percentage']:.1f}%"
        })
    summary_df = pd.DataFrame(summary_data).sort_values('Count', ascending=False)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Sheet 2: Coping strategies
    coping_df.to_excel(writer, sheet_name='Coping_Strategies', index=False)
    
    # Sheet 3: Stress posts
    stress_export = stress_posts[['id', 'title', 'text', 'score', 'num_comments',
                                  'coping_mentioned', 'social_support', 
                                  'mental_health_explicit', 'leave_quit']].copy()
    stress_export.to_excel(writer, sheet_name='Stress_Posts', index=False)
    
    # Sheet 4-8: Quote collections
    for category, quotes in quotes_collection.items():
        if len(quotes) > 0:
            quotes_df = pd.DataFrame(quotes)
            quotes_df = quotes_df.sort_values('engagement', ascending=False)
            quotes_df.to_excel(writer, sheet_name=f'Quotes_{category[:20]}', index=False)
    
    # Sheet 9: All coded posts
    export_cols = ['id', 'title', 'text', 'score', 'num_comments'] + list(search_patterns.keys())
    df[export_cols].to_excel(writer, sheet_name='All_Posts_Coded', index=False)

print(f"   ✓ Saved to: stress_mental_health_analysis.xlsx")

# ============================================
# KEYWORD FREQUENCY ANALYSIS
# ============================================
print("\n7. Analyzing specific keyword frequencies...")

# Count specific terms
term_counts = {}
important_terms = {
    'Stress terms': ['stress', 'stressed', 'stressful'],
    'Mental health': ['mental health', 'therapy', 'counseling'],
    'Depression': ['depression', 'depressed'],
    'Anxiety': ['anxiety', 'anxious'],
    'Burnout': ['burnout', 'burned out', 'burnt out'],
    'Exhaustion': ['exhausted', 'drained'],
    'Coping': ['cope', 'coping'],
    'Support': ['support', 'help'],
    'Quit/Leave': ['quit', 'quitting', 'leave', 'leaving'],
    'Apps general': ['app', 'apps', 'application'],
    'Wellness apps': ['calm', 'headspace', 'betterhelp', 'meditation app']
}

all_text = ' '.join(df['full_text_lower'].fillna(''))

print("\n   Keyword frequency counts:")
for category, terms in important_terms.items():
    total = 0
    for term in terms:
        count = all_text.count(term)
        total += count
    term_counts[category] = total
    print(f"      {category}: {total} mentions")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)

print(f"\nKey Findings:")
print(f"  • Stress mentioned: {results['stress_general']['count']} posts ({results['stress_general']['percentage']:.1f}%)")
print(f"  • Mental health explicit: {results['mental_health_explicit']['count']} posts ({results['mental_health_explicit']['percentage']:.1f}%)")
print(f"  • Emotional exhaustion: {results['emotional_exhaustion']['count']} posts ({results['emotional_exhaustion']['percentage']:.1f}%)")
print(f"  • Social support seeking: {results['social_support']['count']} posts ({results['social_support']['percentage']:.1f}%)")
print(f"  • Leaving/quitting: {results['leave_quit']['count']} posts ({results['leave_quit']['percentage']:.1f}%)")

print(f"\nComparison:")
print(f"  • Posts about stress/mental health: {results['stress_general']['count']}")
print(f"  • Posts mentioning wellness apps: 6")
print(f"  • Ratio: {results['stress_general']['count']/6:.1f}:1")

print(f"\nFiles created:")
print(f"  • stress_mental_health_analysis.xlsx - Full analysis")
print(f"  • Multiple quote collections by theme")

print("\n" + "="*60)