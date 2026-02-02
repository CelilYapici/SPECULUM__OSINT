SPECULUM — Quick Setup and Running Guide

This project is a `Streamlit`-based OSINT (Open Source Intelligence) tool. Below are the basic steps to run it on your local machine.

## 1. Python and pip
- On macOS, use the `python3` command (your system may not have `python`).

## 2. Virtual Environment (recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Python Dependencies
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## 4. Optional: CLI OSINT Tools

The application supports the following CLI tools **optionally**:

- **Sherlock**: Username-based account search (120+ platforms)
  ```bash
  python3 -m pip install sherlock
  # After installation, the "Sherlock Scan" option will be active in the UI
  ```

- **theHarvester**: Domain/email domain data gathering
  ```bash
  python3 -m pip install theHarvester
  ```

- **SpiderFoot**: Comprehensive OSINT scanning (emails, domains, IPs, etc.)
  ```bash
  python3 -m pip install spiderfoot
  # Alternative: Docker or source code installation
  ```

- **Holehe**: Email-based deep account scanning
  ```bash
  python3 -m pip install holehe
  ```

**Notes:**
- Installing these tools is entirely optional.
- If not installed/selected, the application will automatically skip them or display an info message.
- When a user selects a scan option in the UI, the app automatically checks if that CLI tool is installed.

## 5. Running the Application
```bash
python3 -m streamlit run main.py
```

Your browser will automatically open to `http://localhost:8501`.

## 6. Deploy to Streamlit Cloud (Optional)

To share this application on the internet, deploy it to **Streamlit Cloud** (free):

### Steps:
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click **"Create app"**
4. Fill in:
   - **Repository:** `CelilYapici/SPECULUM__OSINT`
   - **Branch:** `main`
   - **Main file path:** `main.py`
5. Click **Deploy**

### Result:
After deployment, you'll get a public URL like:
```
https://speculumosint.streamlit.app
```

Share this link with anyone — they can access your OSINT tool from their browser without installing anything!

**⚠️ Note on Streamlit Cloud:**
- Basic scans work: **Gravatar, GitHub, Google Search**
- Limited scans: **Holehe Deep Scan, Sherlock** (depends on external API availability)
- CLI tools do NOT work on Streamlit Cloud (environment restrictions): theHarvester, SpiderFoot
- For full functionality with CLI tools, use local installation or a VPS

---

## 7. Important Notes
- Do NOT run `main.py` directly with `python main.py` — Streamlit context will not be created.
- CLI tools must be available in the system PATH (the app will automatically check if they are installed via `pip install`).
- If you encounter any issues or errors, check the terminal output for diagnostics.
- On **Streamlit Cloud**, optional CLI tools (Sherlock, theHarvester, SpiderFoot) may not work due to environment restrictions. Basic scans (Gravatar, GitHub, Google) will still work.

---

## Quick Usage:
1. After the home page loads, enter the target's **Full Name** and/or **Email Address**.
2. Check the scan options you want (Deep Scan, Sherlock, theHarvester, etc.).
3. Click the **START ANALYSIS** button.
4. Results will automatically appear on the screen.

## Project Structure
```
speculum/
├── main.py                # Application entry point (Orchestrator)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── src/
    ├── backend/          # Processing logic
    │   ├── __init__.py
    │   └── engine.py     # SpeculumEngine class with all scan functions
    └── frontend/         # User interface
        ├── __init__.py
        └── ui.py         # SpeculumUI class for design and forms
```

## Features
- **Gravatar Scan**: Check for profile images linked to an email
- **GitHub Scan**: Search for matching GitHub usernames
- **Holehe Deep Scan**: Search 120+ platforms for email-based accounts
- **Google Search**: Full-name based search results
- **Sherlock**: Multi-platform username search
- **theHarvester**: Domain/email intelligence gathering
- **SpiderFoot**: Comprehensive OSINT intelligence gathering

---

For questions or issues, feel free to ask for help!