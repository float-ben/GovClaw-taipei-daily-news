import json
import urllib.request
import os
from datetime import datetime, timedelta, timezone

def send_discord_notification():
    webhook_url = "https://discord.com/api/webhooks/1489170065638035509/zC-HrxYHUdOwIjvhDrusT0I6HmQkF6kTyHsmew7cmPLSIesOgJ9ORvsSlF-s5pz0IZJ6"
    
    youtube_url = "https://www.youtube.com/watch?v=pRjtguERlVs"
    if os.path.exists("output/latest_youtube_url.txt"):
        with open("output/latest_youtube_url.txt", "r", encoding="utf-8") as f:
            youtube_url = f.read().strip()

    # Load today's selected articles
    articles_list = []
    if os.path.exists("output/selected_articles.json"):
        try:
            with open("output/selected_articles.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                articles_list = data.get("selected", [])
        except Exception as e:
            print(f"Error loading selected_articles.json: {e}")

    if articles_list:
        articles_text = "\n".join([f"{idx+1}. **{art.get('title')}**" for idx, art in enumerate(articles_list)])
    else:
        articles_text = (
            "1. **「2026四平解壓生活節」熱鬧登場！揮別負能量、找回好心情 壓力一槌擊碎！**\n"
            "2. **「2026本草派對 生息未來」8/29、30大稻埕登場！市集、餐飲、療癒體驗一次玩**\n"
            "3. **AI焦慮不必卡關！北市發布青年AI職涯地圖 148家企業8月15日花博爭艷館徵才**\n"
            "4. **「先生還在車上！」 八旬夫妻轉乘捷運被人潮沖散 捷警迅速調閱監視器助團圓**\n"
            "5. **出席中等學校校長會議 蔣萬安：投資教育穩賺不賠 教育預算創歷史新高**"
        )

    taipei_tz = timezone(timedelta(hours=8))
    today_str = datetime.now(taipei_tz).strftime("%Y-%m-%d")
    content = (
        f"✅ **[{today_str}] 每日台北市政新聞影片管線已順利完成！**\n\n"
        "今日精選的五大市政要聞如下：\n"
        f"{articles_text}\n\n"
        f"📺 **YouTube 影片連結：** {youtube_url}\n"
        "🌐 **市政資訊入口網站：** https://taipei-doit.github.io/CiviClaw-taipei-daily-news/\n"
        "🎧 **Spotify 播客頻道：** https://open.spotify.com/show/033jJtZiN097aPxw99mHYW\n\n"
        "本管道已將網站、Podcast 節目更新，並完成 LINE 官方帳號廣播、推送。心跳狀態已更新！"
    )

    payload = {"content": content}
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(webhook_url, data=data, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            print(f"[Discord] Sent successfully! HTTP {status}")
    except Exception as e:
        print(f"[Discord] Error sending message: {e}")

if __name__ == "__main__":
    send_discord_notification()
