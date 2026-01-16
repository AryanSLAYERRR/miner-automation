from playwright.sync_api import sync_playwright
import time
from  gmailcoder import get_verification_code, clear_login_emails # Make sure this is in same folder
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import logging
from datetime import datetime


num_tabs = 5 #mining tabs number

email_address = "your_email"

SCOPES = ['https://mail.google.com/']
dirnav = "cd /home/project"
with open("command.txt", "r") as f:
    command_to_paste = f.read().strip()


logging.basicConfig(
    filename="mining_log.txt",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

    
def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES) #checks if token.json already exists
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def keep_tab_alive(page): #keeps the site alive, avoiding timeout for running long sessions
    page.evaluate("""
        if (!window.keepAliveInterval) {
            window.keepAliveInterval = setInterval(() => {
                const textarea = document.querySelector('textarea.xterm-helper-textarea');
                if (textarea) {
                    textarea.focus();
                    const event = new Event('input', { bubbles: true });
                    textarea.dispatchEvent(event);
                }
                window.scrollBy(0, 1);  // simulate slight movement
                window.scrollBy(0, -1);
            }, 80000); // every 2 minutes
        }
    """)
    logging.info("✅ Safe JS-based keep-alive injected (no T key, no interference).")


def open_and_mine(page): # simulates the miner setup 
    # Wait for chat input
    page.wait_for_selector("textarea", timeout=15000)
    page.fill("textarea", "Just say 1 word nothing else") # preserves tokens by limiting response
    page.keyboard.press("Enter")
    #--------------------------------------
    page.locator('button:has(svg.lucide.lucide-chevrons-left)')
    page.click('button:has(svg.lucide.lucide-chevrons-left)')
    #--------------------------------------
    page.wait_for_selector("text=Terminal", timeout=5000)
    page.click("text=Terminal")
    time.sleep(1)

   #page.evaluate("document.querySelector('textarea.xterm-helper-textarea').scrollIntoView()")

    page.wait_for_timeout(1000)   
    page.evaluate("document.querySelector('textarea.xterm-helper-textarea').scrollIntoView()")
    page.wait_for_timeout(1000)
    page.evaluate("document.querySelector('textarea.xterm-helper-textarea').focus()")

    #----------------------------------------------------------------------------
    
    page.keyboard.press('Enter')
    page.keyboard.press("Enter")
    time.sleep(3)
    page.type("textarea.xterm-helper-textarea", dirnav)
    page.keyboard.press('Enter')
    time.sleep(1)
    page.fill("textarea.xterm-helper-textarea", command_to_paste)  # direct paste
    #--------------------------------------
    page.locator("textarea.xterm-helper-textarea").dispatch_event("input")
    time.sleep(1)
    page.keyboard.press("Enter")
    
    keep_tab_alive(page)

def duplicate_and_mine(page): # for other tabs 
    
    page.locator('button:has(svg.lucide.lucide-chevrons-left)')
    page.click('button:has(svg.lucide.lucide-chevrons-left)')
    page.wait_for_selector("text=Terminal", timeout=5000)
    page.click("text=Terminal")
    time.sleep(1)
    page.evaluate("document.querySelector('textarea.xterm-helper-textarea').scrollIntoView()")
    page.wait_for_timeout(1000)
    page.evaluate("document.querySelector('textarea.xterm-helper-textarea').focus()")

    #--------------------------------------
    page.keyboard.press('Enter')
    page.keyboard.press("Enter")
    time.sleep(3)
    page.fill("textarea.xterm-helper-textarea", command_to_paste)  # direct paste
    page.locator("textarea.xterm-helper-textarea").dispatch_event("input")
    time.sleep(1)
    page.keyboard.press("Enter")

    keep_tab_alive(page)
       
def automate_mining(): # functions that handels logging in and calling the mining function
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        service = get_gmail_service()
        clear_login_emails(service) #deleting emails of previous one-time codes

        page.goto("")
        time.sleep(0.5)
        #--------------------------------------
        page.fill('input[type="email"]', email_address)
        page.click("button:has-text('Continue')")

        code = get_verification_code()
        if not code:
            logging.error("❌ No code retrieved. Aborting login.")
            return
        
        assert len(code) == 6, "Login code must be 6 digits"

        page.wait_for_selector('input[data-test="otp-input"]', timeout=10000)

        for i, digit in enumerate(code):
            otp_input = page.locator(f'input[data-index="{i}"]')
            otp_input.click()  # focuses the box
            page.keyboard.type(digit, delay=100)  #otp typer
            

        time.sleep(5)

        #--------------------------------------
        open_and_mine(page)

        current_url = page.url
        logging.info(f"Current chat URL: {current_url}")

        for i in range(1, num_tabs):
            new_page = page.context.new_page()
            new_page.goto(current_url)
            duplicate_and_mine(new_page)
            logging.info(f"✅ Tab {i+1}/{num_tabs} running")

        logging.info(f"🚀 {num_tabs} mining tabs running.")
        input("Press Enter to close...")
        browser.close()

if __name__ == "__main__":
    automate_mining()

