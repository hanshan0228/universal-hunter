#!/usr/bin/env python3
"""
Universal Hunter - Multi-Niche Tactical Database & Anti-Ban Engine
Handles:
- Dynamic relative path resolution (no hardcoded directories)
- Multi-niche data isolation (stats, keywords, and interaction quotas)
- Code-level Jaccard similarity check to prevent platform NLP clustering bans
- Subreddit Karma gating & risk classification
- URL sanitization and duplication prevention
"""

import sys
import os
import re
import json
import sqlite3
from datetime import datetime

DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'history.db'))
DB_PATH = os.environ.get('UNIVERSAL_HUNTER_DB_PATH', DEFAULT_DB_PATH)

HIGH_RISK_COMMERCIAL_SUBS = {
    'tiktokads', 'facebookads', 'dropship', 'dropshipping',
    'shopify', 'affiliate_marketing', 'adops', 'ecommerce', 'ppc'
}

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Check if interactions table exists with old UNIQUE(url)
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='interactions'")
    row = cursor.fetchone()
    if row and "url TEXT NOT NULL UNIQUE" in row['sql']:
        cursor.execute("ALTER TABLE interactions RENAME TO interactions_old")
        cursor.execute('''
            CREATE TABLE interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                niche TEXT NOT NULL DEFAULT 'default',
                platform TEXT NOT NULL,
                tier INTEGER NOT NULL,
                url TEXT NOT NULL,
                action TEXT NOT NULL,
                reply_snippet TEXT,
                target_user TEXT,
                routing_mode TEXT DEFAULT 'bio_routing',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(niche, url)
            )
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO interactions 
            (id, niche, platform, tier, url, action, reply_snippet, target_user, routing_mode, timestamp)
            SELECT id, niche, platform, tier, url, action, reply_snippet, target_user, routing_mode, timestamp
            FROM interactions_old
        ''')
        cursor.execute("DROP TABLE interactions_old")
    else:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                niche TEXT NOT NULL DEFAULT 'default',
                platform TEXT NOT NULL,
                tier INTEGER NOT NULL,
                url TEXT NOT NULL,
                action TEXT NOT NULL,
                reply_snippet TEXT,
                target_user TEXT,
                routing_mode TEXT DEFAULT 'bio_routing',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(niche, url)
            )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyword_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            niche TEXT NOT NULL DEFAULT 'default',
            keyword TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def clean_url_str(url):
    if not url:
        return ""
    # Strip whitespace, query parameters, hash fragments, and trailing slashes
    cleaned = url.strip().split('?')[0].split('#')[0].rstrip('/')
    return cleaned

def stats(niche=None):
    conn = get_db()
    cursor = conn.cursor()
    
    if niche and niche != 'all':
        cursor.execute(
            "SELECT COUNT(*) as cnt FROM interactions WHERE niche = ? AND date(timestamp) = date('now')",
            (niche,)
        )
        replies_today = cursor.fetchone()['cnt']
        
        cursor.execute("SELECT COUNT(*) as cnt FROM interactions WHERE niche = ?", (niche,))
        total_interactions = cursor.fetchone()['cnt']
    else:
        cursor.execute("SELECT COUNT(*) as cnt FROM interactions WHERE date(timestamp) = date('now')")
        replies_today = cursor.fetchone()['cnt']
        
        cursor.execute("SELECT COUNT(*) as cnt FROM interactions")
        total_interactions = cursor.fetchone()['cnt']
        
    print(json.dumps({
        "niche": niche or "all",
        "replies_today": replies_today,
        "total_interactions": total_interactions,
        "max_daily_limit": 8
    }))
    conn.close()

def check_keyword(keyword, niche='default'):
    kw = (keyword or "").strip().lower()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) as cnt FROM keyword_logs WHERE LOWER(keyword) = ? AND niche = ? AND timestamp >= datetime('now', '-24 hours')",
        (kw, niche)
    )
    cnt = cursor.fetchone()['cnt']
    print(json.dumps({
        "used_last_24h": cnt > 0,
        "keyword": keyword,
        "niche": niche
    }))
    conn.close()

def log_keyword(keyword, niche='default'):
    kw = (keyword or "").strip().lower()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO keyword_logs (keyword, niche) VALUES (?, ?)", (kw, niche))
    conn.commit()
    print(json.dumps({"logged": True, "keyword": keyword, "niche": niche}))
    conn.close()

def check_url(url, niche=None):
    cleaned = clean_url_str(url)
    conn = get_db()
    cursor = conn.cursor()
    if niche:
        cursor.execute("SELECT COUNT(*) as cnt FROM interactions WHERE url = ? AND niche = ?", (cleaned, niche))
    else:
        cursor.execute("SELECT COUNT(*) as cnt FROM interactions WHERE url = ?", (cleaned,))
    cnt = cursor.fetchone()['cnt']
    print(json.dumps({"duplicate": cnt > 0, "url": cleaned}))
    conn.close()

def log_interaction(niche, platform, tier, url, action, reply_snippet, target_user='', routing_mode='bio_routing'):
    cleaned = clean_url_str(url)
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''INSERT INTO interactions 
               (niche, platform, tier, url, action, reply_snippet, target_user, routing_mode) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (niche, platform, int(tier), cleaned, action, reply_snippet, target_user, routing_mode)
        )
        conn.commit()
        print(json.dumps({"logged": True, "url": cleaned, "niche": niche, "routing_mode": routing_mode}))
    except sqlite3.IntegrityError:
        print(json.dumps({"logged": False, "error": "IntegrityError (duplicate URL for this niche)"}))
    conn.close()

def tokenize(text):
    if not text:
        return set()
    # Match english words/numbers, and CJK characters/bigrams for accurate cross-language tokenization
    cjk_chars = re.findall(r'[\u4e00-\u9fff]', text)
    cjk_bigrams = [text[i:i+2] for i in range(len(text)-1) if re.match(r'[\u4e00-\u9fff]{2}', text[i:i+2])]
    words = set(re.findall(r'[a-zA-Z0-9]+', text.lower()))
    return words | set(cjk_bigrams) | set(cjk_chars)

def check_similarity(new_text, niche=None, threshold=0.50):
    new_tokens = tokenize(new_text)
    if not new_tokens or len(new_tokens) < 4:
        print(json.dumps({"allowed": True, "max_similarity": 0.0, "reason": "text too short to cluster"}))
        return

    conn = get_db()
    cursor = conn.cursor()
    if niche:
        cursor.execute(
            "SELECT reply_snippet FROM interactions WHERE niche = ? AND reply_snippet IS NOT NULL ORDER BY id DESC LIMIT 30",
            (niche,)
        )
    else:
        cursor.execute(
            "SELECT reply_snippet FROM interactions WHERE reply_snippet IS NOT NULL ORDER BY id DESC LIMIT 30"
        )
    rows = cursor.fetchall()
    conn.close()

    max_sim = 0.0
    conflicting_snippet = None

    for r in rows:
        prev_text = r['reply_snippet']
        prev_tokens = tokenize(prev_text)
        if not prev_tokens:
            continue
        intersection = len(new_tokens & prev_tokens)
        union = len(new_tokens | prev_tokens)
        sim = intersection / union if union > 0 else 0.0
        if sim > max_sim:
            max_sim = sim
            conflicting_snippet = prev_text

    is_allowed = max_sim < threshold
    result = {
        "allowed": is_allowed,
        "max_similarity": round(max_sim, 3),
        "threshold": threshold
    }
    if not is_allowed and conflicting_snippet:
        result["conflict_preview"] = conflicting_snippet[:80] + "..."
        result["directive"] = "Reject comment. Re-frame from a different angle to prevent platform clustering ban."
    print(json.dumps(result))

def check_karma_gate(karma_str, subreddit):
    try:
        karma = int(karma_str)
    except (ValueError, TypeError):
        karma = 0
    # Clean subreddit: handle /r/name, r/name, name, or full reddit URLs like https://reddit.com/r/name/...
    sub_raw = (subreddit or "").lower().strip()
    sub_extracted = re.sub(r'^.*?/?r/', '', sub_raw).split('/')[0].strip()
    
    if sub_extracted in HIGH_RISK_COMMERCIAL_SUBS and karma < 50:
        print(json.dumps({
            "allowed": False,
            "karma": karma,
            "subreddit": subreddit,
            "clean_subreddit": sub_extracted,
            "reason": f"Karma ({karma}) < 50. High risk of AutoMod instant ban in r/{sub_extracted}. Switch to warming mode in general subreddits."
        }))
    else:
        print(json.dumps({
            "allowed": True,
            "karma": karma,
            "subreddit": subreddit,
            "clean_subreddit": sub_extracted
        }))

if __name__ == '__main__':
    init_db()
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided"}))
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == 'stats':
        niche = sys.argv[2] if len(sys.argv) >= 3 else None
        stats(niche)
    elif cmd == 'check_keyword' and len(sys.argv) >= 3:
        niche = sys.argv[3] if len(sys.argv) >= 4 else 'default'
        check_keyword(sys.argv[2], niche)
    elif cmd == 'log_keyword' and len(sys.argv) >= 3:
        niche = sys.argv[3] if len(sys.argv) >= 4 else 'default'
        log_keyword(sys.argv[2], niche)
    elif cmd == 'check_url' and len(sys.argv) >= 3:
        niche = sys.argv[3] if len(sys.argv) >= 4 else None
        check_url(sys.argv[2], niche)
    elif cmd == 'log_interaction' and len(sys.argv) >= 8:
        target_user = sys.argv[8] if len(sys.argv) >= 9 else ''
        routing = sys.argv[9] if len(sys.argv) >= 10 else 'bio_routing'
        log_interaction(
            niche=sys.argv[2],
            platform=sys.argv[3],
            tier=sys.argv[4],
            url=sys.argv[5],
            action=sys.argv[6],
            reply_snippet=sys.argv[7],
            target_user=target_user,
            routing_mode=routing
        )
    elif cmd == 'check_similarity' and len(sys.argv) >= 3:
        niche = sys.argv[3] if len(sys.argv) >= 4 else None
        threshold = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.50
        check_similarity(sys.argv[2], niche, threshold)
    elif cmd == 'check_karma' and len(sys.argv) >= 4:
        check_karma_gate(sys.argv[2], sys.argv[3])
    else:
        print(json.dumps({"error": f"Unknown command or invalid args: {cmd}"}))
        sys.exit(1)
