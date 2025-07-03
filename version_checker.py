import os
import requests
import json
import time

# --- تنظیمات اصلی ---
REPOS_TO_CHECK = {
    # FIX: Corrected the repository path for v2rayN
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
    # FIX: Switched to HTML parse mode for better reliability
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

                if "Windows" in app_name:
                    # FIX: Updated logic for the new v2rayN repo asset names
                    link_64 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "v2rayN.zip" in asset["name"]), None)
                    if link_64: links_text += f'\n- <a href="{link_64}">دانلود نسخه کامل (64 و 32 بیتی)</a>'
                    instructions_text = (
                        "\n\n<b>💡 نکته برای آپدیت آسان:</b>\n"
                        "از منوی برنامه <i>Check for updates</i> را انتخاب کرده، تیک همه گزینه‌ها را فعال نگه دارید و روی <i>Update</i> کلیک کنید."
                    )
                elif "Android" in app_name:
                    link_arm64 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "arm64-v8a" in asset["name"]), None)
                    link_arm32 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "armeabi-v7a" in asset["name"]), None)
                    if link_arm64: links_text += f'\n- <a href="{link_arm64}">دانلود نسخه 64 بیتی (اکثر گوشی‌ها)</a>'
                    if link_arm32: links_text += f'\n- <a href="{link_arm32}">دانلود نسخه 32 بیتی (گوشی‌های قدیمی)</a>'
                elif "macOS" in app_name:
                    link_dmg = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if ".dmg" in asset["name"]), None)
                    if link_dmg: links_text += f'\n- <a href="{link_dmg}">دانلود نسخه مک</a>'
                    instructions_text = (
                        "\n\n<b>💡 نکته برای آپدیت آسان:</b>\n"
                        "از منوی بالای صفحه روی <i>V2RayX</i> و سپس <i>Check for Updates...</i> کلیک کنید."
                    )

                if not links_text: continue
                message_part = (
                    f"📱 <b>{app_name}</b>\n"
                    f"🔖 <b>نسخه:</b> <code>{release_data['tag_name']}</code>\n"
                    f"<b>لینک‌های دانلود:</b>{links_text}"
                    f"{instructions_text}"
                )
                updated_apps_messages.append(message_part)
                last_versions[repo_path] = latest_version_id
        
        except requests.RequestException as e:
            print(f"خطا در بررسی {app_name}: {e}")

    if updated_apps_messages:
        final_message = "📢 <b>آپدیت جدید برای نرم‌افزارها منتشر شد!</b>\n\n"
        final_message += "\n\n---\n\n".join(updated_apps_messages)
        final_message += f"\n\n🆔 @ACV_2ray"
        if send_telegram_message(final_message):
            save_last_versions(last_versions)
            time.sleep(5)
            ios_message = "🍏 <b>یادآوری برای کاربران آیفون (iOS)</b>\n\nبرای دریافت آخرین نسخه، همیشه می‌توانید از لینک‌های رسمی اپ استور زیر استفاده کنید:\n\n"
            for name, link in IOS_APPS.items():
                ios_message += f'• <a href="{link}">{name}</a>\n'
            ios_message += f"\n🆔 @ACV_2ray"
            send_telegram_message(ios_message)
    else:
        print("هیچ نسخه جدیدی یافت نشد.")

if __name__ == "__main__":
    check_for_updates()
