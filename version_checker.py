import os
import requests
import json
import time

# --- تنظیمات اصلی ---
REPOS_TO_CHECK = {
    "v2rayN (Desktop)": "2dust/v2rayN",
    "v2rayNG (Android)": "2dust/v2rayNG"
}
# NEW: Added V2Box to the list of recommended iOS apps
IOS_APPS = {
    "FoXray": "https://apps.apple.com/us/app/foxray/id6448898396",
    "Streisand": "https://apps.apple.com/us/app/streisand/id6450534064",
    "V2Box": "https://apps.apple.com/us/app/v2box-v2ray-client/id6446814690"
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

def find_asset_url(assets, keywords):
    for keyword in keywords:
        asset = next((asset for asset in assets if keyword in asset["name"].lower()), None)
        if asset:
            return asset["browser_download_url"]
    return None

def check_for_updates():
    print("شروع بررسی برای نسخه‌های جدید...")
    last_versions = get_last_versions()
    updated_apps_messages = []

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
                assets = release_data.get("assets", [])
                
                message_part = ""
                
                if "Desktop" in app_name:
                    win_link = find_asset_url(assets, ["v2rayn-core.zip"])
                    mac_arm_link = find_asset_url(assets, ["macos-arm64.dmg", "macos-arm64.zip"])
                    mac_intel_link = find_asset_url(assets, ["macos-64.dmg", "macos-64.zip"])
                    linux_link = find_asset_url(assets, ["linux-64.appimage"])
                    
                    message_part += f"💻 <b>{app_name}</b> | نسخه <code>{release_data['tag_name']}</code>\n"
                    if win_link: message_part += f'\n- <a href="{win_link}">دانلود نسخه کامل ویندوز</a>'
                    if mac_arm_link: message_part += f'\n- <a href="{mac_arm_link}">دانلود نسخه مک (Apple Silicon)</a>'
                    if mac_intel_link: message_part += f'\n- <a href="{mac_intel_link}">دانلود نسخه مک (Intel)</a>'
                    if linux_link: message_part += f'\n- <a href="{linux_link}">دانلود نسخه لینوکس (AppImage)</a>'
                    message_part += new_instructions

                elif "Android" in app_name:
                    link_arm64 = find_asset_url(assets, ["arm64-v8a.apk"])
                    link_arm32 = find_asset_url(assets, ["armeabi-v7a.apk"])
                    
                    message_part += f"📱 <b>{app_name}</b> | نسخه <code>{release_data['tag_name']}</code>\n"
                    if link_arm64: message_part += f'\n- <a href="{link_arm64}">دانلود نسخه 64 بیتی (اکثر گوشی‌ها)</a>'
                    if link_arm32: message_part += f'\n- <a href="{link_arm32}">دانلود نسخه 32 بیتی (گوشی‌های قدیمی)</a>'

                if message_part:
                    updated_apps_messages.append(message_part)
                    last_versions[repo_path] = latest_version_id
        
        except requests.RequestException as e:
            print(f"خطا در بررسی {app_name}: {e}")

    if updated_apps_messages:
        ios_reminder_text = "🍏 <b>یادآوری برای کاربران آیفون (iOS)</b>\n"
        ios_reminder_text += "برای دریافت آخرین نسخه، از لینک‌های رسمی اپ استور زیر استفاده کنید:\n\n"
        for name, link in IOS_APPS.items():
            ios_reminder_text += f'• <a href="{link}">{name}</a>\n'
        
        final_message = "📢 <b>آپدیت جدید برای نرم‌افزارها منتشر شد!</b>\n\n"
        final_message += "\n\n---\n\n".join(updated_apps_messages)
        final_message += "\n\n---\n\n" + ios_reminder_text

        if send_telegram_message(final_message):
            save_last_versions(last_versions)
    else:
        print("هیچ نسخه جدیدی یافت نشد.")

if __name__ == "__main__":
    check_for_updates()
