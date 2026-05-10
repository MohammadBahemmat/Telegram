#!/usr/bin/env python3
"""
V2Ray Apps Update Checker
Checks GitHub releases for v2rayN and v2rayNG, sends Persian Telegram notifications.
"""
import os
import requests
import json

# --- Main Configuration ---
REPOS_TO_CHECK = {
    "v2rayN (Desktop)": "2dust/v2rayN",
    "v2rayNG (Android)": "2dust/v2rayNG"
}

IOS_APPS = {
    "FoXray": "https://apps.apple.com/us/app/foxray/id6448898396",
    "Streisand": "https://apps.apple.com/us/app/streisand/id6450534064",
    "V2Box": "https://apps.apple.com/us/app/v2box-v2ray-client/id6446814690"
}

STATE_FILE = "last_versions.json"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def get_last_versions():
    """Load previously saved version IDs from state file."""
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'w') as f:
            json.dump({}, f)
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_last_versions(versions):
    """Save updated version IDs to state file."""
    with open(STATE_FILE, "w") as f:
        json.dump(versions, f, indent=4)


def send_telegram_message(message):
    """Send a formatted message to the configured Telegram channel."""
    if not BOT_TOKEN or not CHANNEL_ID:
        print("Error: BOT_TOKEN or CHANNEL_ID not set.")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Message sent successfully to channel {CHANNEL_ID}.")
            return True
        else:
            print(f"Error sending message: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return False


def find_asset_url(assets, keywords):
    """Find the first asset URL matching any of the given keywords."""
    for keyword in keywords:
        asset = next((a for a in assets if keyword in a["name"].lower()), None)
        if asset:
            return asset["browser_download_url"]
    return None


def check_for_updates():
    """Main function to check for new releases and send notifications."""
    print("شروع بررسی نسخه‌های جدید...")
    last_versions = get_last_versions()
    updated_apps_messages = []

    # --- Persian instruction for easy update ---
    update_guide = (
        "\n\n<b>💡 راهنمای آپدیت آسان:</b>\n"
        "در برنامه، از منوی بالا گزینه <i>Check for updates</i> را بزنید. "
        "تمام گزینه‌ها را فعال بگذارید و <i>Check for pre-release update</i> را خاموش کنید. "
        "سپس روی <i>Check update</i> کلیک کنید. پس از پایان آپدیت، برنامه را کاملاً بسته و دوباره باز کنید."
    )

    for app_name, repo_path in REPOS_TO_CHECK.items():
        try:
            url = f"https://api.github.com/repos/{repo_path}/releases/latest"
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            release_data = response.json()
            latest_version_id = release_data["id"]

            # Skip if already notified about this version
            if last_versions.get(repo_path) == latest_version_id:
                continue

            print(f"نسخه جدید برای {app_name} پیدا شد: {release_data['tag_name']}")
            assets = release_data.get("assets", [])
            message_part = ""

            # --- Desktop (v2rayN) ---
            if "Desktop" in app_name:
                win_link_sc = find_asset_url(
                    assets, ["windows-64-selfcontained.zip"]
                )
                win_link_64 = find_asset_url(assets, ["windows-64.zip"])
                mac_arm_link = find_asset_url(
                    assets, ["macos-arm64.dmg", "macos-arm64.zip"]
                )
                mac_intel_link = find_asset_url(
                    assets, ["macos-64.dmg", "macos-64.zip"]
                )

                desktop_links = ""
                if win_link_sc:
                    desktop_links += f'\n- <a href="{win_link_sc}">💻 نسخه ویندوز ۶۴ بیتی Self‑Contained</a> (پیشنهادی)'
                elif win_link_64:
                    desktop_links += f'\n- <a href="{win_link_64}">💻 نسخه ویندوز ۶۴ بیتی</a>'

                if mac_arm_link:
                    desktop_links += f'\n- <a href="{mac_arm_link}">🍎 نسخه مک (Apple Silicon)</a>'
                if mac_intel_link:
                    desktop_links += f'\n- <a href="{mac_intel_link}">🍎 نسخه مک (Intel)</a>'

                if desktop_links:
                    message_part += f"<b>{app_name}</b> | نسخه <code>{release_data['tag_name']}</code>"
                    message_part += desktop_links
                    message_part += update_guide

            # --- Android (v2rayNG) ---
            elif "Android" in app_name:
                link_arm64 = find_asset_url(assets, ["arm64-v8a.apk"])
                if link_arm64:
                    message_part += f"📱 <b>{app_name}</b> | نسخه <code>{release_data['tag_name']}</code>\n"
                    message_part += f'- <a href="{link_arm64}">دانلود نسخه ۶۴ بیتی (v8a)</a>'

            if message_part:
                updated_apps_messages.append(message_part)
                last_versions[repo_path] = latest_version_id

        except requests.RequestException as e:
            print(f"خطا در بررسی {app_name}: {e}")

    # --- Build and send the final Telegram message (all in Persian) ---
    if updated_apps_messages:
        ios_reminder = "🍏 <b>یادآوری برای کاربران آیفون (iOS)</b>\n"
        ios_reminder += "برای دریافت آخرین نسخه، از لینک‌های رسمی اپ استور زیر استفاده کنید:\n\n"
        for name, link in IOS_APPS.items():
            ios_reminder += f'• <a href="{link}">{name}</a>\n'

        final_message = "📢 <b>آپدیت جدید برای نرم‌افزارهای V2Ray منتشر شد!</b>\n\n"
        final_message += "\n\n---\n\n".join(updated_apps_messages)
        final_message += "\n\n---\n\n" + ios_reminder

        if send_telegram_message(final_message):
            save_last_versions(last_versions)
    else:
        print("هیچ نسخه جدیدی یافت نشد.")


if __name__ == "__main__":
    check_for_updates()
