# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
"""
Apache License 2.0
Copyright (c) 2022 @Digital_Botz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Telegram Link : https://t.me/Digital_Botz 
Repo Link : https://github.com/DigitalBotz/Digital-Rename-Bot
License Link : https://github.com/DigitalBotz/Digital-Rename-Bot/blob/main/LICENSE
"""

from aiohttp import web
import json
import time
import psutil
import shutil
import os
import base64
from config import Config
from plugins import __version__
from helper.utils import humanbytes
from helper.database import digital_botz

# Ensure templates directory exists
os.makedirs('templates', exist_ok=True)

async def get_status():
    # Calculate your bot status metrics
    # Telethon/Pyrogram agnostic - relies on DB wrapper
    total_users = await digital_botz.total_users_count()
    
    # Check Config (set in config.py)
    if getattr(Config, 'PREMIUM_MODE', False):
        total_premium_users = await digital_botz.total_premium_users_count()
    else:
        total_premium_users = "Disabled ✅"
    
    # Calculate Uptime
    uptime_seconds = time.time() - Config.BOT_UPTIME
    currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(uptime_seconds))    
    
    # System Stats
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(psutil.net_io_counters().bytes_sent)
    recv = humanbytes(psutil.net_io_counters().bytes_recv)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    return {
        "status": "Operational",
        "version": __version__,
        "total_users": total_users,
        "total_premium_users": total_premium_users,
        "uptime": currentTime,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "disk_usage": disk_usage,
        "total_disk": total,
        "used_disk": used,
        "free_disk": free,
        "sent": sent,
        "recv": recv
    }
    
DigitalRenameBot = web.RouteTableDef()

@DigitalRenameBot.get("/", allow_head=True)
async def root_route_handler(request):
    # Get real-time status data
    status_data = await get_status()
    
    # Render template with actual data
    # Ensure templates/welcome.html exists in your directory
    try:
        with open('templates/welcome.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        return web.Response(text="Welcome to Digital Rename Bot (Template not found)", content_type='text/plain')
    
    # Replace placeholders with actual data
    html_content = template_content
    html_content = html_content.replace('{{bot_status}}', str(status_data['status']))
    html_content = html_content.replace('{{bot_version}}', str(status_data['version']))
    html_content = html_content.replace('{{total_users}}', str(status_data['total_users']))
    html_content = html_content.replace('{{premium_users}}', str(status_data['total_premium_users']))
    html_content = html_content.replace('{{bot_uptime}}', str(status_data['uptime']))
    html_content = html_content.replace('{{data_sent}}', str(status_data['sent']))
    html_content = html_content.replace('{{data_recv}}', str(status_data['recv']))
    
    html_content = html_content.replace('{{system_uptime}}', str(status_data['uptime']))
    html_content = html_content.replace('{{cpu_usage}}', str(status_data['cpu_usage']))
    html_content = html_content.replace('{{ram_usage}}', str(status_data['ram_usage']))
    html_content = html_content.replace('{{disk_usage}}', str(status_data['disk_usage']))
    html_content = html_content.replace('{{total_disk}}', str(status_data['total_disk']))
    html_content = html_content.replace('{{used_disk}}', str(status_data['used_disk']))
    html_content = html_content.replace('{{free_disk}}', str(status_data['free_disk']))
    html_content = html_content.replace('{{system_sent}}', str(status_data['sent']))
    html_content = html_content.replace('{{system_recv}}', str(status_data['recv']))
    
    # Add current timestamp for cache busting
    html_content = html_content.replace('{{timestamp}}', str(int(time.time())))
    
    return web.Response(text=html_content, content_type='text/html')

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(DigitalRenameBot)
    return web_app

# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Update Channel @Digital_Botz & @DigitalBotz_Support
