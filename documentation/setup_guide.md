# Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Reddit account with API credentials

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/GladysDalla/Preliminary_work.git
cd Preliminary_work
```

### 2. Create Virtual Environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app"
3. Choose "script" as the app type
4. Give it a name (e.g., "care-worker-research")
5. Set redirect URI to: `http://localhost:8080`
6. Copy your `client_id` (under app name) and `client_secret`

### 5. Create `.env` File

Edit `.env` with your actual credentials:
```
REDDIT_CLIENT_ID=your_actual_client_id
REDDIT_CLIENT_SECRET=your_actual_client_secret
REDDIT_USER_AGENT=academic_research_care_workers_v1.0
```

**Important:** Never commit `.env` to GitHub! It's already in `.gitignore`.

### 6. Run Data Collection
```bash
python code/collect_cna_posts.py
```

## Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

## Troubleshooting

**"Command 'python' not found"**
- Try `python3` instead of `python`

**"Module not found" errors**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**"Invalid credentials" error**
- Check your `.env` file has correct credentials
- Verify no extra spaces around `=` signs
- Make sure you copied the full client_secret (it's long)

**Virtual environment activation not working on Windows PowerShell**
- You may need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then try activating again

## Security Notes

- `.env` file contains sensitive credentials and must never be committed
- `venv/` folder is excluded from git (in `.gitignore`)
- Raw data files are excluded for privacy protection
- Only aggregated, anonymized results should be shared