<h1 align="center">🛠 Miner Automation</h1>
<p align="center">
Automated browser-based Monero mining using Playwright and Gmail OTP login — use at your own risk.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg">
  <img src="https://img.shields.io/badge/Playwright-Driven-lightgrey.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
</p>

---

##  Disclaimer

**This project is for educational purposes only.**  
The developer is not responsible for any misuse, consequences, damage, or terms violations resulting from its use. **Use at your own risk.**  
*If you're curious how it works, feel free to contact me on Instagram rather than relying on this README.*  

---

##  Overview

Miner Automation streamlines browser-based Monero mining by:

- Using Playwright for automated browser control.
- Logging in via Gmail OTP (through Gmail API).
- Opening multiple tabs to mine with a safe JavaScript keep-alive script.
- Delivering notable hash rates (~700–800 H/s per tab).
- Injecting commands and cleaning inbox emails.
- Designed around XMRig CC from Bendr0id.

> **Paused:** Mining functionality currently doesn't work. A workaround is in progress.

---

##  Features

- **Auto-login** using Gmail OTP (via Gmail API).
- **Multi‑tab mining** (configurable count).
- **Safe keep-alive** with JS: scrolling, focusing, input events.
- **Terminal command injection** via browser UI.
- **Gmail cleanup** to manage inbox clutter.
- Approx. **700–800 H/s per tab**, depending on resources.
- **Planned enhancements**: inactivity detection, config optimization, improved hashrates.

---

##  Requirements

- **Python 3.10+**
- **Playwright**
- **Gmail API credentials** (`credentials.json`)
- Google API packages:
  ```bash
  pip install --upgrade google-api-python-client                    google-auth-httplib2                    google-auth-oauthlib
  ```
- **Playwright browser binaries** (via `playwright install`).

---

##  Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/AryanSLAYERRR/miner-automation.git
   cd miner-automation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. **Set up Gmail API** (gives the script access to your Gmail — use an alternate/test account recommended):
   - Go to Google Cloud Console → Create a new project.
   - Enable the **Gmail API**.
   - Create **OAuth 2.0 credentials** (set type = Desktop app).
   - Download and rename file to `credentials.json`, placing it in the project root.

4. **Configure command and credentials**:
   - Edit `command.txt` and paste your mining command, including your Monero wallet address.
   - In `main.py`, set `"your_email"` to match the one used for the Gmail API.

---

##  Usage

```bash
python gmailcode.py
```

- You’ll be prompted to authorize via a browser.
- If you encounter access errors, update your Google Cloud project's OAuth consent screen:
  - Add your testing email under **API & Services → OAuth consent → Test Users**.
  - Retry.
- On success, you'll receive a `token.json` file.

Then run:

```bash
python main.py
```

- Chrome should launch via Playwright, performing mining automation.

**Optional config**: adjust `num_tabs` for parallel mining — avoid exceeding ~90% RAM to prevent system instability.

Monitor progress on [Nanopool](https://nanopool.org) by searching your wallet address.

---

##  Keep-Alive Mechanism

To keep terminal sessions alive without pushing keystrokes, the injected JS:

- Scrolls the page slightly up and down.
- Focuses on the hidden input.
- Dispatches an `input` event.

---

##  Project Structure

```
miner-automation/
├── gmailcode.py        # Gmail OTP handler
├── main.py             # Core automation logic
├── command.txt         # Mining command with wallet info
├── credentials.json    # Downloaded Google OAuth credentials
├── token.json          # Generated after Gmail authorization
├── requirements.txt
├── .gitignore
└── README.md
```

---

##  Security Notes

- Your Gmail credentials (credentials.json, token.json) are stored locally.  
- **Never share them.**  
- Avoid using accounts with 2FA unless using app passwords.

---

##  License

MIT License © 2025 AryanSLAYERRR  
Permission is granted, free of charge, to use, copy, modify, or distribute this software under the terms of the license.

---

##  About

A browser‑based Monero mining tool showcasing Playwright automation and Gmail OTP integration.

---

<p align="center">✨ Made with automation and a touch of caution ✨</p>
