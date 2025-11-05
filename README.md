## Overview

This repository contains code, methodology documentation, and anonymized results from exploratory mixed-methods research investigating the disconnect between digital wellness interventions and care workers' actual stress-coping practices.

### Research Question

How do care workers articulate their needs and coping strategies in online discourse, and why are wellness-focused digital interventions largely absent from these discussions?

### Key Finding

Despite being deeply embedded in technology (the term "app" appeared 460 times), wellness apps were mentioned in only 6 of 364 analyzed posts (1.6%)—a ratio of 51:1. Care workers instead discussed economic exit strategies (31.3%), peer support (30.2%), and structural workplace stressors (financial stress: 45.3%; scheduling issues: 43.7%).

## Repository Structure
```
care-worker-digital-wellbeing-preliminary/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                      # Template for API credentials
├── .gitignore                        # Excludes sensitive files
│
├── code/
│   ├── 01_collect_reddit_posts.py    # Data collection from r/CNA
│   ├── 02_thematic_coding.py         # Automated thematic analysis
│   └── 03_deep_dive_search.py        # Stress & mental health patterns
│
├── documentation/
│   ├── methodology.md                # Detailed research methodology
│   ├── ethical_considerations.md     # Privacy & ethics protocols
│   └── setup_guide.md                # Installation instructions
│
├── outputs/                          # Aggregated results (no raw data)
│   ├── summary_statistics.md         # Key findings summary
│   └── pattern_analysis.md           # Identified patterns
│
└── data/                             # Raw data (NOT in repository)
    └── .gitkeep                      # Placeholder only
```

## Dataset

**Source:** r/CNA (Certified Nursing Assistants subreddit, ~18,000 members)  
**Collection Period:** Posts from 2022-2024  
**Sample Size:** 364 themed posts (filtered for relevance to work stress, technology, coping)  
**Collection Method:** Reddit API (PRAW) with ethical protocols

### Data Availability

Raw data files are **not included** in this repository to protect user privacy, even though posts are publicly available. Only aggregated, anonymized results are shared.

## Methodology

### Mixed-Methods Approach

**1. Ethnographic Observation**
- 17 months volunteering at long-term care facility (May 2024 - present)
- Documented technology use patterns among CNAs
- Contextual understanding of work environment and stressors

**2. Computational Discourse Analysis**
- Keyword-based categorization across 8 thematic categories
- Frequency analysis of technology, stress, and coping terms
- Pattern identification and co-occurrence analysis
- Manual validation of automated classifications

**3. Synthesis**
- Triangulation of ethnographic and computational findings
- Comparison of private behavior (apps on phones) vs. public discourse (what's discussed online)

See [`documentation/methodology.md`](documentation/methodology.md) for complete details.

## Key Findings

### Technology Use Patterns

| Metric | Count | Percentage |
|--------|-------|------------|
| "App" mentions (general) | 460 | N/A |
| Wellness app mentions | 6 posts | 1.6% |
| **Ratio** | **51:1** | |

### Coping Strategies Discussed

| Strategy | Posts | Percentage |
|----------|-------|------------|
| Economic exit (job searching/quitting) | 114 | 31.3% |
| Peer support seeking | 110 | 30.2% |
| Personal strategies (exercise/hobbies) | 68 | 18.7% |
| Professional help (therapy/counseling) | 21 | 5.8% |
| **Wellness apps** | **6** | **1.6%** |

### Structural Stressors

| Stressor | Posts | Percentage |
|----------|-------|------------|
| Financial stress / low wages | 165 | 45.3% |
| Scheduling issues | 159 | 43.7% |
| Stress (general discussion) | 30 | 8.2% |
| Mental health conditions | 37 | 10.2% |

### Keyword Frequencies

- "Support": 303 mentions
- "Quit/Leave": 204 mentions
- "Apps" (general): 460 mentions
- "Wellness apps" (Calm, Headspace, etc.): 9 mentions

## Installation & Usage

### Prerequisites

- Python 3.8+
- Reddit account with API credentials
- pip package manager

### Quick Setup

1. **Clone repository:**
```bash
   git clone https://github.com/GladysDalla/Preliminary_work.git
   cd Preliminary_work
```

2. **Create virtual environment:**
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

4. **Set up credentials:**
   - Copy `.env.example` to `.env`
   - Add your Reddit API credentials to `.env`
   - See [Setup Guide](documentation/setup_guide.md) for details

5. **Run analysis:**
```# Collect data
python code/01_collect_reddit_posts.py

# Run thematic coding
python code/02_thematic_coding.py

# Analyze stress patterns
python code/03_deep_dive_search.py
```

## Ethical Considerations

This research follows established protocols for internet research:

✓ **Public data only** - No password-protected or private content  
✓ **No usernames retained** - All identifying information removed  
✓ **Anonymized quotes** - No direct links or identifying details in outputs  
✓ **Aggregate statistics only** - Individual posts not published  
✓ **IRB guidelines** - Follows AoIR ethics framework  

See [`documentation/ethical_considerations.md`](documentation/ethical_considerations.md) for complete protocols.

## Limitations

- Analysis limited to English-language posts
- Sample represents Reddit users only (selection bias)
- Cannot verify demographic claims in posts
- Exploratory analysis only - not definitive findings
- Single platform (r/CNA) - may not generalize to all care workers

## Research Implications

These preliminary findings informed dissertation research design:

1. **Cannot assume wellness apps are appropriate interventions** - Must investigate what workers actually need vs. what's prescribed for them

2. **Economic precarity must be centered** - Technology that ignores material conditions risks same irrelevance as wellness apps

3. **Peer support is existing infrastructure** - Interventions should amplify, not replace, community coping

4. **Co-design is epistemologically necessary** - Gap between external prescriptions and lived reality requires worker voice throughout

## Future Work

This preliminary analysis informs two dissertation projects:

**Project 1:** Expanded multi-platform analysis with theoretical grounding in care work scholarship, labor studies, and community psychology

**Project 2:** Participatory co-design of digital interventions that respect workers' actual coping ecologies rather than imposing individual wellness solutions

## Dependencies

See `requirements.txt` for complete list. Key packages:
```
praw==7.7.1                # Reddit API wrapper
pandas==2.1.0              # Data manipulation
openpyxl==3.1.2           # Excel file handling
python-dotenv==1.0.0      # Environment variable management
```

## Citation

If you use or reference this work, please cite:
```
[Gladys Dalla]. (2024). Care Worker Digital Wellbeing: Preliminary Exploration. 
GitHub repository: https://github.com/[GladysDalla]/Preliminary_work
```

## License

MIT License - See LICENSE file for details
```
## Acknowledgments

- r/CNA community for publicly sharing their experiences
- Hawthorne Lane House for hosting volunteer work
- Reddit API for data access
- UW-Milwaukee Information Science program for methodological training

---

**Note:** This is preliminary exploratory work conducted for PhD applications. Formal dissertation research will expand scope, deepen theoretical engagement, and include direct worker participation through interviews and co-design.
---
