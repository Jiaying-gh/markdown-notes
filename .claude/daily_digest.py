"""技术写作日报 — 自动收集并发送邮件"""

import json
import re
import smtplib
import ssl
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

# ── 配置 ──────────────────────────────────────────────────

SMTP_HOST = "smtp.163.com"
SMTP_PORT = 465
SMTP_USER = "sisuzanel@163.com"
SMTP_PASS = "FUyz5kfR99kVENNA"
MAIL_TO = "sisuzanel@163.com"
MAIL_FROM_NAME = "技术写作日报"

# 最大条目数
MAX_TOTAL = 10
# 期望比例：社交帖子 6-7 条，文章 3-4 条
TARGET_SOCIAL_MAX = 7
TARGET_ARTICLE_MAX = 4

SOURCES = [
    {
        "name": "Dev.to",
        "url": "https://dev.to/feed/tag/technicalwriting",
        "type": "rss",
        "category": "article",
    },
    {
        "name": "I'd Rather Be Writing",
        "url": "https://idratherbewriting.com/feed.xml",
        "type": "rss",
        "category": "article",
    },
    {
        "name": "Hacker News",
        "url": "https://hn.algolia.com/api/v1/search"
               "?query=technical+writing&tags=story"
               "&hitsPerPage=30&numericFilters=created_at_i>",
        "type": "hn_api",
        "category": "social",
    },
]

# 三天内的内容有效
CUTOFF_HOURS = 72


# ── 通用工具 ──────────────────────────────────────────────

def fetch_url(url, timeout=15):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                " AppleWebKit/537.36"
            ),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        return None


def parse_rss_date(date_str):
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
    ):
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(
                tzinfo=timezone.utc
            ) if date_str.strip() else None
        except (ValueError, AttributeError):
            continue
    return None


def clean_html(html_text):
    text = re.sub(r"<[^>]+>", "", html_text)
    text = text.replace("&amp;", "&") \
               .replace("&lt;", "<") \
               .replace("&gt;", ">") \
               .replace("&quot;", '"') \
               .replace("&#39;", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:200] + "..." if len(text) > 200 else text


# ── RSS 源采集 ──────────────────────────────────────────

def fetch_rss(source):
    data = fetch_url(source["url"])
    if not data:
        return []

    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return []

    channel = root.find("channel")
    items_node = channel.findall("item") if channel is not None else []
    if not items_node:
        items_node = root.findall(".//item")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=CUTOFF_HOURS)
    entries = []

    for item in items_node:
        title_el = item.find("title")
        link_el = item.find("link")
        desc_el = item.find("description")
        date_el = item.find("pubDate")
        if date_el is None:
            date_el = item.find("dc:date")
        if date_el is None:
            date_el = item.find("published")
        creator_el = item.find("{http://purl.org/dc/elements/1.1/}creator")
        if creator_el is None:
            creator_el = item.find("author")

        title = title_el.text if title_el is not None and title_el.text else "(无标题)"
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        desc = desc_el.text if desc_el is not None and desc_el.text else ""
        date_str = date_el.text.strip() if date_el is not None and date_el.text else ""
        author = creator_el.text.strip() if creator_el is not None and creator_el.text else ""

        pub_date = parse_rss_date(date_str) if date_str else None

        # 只保留三天内的内容
        if pub_date and pub_date < cutoff:
            continue

        entries.append({
            "title": title,
            "link": link,
            "summary": clean_html(desc),
            "author": author,
            "date": pub_date.strftime("%Y-%m-%d") if pub_date else "",
            "date_obj": pub_date or datetime.min.replace(tzinfo=timezone.utc),
            "source": source["name"],
            "category": source["category"],
        })

    return entries


# ── Hacker News API 采集 ───────────────────────────────

def fetch_hacker_news(source):
    cutoff_ts = int(
        (datetime.now(timezone.utc) - timedelta(hours=CUTOFF_HOURS)).timestamp()
    )
    url = source["url"] + str(cutoff_ts)
    data = fetch_url(url)
    if not data:
        return []

    try:
        result = json.loads(data)
    except json.JSONDecodeError:
        return []

    entries = []
    for hit in result.get("hits", []):
        title = hit.get("title", "")
        link = (
            hit.get("url")
            or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
        )
        author = hit.get("author", "")
        points = hit.get("points", 0)
        created_at = hit.get("created_at", "")
        created_ts = hit.get("created_at_i", 0)

        pub_date = datetime.fromtimestamp(created_ts, tz=timezone.utc) if created_ts else None
        if pub_date and pub_date < datetime.now(timezone.utc) - timedelta(hours=CUTOFF_HOURS):
            continue

        entries.append({
            "title": title,
            "link": link,
            "summary": f"👍 {points} points · by {author}" if author else f"👍 {points} points",
            "author": author,
            "date": created_at[:10] if created_at else "",
            "date_obj": pub_date or datetime.min.replace(tzinfo=timezone.utc),
            "source": "Hacker News",
            "category": "social",
        })

    return entries


# ── 条目筛选 ────────────────────────────────────────────

def select_entries(all_entries):
    """
    按规则筛选条目：
    - 最多 10 条
    - 社交帖子 6-7 条，文章 3-4 条
    - 按日期排序，最新的优先
    - 如果某类不够，另一类可补充（但总数不超过 10）
    """
    all_entries.sort(key=lambda e: e["date_obj"], reverse=True)

    social = [e for e in all_entries if e["category"] == "social"]
    articles = [e for e in all_entries if e["category"] == "article"]

    selected_social = social[:TARGET_SOCIAL_MAX]
    selected_articles = articles[:TARGET_ARTICLE_MAX]

    remaining_slots = MAX_TOTAL - len(selected_social) - len(selected_articles)

    # 如果还有空位，从两类中补充更多（优先补社交，再补文章）
    if remaining_slots > 0:
        extra_social = social[TARGET_SOCIAL_MAX:TARGET_SOCIAL_MAX + remaining_slots]
        selected_social.extend(extra_social)
        remaining_slots = MAX_TOTAL - len(selected_social) - len(selected_articles)
        if remaining_slots > 0:
            extra_articles = articles[TARGET_ARTICLE_MAX:TARGET_ARTICLE_MAX + remaining_slots]
            selected_articles.extend(extra_articles)

    result = selected_social + selected_articles
    result.sort(key=lambda e: e["date_obj"], reverse=True)
    return result


# ── 邮件生成与发送 ──────────────────────────────────────

def build_html(entries):
    total = len(entries)
    today = datetime.now().strftime("%Y-%m-%d")

    social_count = sum(1 for e in entries if e["category"] == "social")
    article_count = sum(1 for e in entries if e["category"] == "article")

    html_parts = [
        f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: -apple-system, 'Segoe UI', sans-serif;
             max-width: 680px; margin: 0 auto; padding: 20px;
             background: #f9f9f9;">
<div style="background: #fff; border-radius: 8px;
            padding: 32px; box-shadow: 0 1px 4px rgba(0,0,0,.08);">
<h1 style="font-size: 22px; color: #1a1a1a; margin: 0 0 4px 0;">
    📖 技术写作日报</h1>
<p style="color: #666; margin: 0 0 24px 0; font-size: 14px;">
    {today} · 社交 {social_count} 条 / 文章 {article_count} 篇</p>
<hr style="border: none; border-top: 1px solid #eee; margin: 0 0 24px 0;">
"""
    ]

    # 社交帖子区
    social_entries = [e for e in entries if e["category"] == "social"]
    if social_entries:
        html_parts.append("""
<h2 style="font-size: 17px; color:#333; margin: 28px 0 12px 0;
           padding-bottom:6px; border-bottom:2px solid #f59e0b;">
    💬 社交平台</h2>
""")
        for entry in social_entries:
            html_parts.append(_entry_html(entry, is_social=True))

    # 文章区
    article_entries = [e for e in entries if e["category"] == "article"]
    if article_entries:
        html_parts.append("""
<h2 style="font-size: 17px; color:#333; margin: 28px 0 12px 0;
           padding-bottom:6px; border-bottom:2px solid #4f46e5;">
    📄 文章</h2>
""")
        for entry in article_entries:
            html_parts.append(_entry_html(entry, is_social=False))

    html_parts.append(f"""
<hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
<p style="font-size: 12px; color: #999; text-align: center;">
    由 Claude Code 自动生成 · {today}</p>
</div></body></html>
""")

    return "\n".join(html_parts)


def _entry_html(entry, is_social=False):
    date_tag = f'<span style="color:#999;font-size:12px;">{entry["date"]}</span>' if entry.get("date") else ""
    author_tag = f'<span style="color:#999;font-size:12px;"> · {entry["author"]}</span>' if entry.get("author") else ""

    if is_social:
        # 社交帖子简化展示
        return f"""
<div style="padding: 10px 0; border-bottom: 1px solid #f0f0f0;">
    <a href="{entry["link"]}" style="font-size:14px;color:#2563eb;
       text-decoration:none;font-weight:500;">
       {entry["title"]}</a>
    <div style="font-size:12px;color:#888;margin-top:2px;">
        {date_tag}{author_tag}</div>
</div>"""
    else:
        # 文章展示详细信息
        return f"""
<div style="padding: 12px 0; border-bottom: 1px solid #f0f0f0;">
    <a href="{entry["link"]}" style="font-size:15px;color:#2563eb;
       text-decoration:none;font-weight:500;">
       {entry["title"]}</a>
    <div style="font-size:13px;color:#666;margin-top:4px;">
        {entry["summary"]}</div>
    <div style="font-size:12px;color:#999;margin-top:2px;">
        {date_tag}{author_tag}</div>
</div>"""


def send_email(subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr(
        (str(Header(MAIL_FROM_NAME, "utf-8")), SMTP_USER)
    )
    msg["To"] = MAIL_TO
    msg["Subject"] = Header(subject, "utf-8")

    text_body = re.sub(r"<[^>]+>", "", html_body)
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [MAIL_TO], msg.as_string())

    return True


# ── 主流程 ──────────────────────────────────────────────

def collect_all():
    fetchers = {
        "rss": fetch_rss,
        "hn_api": fetch_hacker_news,
    }

    all_entries = []
    for source in SOURCES:
        fetcher = fetchers.get(source["type"])
        if not fetcher:
            continue
        try:
            entries = fetcher(source)
            all_entries.extend(entries)
            sys.stderr.write(
                f"  ✓ {source['name']}: {len(entries)} 条\n"
            )
        except Exception as e:
            sys.stderr.write(
                f"  ✗ {source['name']}: {e}\n"
            )
        time.sleep(1)

    return all_entries


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    sys.stderr.write(f"📖 技术写作日报 · {today}\n")
    sys.stderr.write("正在采集...\n")

    all_entries = collect_all()

    # 筛选
    selected = select_entries(all_entries)

    if not selected:
        sys.stderr.write("没有符合条件的内容，跳过发送。\n")
        return

    social = sum(1 for e in selected if e["category"] == "social")
    article = sum(1 for e in selected if e["category"] == "article")

    sys.stderr.write(
        f"筛选完成：共 {len(selected)} 条"
        f"（社交 {social} / 文章 {article}）\n"
    )
    sys.stderr.write("正在生成邮件...\n")

    html = build_html(selected)
    subject = f"技术写作日报 - {today}"

    send_email(subject, html)
    sys.stderr.write(f"✅ 邮件已发送到 {MAIL_TO}\n")


if __name__ == "__main__":
    main()
