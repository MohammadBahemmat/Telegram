<div align="center">

<a href="https://github.com/MohammadBahemmat/Telegram/blob/main/README.EN.md">
    <img src="https://img.shields.io/badge/Read_in-English-009688?style=for-the-badge&logo=readthedocs" alt="Read in English">
</a>

<img src="https://github.com/MohammadBahemmat/Telegram/actions/workflows/main.yml/badge.svg" alt="Workflow Status">

<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative" alt="License">
<img src="https://img.shields.io/badge/Platform-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions" alt="GitHub Actions">

</div>

<hr>

<h1>🔄 بررسی‌کننده آپدیت نرم‌افزارهای V2ray</h1>

<p>
<strong>ربات بررسی و اعلام نسخه‌های جدید نرم‌افزارهای V2ray در کانال تلگرام</strong><br>
این پروژه با استفاده از <strong>GitHub Actions</strong> به‌طور خودکار هر ساعت آخرین نسخه‌های منتشر شده از نرم‌افزارهای V2Ray را بررسی می‌کند و در صورت وجود آپدیت جدید، پیامی حاوی لینک دانلود و راهنمای نصب به <strong>کانال تلگرام</strong> شما ارسال می‌کند.
</p>

<hr>

<h2>🚀 ویژگی‌ها</h2>
<table>
<thead><tr><th>ویژگی</th><th>توضیح</th></tr></thead>
<tbody>
<tr><td><strong>⏱️ بررسی خودکار</strong></td><td>هر ساعت از طریق GitHub Actions بدون نیاز به سرور اختصاصی</td></tr>
<tr><td><strong>📱 چندسکویی</strong></td><td>تشخیص لینک‌های دانلود برای ویندوز (x64)، مک (ARM/Intel) و اندروید (arm64)</td></tr>
<tr><td><strong>📢 اطلاع‌رسانی تلگرام</strong></td><td>ارسال پیام‌های HTML شکیل با لینک‌های مستقیم دانلود</td></tr>
<tr><td><strong>💾 ذخیره وضعیت</strong></td><td>ذخیره آخرین شناسه نسخه برای جلوگیری از ارسال تکراری</td></tr>
<tr><td><strong>🍏 پشتیبانی iOS</strong></td><td>شامل لینک مستقیم اپ استور برای FoXray، Streisand و V2Box</td></tr>
<tr><td><strong>🆓 کاملاً رایگان</strong></td><td>۱۰۰٪ متن‌باز و اجرا روی GitHub Actions رایگان</td></tr>
</tbody>
</table>

<hr>

<h2>📢 کانال تلگرام ما</h2>
<p>برای دریافت آخرین اخبار و آپدیت‌های V2ray، حتماً عضو کانال زیر شوید:</p>
<p>🔗 <strong><a href="https://t.me/ACV_2ray" target="_blank">@ACV_2ray</a></strong></p>

<hr>

<h2>📦 نیازمندی‌ها</h2>
<ul>
    <li>Python 3.10 یا بالاتر</li>
    <li>نصب نیازمندی‌ها:
        <pre class="ltr-block">pip install -r requirements.txt</pre>
    </li>
    <li>توکن ربات تلگرام از <a href="https://t.me/BotFather" target="_blank">BotFather@</a></li>
    <li>شناسه عددی کانال تلگرام (مثلاً <code>100123456789@-</code>)</li>
</ul>

<hr>

<h2>⚙️ راه‌اندازی سریع (برای توسعه‌دهندگان)</h2>
<ol>
    <li><strong>Fork</strong> کردن این مخزن</li>
    <li>به <strong>Settings → Secrets and variables → Actions</strong> بروید و دو Secret زیر را ایجاد کنید:
        <table>
        <tr><th>نام Secret</th><th>توضیح</th></tr>
        <tr><td><code>BOT_TOKEN</code></td><td>توکن ربات تلگرام شما</td></tr>
        <tr><td><code>CHANNEL_ID</code></td><td>شناسه عددی کانال تلگرام شما</td></tr>
        </table>
    </li>
    <li>مطمئن شوید <strong>GitHub Actions</strong> در مخزن فعال است</li>
    <li>Workflow به صورت خودکار هر یک ساعت اجرا می‌شود</li>
</ol>

<hr>

<h2>🗂️ ساختار پروژه</h2>
<pre class="ltr-block">
.
├── .github/
│   └── workflows/
│       └── main.yml                  # گردش‌کار GitHub Actions (cron ساعتی)
├── version_checker.py                # اسکریپت اصلی بررسی آپدیت
├── last_versions.json                # فایل وضعیت برای ذخیره شناسه نسخه‌ها
├── requirements.txt                  # نیازمندی‌های پایتون
├── .gitignore                        # فایل‌های نادیده گرفته‌شده
├── README.md                         # مستندات انگلیسی
└── README.fa.md                      # مستندات فارسی
</pre>

<hr>

<h2>🛠️ سفارشی‌سازی</h2>
<ul>
    <li>برای <strong>تغییر فرکانس بررسی</strong>، مقدار <code>cron</code> را در <code>main.yml</code> ویرایش کنید</li>
    <li>برای <strong>افزودن یا حذف نرم‌افزار</strong>، دیکشنری‌های <code>REPOS_TO_CHECK</code> و <code>IOS_APPS</code> را در <code>version_checker.py</code> تغییر دهید</li>
    <li>برای <strong>تغییر متن پیام</strong>، رشته‌های قالب پیام در <code>version_checker.py</code> را ویرایش کنید</li>
</ul>

<hr>

<h2>❗ خطاهای رایج و راه‌حل</h2>
<details>
<summary><strong>خطای "BOT_TOKEN or CHANNEL_ID not set"</strong></summary>
<p>مطمئن شوید دو Secret به نام‌های <code>BOT_TOKEN</code> و <code>CHANNEL_ID</code> در <strong>Settings → Secrets and variables → Actions</strong> به درستی تنظیم شده‌اند.</p>
</details>
<details>
<summary><strong>پیام تلگرام ارسال نمی‌شود</strong></summary>
<ul>
    <li>بررسی کنید که ربات <strong>ادمین</strong> کانال باشد</li>
    <li>شناسه کانال (CHANNEL_ID) باید عددی و صحیح باشد</li>
</ul>
</details>

<hr>

<h2>🙏 تقدیر و تشکر</h2>
<p>از تمام کاربران و توسعه‌دهندگانی که با استفاده از این ابزار به گسترش V2ray کمک می‌کنند سپاسگزاریم. لطفاً با ارسال نظرات و پیشنهادات خود در بخش Issues یا از طریق کانال تلگرام ما را یاری کنید.</p>

<hr>

<h2>📄 مجوز</h2>
<p>این پروژه تحت مجوز <strong>MIT</strong> منتشر شده است. استفاده، تغییر و توزیع آن آزاد است.</p>
