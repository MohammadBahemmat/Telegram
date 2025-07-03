import os
import requests
import json
import time

# --- تنظیمات اصلی ---
REPOS_TO_CHECK = {
    "v2rayN (Windows)": "2dust/v2rayN",
    "v2rayNG (Android)": "2dust/v2rayNG",
    "V2RayX (macOS)": "Cenmrev/V2RayX"
}
IOS_APPS = {
    "FoXray": "https://apps.apple.com/us/app/foxray/id6448898396",
    "Streisand": "https://apps.apple.com/us/app/streisand/id6450534064"
}
STATE_FILE = "last_versions.json"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def get_last_versions():
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'w') as f:
            json.dump({}, f)
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_last_versions(versions):
    with open(STATE_FILE, "w") as f:
        json.dump(versions, f, indent=4)

def send_telegram_message(message):
    if not BOT_TOKEN or not CHANNEL_ID:
        print("خطا: توکن ربات یا شناسه کانال تنظیم نشده است.")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"پیام با موفقیت به کانال {CHANNEL_ID} ارسال شد.")
        return True
    else:
        print(f"خطا در ارسال پیام: {response.text}")
        return False

def check_for_updates():
    print("شروع بررسی برای نسخه‌های جدید...")
    last_versions = get_last_versions()
    updated_apps_messages = []

    # NEW: The new instruction text provided by the user
    new_instructions = (
        "\n\n<b>💡 نکته برای آپدیت آسان:</b>\n"
        "در برنامه، از منوی بالا روی <i>Check for updates</i> کلیک کنید. "
        "همه مقادیر را فعال بگذراید و بخش <i>Check for pre-release update</i> را خاموش کنید "
        "و در پایان روی <i>Check update</i> کلیک کنید. برنامه آپدیت را انجام داده و در نهایت "
        "یک دور به طور کامل (از تسک منیجر و تسک بار) ببندید و مجدد باز کنید."
    )

    for app_name, repo_path in REPOS_TO_CHECK.items():
        try:
            url = f"https://api.github.com/repos/{repo_path}/releases/latest"
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            release_data = response.json()
            latest_version_id = release_data["id"]

            if last_versions.get(repo_path) != latest_version_id:
                print(f"نسخه جدیدی برای {app_name} یافت شد: {release_data['tag_name']}")
                
                links_text = ""
                instructions_text = ""
                emoji = "📱" # Default emoji

                if "Windows" in app_name:
                    emoji = "💻"
                    # FIX: Updated logic for v2rayN to find 'v2rayN-Core.zip'
                    link_main = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "v2rayN-Core.zip" in asset["name"]), None)
                    if link_main: links_text += f'\n- <a href="{link_main}">دانلود نسخه کامل ویندوز</a>'
                    instructions_text = new_instructions
                
                elif "Android" in app_name:
                    emoji = "📱"
                    link_arm64 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "arm64-v8a" in asset["name"]), None)
                    link_arm32 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "armeabi-v7a" in asset["name"]), None)
                    if link_arm64: links_text += f'\n- <a href="{link_arm64}">دانلود نسخه 64 بیتی (اکثر گوشی‌ها)</a>'
                    if link_arm32: links_text += f'\n- <a href="{link_arm32}">دانلود نسخه 32 بیتی (گوشی‌های قدیمی)</a>'

                elif "macOS" in app_name:
                    emoji = "💻"
                    link_mac = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if ".app.zip" in asset["name"] or ".dmg" in asset["name"]), None)
                    if link_mac: links_text += f'\n- <a href="{link_mac}">دانلود نسخه مک</a>'
                    instructions_text = new_instructions

                if not links_text: 
                    print(f"هشدار: لینک دانلود مناسبی برای {app_name} پیدا نشد.")
                    continue

                message_part = (
                    f"{emoji} <b>{app_name}</b>\n"
                    f"🔖 <b>نسخه:</b> <code>{release_data['tag_name']}</code>\n"
                    f"<b>لینک‌های دانلود:</b>{links_text}"
                    f"{instructions_text}"
                )
                updated_apps_messages.append(message_part)
                last_versions[repo_path] = latest_version_id
        
        except requests.RequestException as e:
            print(f"خطا در بررسی {app_name}: {e}")

    if updated_apps_messages:
        # NEW: iOS reminder is now part of the main message
        ios_reminder_text = (
            "🍏 <b>یادآوری برای کاربران آیفون (iOS)</b>\n"
            "برای دریافت آخرین نسخه، همیشه می‌توانید از لینک‌های رسمی اپ استور زیر استفاده کنید:\n\n"
        )
        for name, link in IOS_APPS.items():
            ios_reminder_text += f'• <a href="{link}">{name}</a>\n'

        # Build the final single message
        final_message = "📢 <b>آپدیت جدید برای نرم‌افزارها منتشر شد!</b>\n\n"
        final_message += "\n\n---\n\n".join(updated_apps_messages)
        final_message += "\n\n---\n\n" + ios_reminder_text # Add iOS part
        final_message += f"\n🆔 @ACV_2ray"

        if send_telegram_message(final_message):
            save_last_versions(last_versions)
    else:
        print("هیچ نسخه جدیدی یافت نشد.")

if __name__ == "__main__":
    check_for_updates()
