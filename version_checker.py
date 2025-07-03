import os
import requests
import json
import time

# --- تنظیمات اصلی ---
REPOS_TO_CHECK = {
    "v2rayN (Desktop)": "2dust/v2rayN",
    "v2rayNG (Android)": "2dust/v2rayNG"
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

def find_asset_url(assets, keywords):
    """A helper function to find the first asset matching a list of keywords."""
    for keyword in keywords:
        for asset in assets:
            if keyword in asset["name"]:
                return asset["browser_download_url"]
    return None

def check_for_updates():
    print("شروع بررسی برای نسخه‌های جدید...")
    last_versions = get_last_versions()
    updated_apps_messages = []

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
                
                # --- NEW: Comprehensive logic for all platforms ---
                message_part = f"⬇️ <b>{app_name}</b> | نسخه <code>{release_data['tag_name']}</code>\n"
                found_links = False

                if "Desktop" in app_name: # For v2rayN repo
                    # Windows
                    win_links = ""
                    win_64_sc = find_asset_url(assets, ["windows-64-SelfContained.zip"])
                    win_64 = find_asset_url(assets, ["windows-64.zip"])
                    win_arm64 = find_asset_url(assets, ["windows-arm64.zip"])
                    if win_64_sc: win_links += f'\n- <a href="{win_64_sc}">نسخه 64 بیتی Self-Contained</a> (پیشنهادی)'
                    if win_64: win_links += f'\n- <a href="{win_64}">نسخه 64 بیتی معمولی</a>'
                    if win_arm64: win_links += f'\n- <a href="{win_arm64}">نسخه ویندوز ARM</a>'
                    if win_links:
                        message_part += "\n💻 <b>Windows</b>" + win_links
                        found_links = True

                    # macOS
                    mac_links = ""
                    mac_arm64 = find_asset_url(assets, ["macos-arm64.dmg"])
                    mac_64 = find_asset_url(assets, ["macos-64.dmg"])
                    if mac_arm64: mac_links += f'\n- <a href="{mac_arm64}">مک (Apple Silicon M1/M2)</a>'
                    if mac_64: mac_links += f'\n- <a href="{mac_64}">مک (Intel)</a>'
                    if mac_links:
                        message_part += "\n\n🍎 <b>macOS</b>" + mac_links
                        found_links = True

                    # Linux
                    linux_links = ""
                    linux_64 = find_asset_url(assets, ["linux-64.AppImage"])
                    linux_arm64 = find_asset_url(assets, ["linux-arm64.AppImage"])
                    if linux_64: linux_links += f'\n- <a href="{linux_64}">لینوکس 64 بیتی (AppImage)</a>'
                    if linux_arm64: linux_links += f'\n- <a href="{linux_arm64}">لینوکس ARM (AppImage)</a>'
                    if linux_links:
                        message_part += "\n\n🐧 <b>Linux</b>" + linux_links
                        found_links = True

                elif "Android" in app_name:
                    android_links = ""
                    link_arm64 = find_asset_url(assets, ["arm64-v8a.apk"])
                    link_arm32 = find_asset_url(assets, ["armeabi-v7a.apk"])
                    link_universal = find_asset_url(assets, ["universal.apk"])
                    if link_arm64: android_links += f'\n- <a href="{link_arm64}">نسخه 64 بیتی (اکثر گوشی‌ها)</a>'
                    if link_arm32: android_links += f'\n- <a href="{link_arm32}">نسخه 32 بیتی (گوشی‌های قدیمی)</a>'
                    if link_universal: android_links += f'\n- <a href="{link_universal}">نسخه Universal (جامع)</a>'
                    if android_links:
                        message_part += android_links
                        found_links = True
                
                if not found_links: continue
                
                updated_apps_messages.append(message_part)
                last_versions[repo_path] = latest_version_id
        
        except requests.RequestException as e:
            print(f"خطا در بررسی {app_name}: {e}")

    if updated_apps_messages:
        ios_reminder_text = "🍏 <b>یادآوری برای کاربران آیفون (iOS)</b>\n"
        ios_reminder_text += "برای دریافت آخرین نسخه، از لینک‌های رسمی اپ استور استفاده کنید:\n\n"
        for name, link in IOS_APPS.items():
            ios_reminder_text += f'• <a href="{link}">{name}</a>\n'
        
        final_message = "📢 <b>آپدیت جدید برای نرم‌افزارها منتشر شد!</b>\n\n"
        final_message += "\n\n---\n\n".join(updated_apps_messages)
        final_message += "\n\n---\n\n" + ios_reminder_text
        final_message += f"\n\n🆔 @ACV_2ray"

        if send_telegram_message(final_message):
            save_last_versions(last_versions)
    else:
        print("هیچ نسخه جدیدی یافت نشد.")

if __name__ == "__main__":
    check_for_updates()
