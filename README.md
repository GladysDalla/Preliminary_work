# Preliminary_work
Preliminary exploratory analysis of care worker discourse on digital mental health tool. PhD application research in HCI.

# Care Worker Digital Wellbeing: Preliminary Exploration

**Author:** [Gladys Dalla]  
**Institution:** University of Wisconsin-Milwaukee  
**Purpose:** Preliminary research for PhD applications in Human-Computer Interaction

## Overview

This repository contains code and documentation for exploratory analysis of care worker discourse on digital mental health tools. This work is preliminary research conducted to inform doctoral dissertation design.

## Research Questions

1. How do care workers articulate their needs and challenges with digital wellness tools online?
2. What patterns emerge in their technology use and information-seeking behaviors?

## Methodology

### Data Collection
- **Source:** Public posts from r/CNA (Reddit)
- **Time Period:** 2022-2024
- **Collection Method:** Reddit API (PRAW)
- **Sample Size:** ~XXX posts (to be updated after collection)

### Analysis Approach
- **Quantitative:** Word frequency analysis of technology, wellness, and work-related terms
- **Qualitative:** Thematic coding of 100-120 high-engagement posts
- **Ethical Protocol:** 
  - Only publicly available data
  - All quotes anonymized (no usernames, identifying details removed)
  - Follows r/CNA community guidelines
  - IRB exemption expected (publicly available data, no identifiers retained)

## Key Findings

*[To be updated after analysis]*

## Repository Structure

- `code/` - Python scripts for data collection and analysis
- `analysis/` - Templates and documentation for thematic coding
- `outputs/` - Aggregated, anonymized results
- `documentation/` - Detailed methodology and ethical considerations

## Ethical Considerations

This research:
- Uses only publicly accessible data
- Does not collect or retain usernames or identifying information
- Anonymizes all quotes before inclusion in research outputs
- Respects Reddit's API terms of service and community guidelines
- Follows established ethical protocols for digital ethnography

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
```bash
   python code/collect_cna_posts.py
```

### Environment Management

Always activate the virtual environment before running scripts:
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

Deactivate when done:
```bash
deactivate
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

---
