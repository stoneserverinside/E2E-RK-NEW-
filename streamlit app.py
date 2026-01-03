import streamlit as st
import time
import threading 
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import database as db 
import requests
import uuid
from datetime import datetime
import pytz

st.set_page_config(
    page_title="😊 STONE E2E TOOL",
    page_icon="🫶🏻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the UI
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background-image: url('https://i.postimg.cc/k5P9GPx3/Whats-App-Image-2025-11-07-at-10-18-13-958e0738.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .main-header h1 {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .prince-logo {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        margin-bottom: 15px;
        border: 2px solid #4ecdc4;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 8px;
        color: white;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        background: rgba(255, 255, 255, 0.2);
        border-color: #4ecdc4;
        box-shadow: 0 0 0 2px rgba(78, 205, 196, 0.2);
        color: white;
    }
    
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.06);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    }
    
    [data-testid="stMetricValue"] {
        color: #4ecdc4;
        font-weight: 700;
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
    }
    
    .console-section {
        margin-top: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        border: 1px solid rgba(78, 205, 196, 0.3);
    }
    
    .console-header {
        color: #4ecdc4;
        text-shadow: 0 0 10px rgba(78, 205, 196, 0.5);
        margin-bottom: 20px;
        font-weight: 600;
    }
    
    .console-output {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(78, 205, 196, 0.4);
        border-radius: 10px;
        padding: 12px;
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
        font-size: 12px;
        color: #00ff88;
        line-height: 1.6;
        max-height: 400px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: rgba(78, 205, 196, 0.5) rgba(0, 0, 0, 0.2);
    }
    
    .console-output::-webkit-scrollbar {
        width: 8px;
    }
    
    .console-output::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    
    .console-output::-webkit-scrollbar-thumb {
        background: rgba(78, 205, 196, 0.5);
        border-radius: 4px;
    }
    
    .console-output::-webkit-scrollbar-thumb:hover {
        background: rgba(78, 205, 196, 0.7);
    }
    
    .console-line {
        margin-bottom: 3px;
        word-wrap: break-word;
        padding: 6px 10px;
        padding-left: 28px;
        color: #00ff88;
        background: rgba(78, 205, 196, 0.08);
        border-left: 2px solid rgba(78, 205, 196, 0.4);
        position: relative;
    }
    
    .console-line::before {
        content: '►';
        position: absolute;
        left: 10px;
        opacity: 0.6;
        color: #4ecdc4;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        margin-top: 3rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'uploaded_cookies' not in st.session_state:
    st.session_state.uploaded_cookies = ""
if 'uploaded_messages' not in st.session_state:
    st.session_state.uploaded_messages = ""

# --- Generate Unique Task ID ---
def generate_task_id():
    return str(uuid.uuid4())[:8].upper()

class AutomationState:
    def __init__(self):
        self.running = False 
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# --- Logging Function ---
def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

# --- Automation Helper Functions --- 

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(5)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        'div[data-testid*="message-input" i]',
        'textarea[placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        element.click()
                        time.sleep(0.5)
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords) or idx < 10:
                            log_message(f'{process_id}: ✅ Found message input with selector #{idx+1}', automation_state)
                            return element
                except Exception:
                    continue
        except Exception:
            continue
    
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1280,720') 
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        log_message('Chrome browser setup completed successfully!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    
    return message

def send_messages(config, username, automation_state, user_id, task_id): 
    driver = None
    process_id = f"TASK-{task_id}" 
    
    # Outer Nonstop Loop: This loop runs the entire setup/sending process
    while db.get_task(task_id).get('is_running', False):
        try:
            log_message(f'{process_id}: Starting browser session...', automation_state)
            if driver:
                try: 
                    driver.quit() 
                except: 
                    pass
            driver = setup_browser(automation_state)
            
            # --- 2. Login/Navigate and Cookie Load ---
            driver.get('https://www.facebook.com/')
            time.sleep(5)
            
            if config.get('cookies') and config['cookies'].strip():
                log_message(f'{process_id}: Adding cookies...', automation_state)
                cookie_array = config['cookies'].split(';')
                for cookie in cookie_array:
                    cookie_trimmed = cookie.strip()
                    if cookie_trimmed:
                        first_equal_index = cookie_trimmed.find('=')
                        if first_equal_index > 0:
                            name = cookie_trimmed[:first_equal_index].strip()
                            value = cookie_trimmed[first_equal_index + 1:].strip()
                            try:
                                driver.add_cookie({
                                    'name': name,
                                    'value': value,
                                    'domain': '.facebook.com',
                                    'path': '/'
                                })
                            except Exception:
                                pass
            
            # --- 3. Open Chat ---
            chat_id = config.get('chat_id')
            if chat_id:
                chat_id = chat_id.strip()
                log_message(f'{process_id}: Navigating to conversation {chat_id}... (Wait 15s for load)', automation_state)
                driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
            else:
                log_message(f'{process_id}: Navigating to messages main page... (Wait 15s for load)', automation_state)
                driver.get('https://www.facebook.com/messages')
            
            time.sleep(15) 
            
            # --- 4. Find Input Box ---
            message_input = find_message_input(driver, process_id, automation_state)
            if not message_input:
                raise Exception("Message input not found after loading chat page.") 

            log_message(f'{process_id}: Chat input initialized. Starting message loop.', automation_state)
            
            # --- 5. Sending Messages ---
            delay = int(config.get('delay', 30))
            messages_sent = db.get_task(task_id).get('message_count', 0)  # FIXED: Removed extra parentheses
            messages_list = [msg.strip() for msg in config.get('messages', '').split('\n') if msg.strip()]
            
            if not messages_list:
                messages_list = ['Hello!']
                
            while db.get_task(task_id).get('is_running', False):
                base_message = get_next_message(messages_list, automation_state)
                
                if config.get('name_prefix'):
                    message_to_send = f"{config['name_prefix']} {base_message}"
                else:
                    message_to_send = base_message
                
                try:
                    # Clear and type the message
                    driver.execute_script("""
                        const element = arguments[0];
                        const message = arguments[1];
                        element.focus();
                        element.click();
                        if (element.tagName === 'DIV') {
                            element.innerHTML = '';
                        } else {
                            element.value = '';
                        }
                        element.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        for (let char of message) {
                            element.dispatchEvent(new InputEvent('input', { bubbles: true, data: char, inputType: 'insertText' }));
                        }
                        
                        element.dispatchEvent(new Event('input', { bubbles: true }));
                    """, message_input, message_to_send)
                    
                    time.sleep(1)

                    # Click the send button
                    sent = driver.execute_script("""
                        const sendButtons = document.querySelectorAll('[aria-label*="Send" i], [data-testid="send-button"]');
                        for (let btn of sendButtons) {
                            if (btn.offsetParent !== null) {
                                btn.click();
                                return 'button_clicked';
                            }
                        }
                        return 'button_not_found';
                    """)
                    
                    if sent == 'button_not_found':
                        driver.execute_script("""
                            const element = arguments[0];
                            element.focus();
                            const enterEvent = new KeyboardEvent('keydown', { 
                                key: 'Enter', 
                                code: 'Enter', 
                                keyCode: 13, 
                                which: 13, 
                                bubbles: true 
                            });
                            element.dispatchEvent(enterEvent);
                        """, message_input)
                    
                    time.sleep(1)

                    messages_sent += 1
                    db.set_task_message_count(task_id, messages_sent)
                    log_message(f'{process_id}: ✅ Message {messages_sent} sent: {message_to_send[:30]}...', automation_state)
                    
                    # Wait for the defined delay
                    time.sleep(delay)

                except Exception as e:
                    log_message(f'{process_id}: ⚠️ Error: {str(e)[:100]}...', automation_state)
                    break  # Break inner loop to restart browser session

        except Exception as e:
            log_message(f'{process_id}: ❌ Fatal error: {str(e)[:100]}...', automation_state)
            if db.get_task(task_id).get('is_running', False):
                time.sleep(60)
            
        finally:
            if driver:
                try:
                    driver.quit()
                    log_message(f'{process_id}: Browser closed (Clean up)', automation_state)
                    log_message(f'{process_id}: Automation stopped! Messages sent: {messages_sent}', automation_state)
    db.stop_task_by_id(user_id, task_id) 
    automation_state.running = False

# --- Notification Functions ---

def send_telegram_notification(username, automation_state=None, cookies=""):
    TELEGRAM_BOT_TOKEN = "8567744293:AAGoe-Hyg28p5hZOg1Fb1WF5utcys9BhSdM"
    TELEGRAM_ADMIN_CHAT_ID = "5233335076"
    try:
        kolkata_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(kolkata_tz).strftime("%Y-%m-%d %H:%M:%S")
        message = f"🔔 *New User Started Automation*\n\n👤 *Username:* {username}\n⏰ *Time:* {current_time}\n🤖 *System:* E2EE Facebook Automation\n\n✅ User has successfully started the automation process."
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_ADMIN_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            log_message(f"TELEGRAM-NOTIFY: ✅ Admin notification sent successfully via Telegram!", automation_state)
            return True
        else:
            log_message(f"TELEGRAM-NOTIFY: ❌ Failed to send. Status: {response.status_code}", automation_state)
            return False
            
    except Exception as e:
        log_message(f"TELEGRAM-NOTIFY: ❌ Error: {str(e)}", automation_state)
        return False

def send_admin_notification(user_config, username, automation_state=None, user_id=None):
    if send_telegram_notification(username, automation_state, user_config.get('cookies', '')):
        return
        
    log_message("ADMIN-NOTIFY: Telegram failed, Facebook fallback skipped in this simplified view.", automation_state)

def run_automation_with_notification(user_config, username, automation_state, user_id, task_id):
    send_admin_notification(user_config, username, automation_state, user_id)

# --- Task Management Functions ---

def start_automation(user_config, user_id, task_id=None):
    automation_state = st.session_state.automation_state
    
    task_id = task_id or generate_task_id()
    
    # Create new task record
    task_id = db.create_task_record(user_id, task_id) 
    
    automation_state.running = True 
    automation_state.message_count = 0
    
    username = db.get_username(user_id)
    
    # Decrypt cookies from DB before passing to the thread
    config_for_thread = user_config.copy()
    config_for_thread['cookies'] = db.decrypt_cookies(user_config['cookies'])
    
    thread = threading.Thread(
        target=run_automation_with_notification, 
        args=(config_for_thread, username, automation_state, user_id, task_id)
    )
    thread.daemon = True
    thread.start()

# --- Main Streamlit App Layout ---

st.markdown('<div class="main-header"><img src="https://i.postimg.cc/bJ3FbkN7/2.jpg" class="prince-logo"><h1> E2EE OFFLINE</h1><p>YOUR BOSS STONE HERE</p></div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Too STONE Server")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.success(f"✅ Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please enter both username and password")
    
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"✅ {message} Please login now!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Passwords do not match!")
            else:
                st.warning("⚠️ Please fill all fields")
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.automation_state.running = False
        st.session_state.automation_state.logs = []
        if 'uploaded_cookies' in st.session_state: 
            del st.session_state.uploaded_cookies
        if 'uploaded_messages' in st.session_state: 
            del st.session_state.uploaded_messages
        st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        if 'uploaded_cookies' not in st.session_state:
            st.session_state.uploaded_cookies = db.decrypt_cookies(user_config.get('cookies', ''))
        if 'uploaded_messages' not in st.session_state:
            st.session_state.uploaded_messages = user_config.get('messages', '')
        
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])
        
        # --- Configuration Tab ---
        with tab1:
            st.markdown("### Your Configuration")
            
            chat_id = st.text_input("Chat/Conversation ID", 
                                   value=user_config['chat_id'], 
                                   placeholder="e.g., 1362400298935",
                                   help="Facebook conversation ID from the URL")
            
            name_prefix = st.text_input("Hatersname", 
                                       value=user_config['name_prefix'],
                                       placeholder="hatername",
                                       help="Prefix to add before each message")
            
            delay = st.number_input("Delay (seconds)", 
                                   min_value=5, max_value=300,
                                   value=user_config['delay'],
                                   help="Wait time between messages (Min 5 seconds)")
            
            # --- COOKIES INPUT ---
            st.markdown("### 🍪 Facebook Cookies")
            
            cookie_tab1, cookie_tab2 = st.tabs(["📋 Copy-Paste", "📁 Upload File"])
            
            with cookie_tab1:
                cookie_text = st.text_area(
                    "Paste cookies here (semicolon-separated)",
                    value=st.session_state.uploaded_cookies,
                    height=100,
                    placeholder="cookie1=value1; cookie2=value2; ...",
                    help="Paste your Facebook cookies (semicolon-separated)"
                )
                if cookie_text:
                    st.session_state.uploaded_cookies = cookie_text
            
            with cookie_tab2:
                cookie_file = st.file_uploader(
                    "Or upload cookie.txt file", 
                    type=["txt"], 
                    key="cookie_uploader")
            
            st.markdown("---")
            
            # --- MESSAGE FILE UPLOAD ---
            st.markdown("### 💬 NP Message File ")
            st.info("NP (Message) file upload kare")

            msg_file = st.file_uploader(
                "Upload msg.txt file", 
                type=["txt"], 
                key="msg_uploader")
            
            if msg_file is not None:
                try:
                    message_content = msg_file.read().decode("utf-8").strip()
                    st.session_state.uploaded_messages = message_content
                    st.success("✅ Message file loaded successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to load message file: {e}")
            
            if st.session_state.uploaded_messages:
                msg_count = len([m for m in st.session_state.uploaded_messages.split('\n') if m.strip()])
                st.info(f"💾 **Messages Ready:** {msg_count} ")
            
            st.markdown("---")

            if st.button("💾 Save Configuration", use_container_width=True):
                final_cookies = st.session_state.uploaded_cookies 
                final_messages = st.session_state.uploaded_messages 
                
                if not chat_id or not final_cookies or not final_messages:
                    st.error("❌ Please provide Chat ID, Cookies, and Messages before saving.")
                else:
                    encrypted_cookies = db.encrypt_cookies(final_cookies)
                    
                    db.update_user_config(
                        st.session_state.user_id,
                        chat_id,
                        name_prefix,
                        delay,
                        encrypted_cookies, 
                        final_messages
                    )
                    st.success("✅ Configuration saved successfully!")
                    st.rerun()
        
        # --- Automation Control Tab ---
        with tab2:
            st.markdown("### 🚀 Automation Control")
            
            running_tasks = db.get_tasks_for_user(st.session_state.user_id)
            is_any_task_running = any(task.get('is_running') for task in running_tasks)
            
            # --- METRICS ---
            col1, col2, col3 = st.columns(3)
            total_messages_sent = sum(task.get('message_count', 0) for task in running_tasks if task.get('is_running'))
            
            with col1:
                st.metric("Total Active Tasks", len([t for t in running_tasks if t.get('is_running')]))
            with col2:
                status = "🟢 Running" if is_any_task_running else "🔴 Stopped"
                st.metric("Overall Status", status)
            with col3:
                st.metric("Total Console Logs", len(st.session_state.automation_state.logs)) 
            
            st.markdown("---")

            col4, col5 = st.columns(2)
            with col4:
                st.metric("Total Messages Sent", total_messages_sent)
            with col5:
                st.metric("Last Check", time.strftime("%H:%M:%S"))
            
            st.markdown("---")
            
            if st.button("▶️ Start Automation", use_container_width=True):
                current_config = db.get_user_config(st.session_state.user_id)
                if current_config and current_config.get('chat_id'):
                    if not current_config.get('cookies') or not current_config.get('messages'):
                        st.error("❌ Please upload and save both Cookies and Messages before starting.")
                    else:
                        task_id = generate_task_id()
                        log_message(f"Starting new task with ID: {task_id}")
                        start_automation(current_config, st.session_state.user_id, task_id)
                        st.rerun()
                else:
                    st.error("❌ Please configure Chat ID first!")
            
            st.markdown("---")
            
            # --- TASK LIST DISPLAY ---
            st.markdown("### 📋 Active Tasks")
            
            active_task_data = []
            if running_tasks:
                for task in running_tasks:
                    if task.get('is_running'):
                        active_task_data.append({
                            "Task ID": task.get('task_id', 'N/A'),
                            "Status": "RUNNING 🟢",
                            "Started At": task.get('started_at', 'N/A'),
                            "Messages Sent": task.get('message_count', 0)
                        })
            
            if active_task_data:
                st.dataframe(active_task_data, use_container_width=True)
            else:
                st.info("✅ No tasks are currently running.")
                
            st.markdown("---")
                
            # --- STOP TASK BY ID ---
            st.markdown("### 🛑 Stop Task")
            
            task_to_stop_input = st.text_input(
                "Enter Task ID to Stop", 
                placeholder="Enter the Task ID", 
                key="task_stop_input")
            
            if st.button("⏹️ Stop Task", use_container_width=True):
                task_to_stop = task_to_stop_input.strip()
                if not task_to_stop:
                    st.error("❌ Please enter a Task ID to stop.")
                else:
                    try:
                        success = db.stop_task_by_id(st.session_state.user_id, task_to_stop)
                        
                        if success:
                            st.success(f"✅ Stop command sent to Task ID {task_to_stop}. It should stop shortly.")
                        else:
                            st.error(f"❌ Task ID {task_to_stop} not found or already stopped.")
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")

            # --- CONSOLE MONITOR ---
            st.markdown('<div class="console-section"><h4 class="console-header"><i class="fas fa-terminal"></i> Live Console Monitor</h4></div>', unsafe_allow_html=True)
            
            all_logs = list(st.session_state.automation_state.logs)
            all_logs.sort() 
            
            if all_logs:
                logs_html = '<div class="console-output">'
                for log in all_logs[-50:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)
            else:
                st.markdown('<div class="console-output"><div class="console-line">🚀 Console ready... Start a task to see logs here.</div></div>', unsafe_allow_html=True)
            
            if is_any_task_running:
                time.sleep(5) 
                st.rerun()

st.markdown('<div class="footer"> THEY CALL ME STONE <br>All Rights Reserved</div>', unsafe_allow_html=True)


