import discord
from discord.ext import commands
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- 1. 生存確認用の簡易サーバー (Koyeb対策) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

# --- 2. Discord Botの設定 ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def schedule(ctx):
    # ここにGoogleカレンダーから予定を取得する処理を書く
    await ctx.send("今日の予定を取得します...")

# --- 3. 実行 ---
if __name__ == "__main__":
    # 生存確認サーバーを別スレッドで起動
    threading.Thread(target=run_health_check, daemon=True).start()
    # Botの起動 (TOKENは環境変数から読み込む)
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))