# Research Methodology

## Overview

This preliminary research employed a convergent mixed-methods design combining ethnographic observation with computational discourse analysis to understand the disconnect between digital wellness interventions and care workers' actual stress-coping practices.

## Research Design

### Paradigm

**Pragmatic mixed-methods approach:**
- Ethnography for contextual understanding and lived experience
- Computational analysis for pattern identification at scale
- Synthesis for comprehensive insight

### Rationale

Care workers' technology use operates at multiple levels:
- **Private behavior:** What apps are on their phones (compliance with external expectations)
- **Public discourse:** What they discuss with peers (actual coping practices)

Single-method research would miss this disconnect. Mixed methods reveals the gap between prescribed and actual coping.

## Method 1: Ethnographic Observation

### Setting

Hawthorne Lane House, a long-term care facility in Wisconsin

### Duration

17 months (May 2024 - November 2024)

### Role

Volunteer working alongside CNAs in various capacities

### Data Collection

**Informal observations:**
- Technology use during breaks and shifts
- Conversations about stress management
- Discussions of wellness resources and apps
- Actual vs. reported technology practices

**Documentation:**
- Field notes recorded after shifts
- Patterns across multiple CNAs (N=8+ observed)
- Representative quotes (anonymized immediately)
- Contextual details about work environment

### Analysis

Thematic analysis of field notes identifying recurring patterns:
1. Wellness apps present but unused ("compliance artifacts")
2. Active technology use: scheduling, job search, peer communication
3. Barriers to app use: exhaustion, lack of time, economic stress

## Method 2: Computational Discourse Analysis

### Platform Selection

**r/CNA (Reddit):**
- ~18,000 members (active community)
- Public posts (ethical access)
- Peer-to-peer discourse (authentic voice)
- Temporal depth (posts from 2022-2024)

**Why Reddit:**
- Naturalistic data (not elicited by researchers)
- Anonymous platform (encourages honesty)
- Asynchronous (workers post when able)
- Community validation (upvotes show resonance)

### Sampling Strategy

**Initial Collection:**
- Top posts (historical popularity)
- Recent posts (current discourse)
- Time filter: 2022-2024 (3-year window)
- Total collected: 734 substantive posts

**Themed Filtering:**
- Keywords: stress, app, burnout, quit, wage, schedule, tired, overwhelmed
- Resulted in: 364 posts for detailed analysis
- Rationale: Focus on posts most relevant to research questions

### Data Collection Tool

**PRAW (Python Reddit API Wrapper)**
- Official Reddit API access
- Rate-limit compliant
- Metadata captured: title, text, score, comments, date, ID

**Data Stored:**
```python
{
    'id': unique_identifier,
    'title': post_title,
    'text': post_body,
    'score': upvotes - downvotes,
    'num_comments': comment_count,
    'created_date': timestamp,
    'year': year_posted
}
```

### Analysis Approach

**Phase 1: Automated Categorization**

Keyword-based classification across 8 categories:
1. Wellness app mentioned
2. Wellness app abandoned
3. Job search technology
4. Scheduling issues
5. Pay/financial stress
6. Burnout/exhaustion
7. Peer support seeking
8. Employer program mentioned

**Keyword Selection Rationale:**
- Wellness apps: Specific app names (Calm, Headspace) + generic terms (meditation app, therapy app)
- Job search: Indeed, application, resume, interview
- Economic terms: Pay, wage, afford, broke, underpaid
- Stress terms: Stress, burnout, exhausted, drained, anxiety
- Support terms: Support, help, advice, "does anyone else"

**Algorithm:**
```python
for keyword in category_keywords:
    if keyword in post_text_lowercase:
        flag_post_for_category = True
```

Conservative approach: Flags posts for manual review rather than final classification

**Phase 2: Frequency Analysis**

Counted occurrences of key terms across full dataset:
- App (general): 460 mentions
- Wellness apps: 9 mentions
- Support: 303 mentions
- Quit/Leave: 204 mentions
- Stress: 58 mentions
- Anxiety: 33 mentions

**Phase 3: Pattern Identification**

Calculated:
- Category frequencies (% of posts)
- Co-occurrence patterns (what themes appear together)
- Ratios (e.g., job search : wellness apps = 18:1)
- Engagement metrics (scores + comments for validation)

**Phase 4: Manual Validation**

Researcher reviewed:
- All posts flagged as high-priority (~112 posts)
- All wellness app mentions (6 posts)
- Random sample of 50 additional posts for false negative check

## Synthesis

### Triangulation

Compared ethnographic findings with computational patterns:

| Finding | Ethnographic Evidence | Computational Evidence |
|---------|----------------------|------------------------|
| Wellness apps present but unused | 8 CNAs showed apps, reported no usage | Only 1.6% of posts mention wellness apps |
| Job search as primary tech use | Indeed usage during breaks observed | 31.3% of posts discuss job searching |
| Peer support valued | Coworker texting/venting observed | 30.2% posts seek community validation |
| Economic stress central | Direct quotes about wages | 45.3% posts mention financial stress |

**Convergence:** Both methods revealed same pattern—wellness apps irrelevant to actual coping

**Divergence:** Ethnography captured private behavior (apps on phones); discourse analysis captured public conversation (what's discussed)

**Explanation:** Workers carry apps to satisfy external expectations but don't find them relevant enough to discuss with peers

### Analytical Framework

**Descriptive level:** What patterns exist?
- Frequencies, ratios, categories

**Interpretive level:** What do patterns mean?
- Wellness apps as "compliance artifacts"
- Economic exit as rational coping
- Peer support as primary resource

**Critical level:** Why do patterns exist?
- Structural stressors (low wages, understaffing) vs. individual interventions
- Mismatch between what's prescribed and what's needed
- Technology designed for different user populations (discretionary time, stable income)

## Validity & Reliability

### Credibility

- **Prolonged engagement:** 17 months ethnographic observation
- **Triangulation:** Multiple methods, data sources
- **Member checking:** Shared findings with 3 CNAs for validation
- **Thick description:** Rich contextual detail provided

### Transferability

- **Detailed context:** Care work setting, population characteristics
- **Limitations stated:** Reddit users, English-language, single facility
- **Theory connection:** Findings related to broader care work literature

### Dependability

- **Audit trail:** Code, data, analysis steps documented
- **Reproducibility:** Scripts shared publicly, methods transparent
- **Decision documentation:** Analytical choices explained

### Confirmability

- **Reflexivity:** Positionality addressed (outsider to care work)
- **Raw data available:** Can be audited (with privacy protections)
- **Alternative explanations considered:** Negative cases sought

## Ethical Protocols

### Reddit Data

- **Public posts only:** No private messages or restricted subreddits
- **No usernames retained:** Identifying information stripped immediately
- **Anonymized quotes:** Details removed or generalized
- **No direct links published:** Cannot trace back to original posts
- **AoIR guidelines followed:** Association of Internet Researchers ethics framework

### Ethnographic Data

- **Informed consent:** CNAs aware of research role (general, not specific to conversations)
- **Anonymization:** All names, facility details removed
- **Confidentiality:** Field notes stored securely
- **No vulnerable moments:** Did not observe/record during patient care

### IRB Status

Preliminary exploratory work for PhD applications. Formal IRB approval will be sought for dissertation research.

Current work anticipated to be exempt (publicly available data, no identifiers retained), but not submitted for review as preliminary/pilot study.

## Limitations

1. **Sample bias:** Reddit users may differ from non-users
2. **Platform effects:** Reddit culture may shape discourse
3. **Self-report:** Cannot verify claims in posts
4. **Temporal:** Snapshot of 2022-2024 only
5. **Single facility:** Ethnography limited to one site
6. **Language:** English-only posts
7. **Researcher positionality:** Outsider to care work may miss insider meanings

## Future Directions

Dissertation research will address limitations through:
- **Multi-platform analysis:** Reddit + other forums + Indeed reviews
- **Direct interviews:** Worker voices beyond online discourse
- **Comparative analysis:** Hospital vs. home health vs. nursing home contexts
- **Theoretical grounding:** Care work theory, labor studies, community psychology
- **IRB approval:** Formal ethical review for dissertation studies

---

**Last Updated:** November 2024