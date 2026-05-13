<div align="center">

<a href="https://github.com/MohammadBahemmat/Telegram/blob/main/README.md">
    <img src="https://img.shields.io/badge/Read_in-Farsi-FF5722?style=for-the-badge&logo=readthedocs" alt="Read in Farsi">
</a>
</div>

<body>
<div class="container">
<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative" alt="License">
<img src="https://img.shields.io/badge/Platform-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions" alt="GitHub Actions">

</div>

<img src="https://github.com/MohammadBahemmat/Telegram/actions/workflows/main.yml/badge.svg" alt="Workflow Status">

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h1>🔄 V2ray Apps Update Checker</h1>

<p>
<strong>An automated bot for checking and announcing new versions of V2Ray applications in a Telegram channel.</strong><br>
This project uses <strong>GitHub Actions</strong> to automatically check the latest releases of V2Ray software every hour and sends a message containing download links and installation guides to your <strong>Telegram channel</strong> whenever a new update is found.
</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>🚀 Features</h2>
<table>
<thead><tr><th>Feature</th><th>Description</th></tr></thead>
<tbody>
<tr><td><strong>⏱️ Automated Checking</strong></td><td>Runs every hour via GitHub Actions without needing a dedicated server</td></tr>
<tr><td><strong>📱 Cross-Platform</strong></td><td>Detects download links for Windows (x64), macOS (ARM/Intel), and Android (arm64)</td></tr>
<tr><td><strong>📢 Telegram Notifications</strong></td><td>Sends beautifully formatted HTML messages with direct download links</td></tr>
<tr><td><strong>💾 State Tracking</strong></td><td>Saves the latest version ID to prevent duplicate notifications</td></tr>
<tr><td><strong>🍏 iOS Support</strong></td><td>Includes direct App Store links for FoXray, Streisand, and V2Box</td></tr>
<tr><td><strong>🆓 Completely Free</strong></td><td>100% open-source and runs on free GitHub Actions</td></tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>📢 Our Telegram Channel</h2>
<p>Join our Telegram channel for the latest V2Ray updates and tutorials:</p>
<p>🔗 <strong><a href="https://t.me/ACV_2ray" target="_blank">@ACV_2ray</a></strong></p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>📦 Requirements</h2>
<ul>
    <li>Python 3.10 or higher</li>
    <li>Install dependencies:
        <pre class="ltr-block">pip install -r requirements.txt</pre>
    </li>
    <li>A Telegram bot token from <a href="https://t.me/BotFather" target="_blank">@BotFather</a></li>
    <li>A Telegram channel ID (e.g., <code>@-100123456789</code>)</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>⚙️ Quick Setup (for Developers)</h2>
<ol>
    <li><strong>Fork</strong> this repository</li>
    <li>Go to <strong>Settings → Secrets and variables → Actions</strong> and add:
        <table>
        <tr><th>Secret Name</th><th>Description</th></tr>
        <tr><td><code>BOT_TOKEN</code></td><td>Your Telegram bot token</td></tr>
        <tr><td><code>CHANNEL_ID</code></td><td>Your Telegram channel ID</td></tr>
        </table>
    </li>
    <li>Enable <strong>GitHub Actions</strong> in the Actions tab</li>
    <li>The workflow runs automatically every hour — no further setup needed</li>
</ol>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>🗂️ Project Structure</h2>
<pre class="ltr-block">
.
├── .github/
│   └── workflows/
│       └── main.yml                  # GitHub Actions workflow (hourly cron)
├── version_checker.py                # Main update checker script
├── last_versions.json                # State file for tracking version IDs
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Ignored files
├── README.EN.md                      # English documentation
└── README.md                         # Persian documentation
</pre>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>🛠️ Customization</h2>
<ul>
    <li>To <strong>change the check frequency</strong>, edit the <code>cron</code> value in <code>main.yml</code></li>
    <li>To <strong>add or remove software</strong>, modify the <code>REPOS_TO_CHECK</code> and <code>IOS_APPS</code> dictionaries in <code>version_checker.py</code></li>
    <li>To <strong>customize the message text</strong>, edit the message template strings in <code>version_checker.py</code></li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>❗ Common Errors & Solutions</h2>
<details>
<summary><strong>Error: "BOT_TOKEN or CHANNEL_ID not set"</strong></summary>
<p>Make sure both <code>BOT_TOKEN</code> and <code>CHANNEL_ID</code> secrets are correctly added in <strong>Settings → Secrets and variables → Actions</strong>.</p>
</details>
<details>
<summary><strong>Telegram message not sending</strong></summary>
<ul>
    <li>Verify that the bot is an <strong>admin</strong> of the channel</li>
    <li>Ensure the <code>CHANNEL_ID</code> is correct (numeric format)</li>
</ul>
</details>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>🙏 Acknowledgements</h2>
<p>Thanks to all users and developers who help spread V2Ray tools. Feel free to submit suggestions or bug reports via <strong>Issues</strong> or through our Telegram channel.</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h2>📄 License</h2>
<p>This project is released under the <strong>MIT</strong> license. Use, modification, and distribution are free.</p>
