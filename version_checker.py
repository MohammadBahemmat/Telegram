import os
import requests
import json
import time

# --- تنظیمات اصلی ---
REPOS_TO_CHECK = {
    "v2rayN (Windows)": "2dust/v2rayN-Core",
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
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except FileNotFoundError:
        return {}

def save_last_versions(versions):
    with open(STATE_FILE, "w") as f: json.dump(versions, f, indent=4)

def send_telegram_message(message):
    if not BOT_TOKEN or not CHANNEL_ID:
        print("خطا: توکن ربات یا شناسه کانال تنظیم نشده است.")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True}
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
    new_versions_found = False
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
                new_versions_found = True

                links_text = ""
                instructions_text = ""

                if "Windows" in app_name:
                    link_64 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "With-Core.zip" in asset["name"] and "x64" in asset["name"]), None)
                    link_32 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "With-Core.zip" in asset["name"] and "x86" in asset["name"]), None)
                    if link_64: links_text += f"\n- [دانلود نسخه 64 بیتی]({link_64}) (پیشنهادی)"
                    if link_32: links_text += f"\n- [دانلود نسخه 32 بیتی]({link_32}) (سیستم‌های قدیمی)"
                    instructions_text = (
                        "\n\n*💡 نکته برای آپدیت آسان:*\n"
                        "همچنین می‌توانید از داخل برنامه آپدیت کنید:\n"
                        "۱. از منو `Check for updates` را انتخاب کنید.\n"
                        "۲. تیک گزینه‌های `v2rayN-Core`, `Xray-Core` و `Geo-files` را فعال نگه دارید.\n"
                        "۳. روی دکمه `Update` کلیک کنید."
                    )
                elif "Android" in app_name:
                    link_arm64 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "arm64-v8a" in asset["name"]), None)
                    link_arm32 = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if "armeabi-v7a" in asset["name"]), None)
                    if link_arm64: links_text += f"\n- [دانلود نسخه 64 بیتی]({link_arm64}) (اکثر گوشی‌ها)"
                    if link_arm32: links_text += f"\n- [دانلود نسخه 32 بیتی]({link_arm32}) (گوشی‌های قدیمی)"
                elif "macOS" in app_name:
                    link_dmg = next((asset["browser_download_url"] for asset in release_data.get("assets", []) if ".dmg" in asset["name"]), None)
                    if link_dmg: links_text += f"\n- [دانلود نسخه مک]({link_dmg})"
                    instructions_text = (
                        "\n\n*💡 نکته برای آپدیت آسان:*\n"
                        "از منوی بالای صفحه روی `V2RayX` و سپس `Check for Updates...` کلیک کنید."
                    )

                if not links_text: continue
                message_part = (
                    f"📱 **{app_name}**\n"
                    f"🔖 **نسخه:** `{release_data['tag_name']}`\n"
                    f"**لینک‌های دانلود:**{links_text}"
                    f"{instructions_text}"
                )
                updated_apps_messages.append(message_part)
                last_versions[repo_path] = latest_version_id

        except requests.RequestException as e:
            print(f"خطا در بررسی {app_name}: {e}")

    if updated_apps_messages:
        final_message = "📢 **آپدیت جدید برای نرم‌افزارها منتشر شد!**\n\n"
        final_message += "\n\n---\n\n".join(updated_apps_messages)
        final_message += f"\n\n🆔 @ACV_2ray"
        if send_telegram_message(final_message):
            save_last_versions(last_versions)
            time.sleep(5)
            ios_message = "🍏 **یادآوری برای کاربران آیفون (iOS)**\n\nبرای دریافت آخرین نسخه، همیشه می‌توانید از لینک‌های رسمی اپ استور زیر استفاده کنید:\n\n"
            for name, link in IOS_APPS.items():
                ios_message += f"• [{name}]({link})\n"
            ios_message += f"\n🆔 @ACV_2ray"
            send_telegram_message(ios_message)
    else:
        print("هیچ نسخه جدیدی یافت نشد.")

if __name__ == "__main__":
    check_for_updates()
