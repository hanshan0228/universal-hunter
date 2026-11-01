import os
import sys
import unittest
import sqlite3
import tempfile
import json
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Point DB_PATH to a temporary database for test isolation
test_dir = tempfile.TemporaryDirectory()
os.environ['UNIVERSAL_HUNTER_DB_PATH'] = os.path.join(test_dir.name, 'test_history.db')

import scripts.db as hunter_db


class TestUniversalHunterDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hunter_db.init_db()

    @classmethod
    def tearDownClass(cls):
        test_dir.cleanup()

    def setUp(self):
        conn = hunter_db.get_db()
        conn.execute("DELETE FROM interactions")
        conn.execute("DELETE FROM keyword_logs")
        conn.commit()
        conn.close()

    def test_clean_url(self):
        self.assertEqual(
            hunter_db.clean_url_str("https://reddit.com/r/tiktokads/comments/123/title/?utm_source=share#cmt_456/"),
            "https://reddit.com/r/tiktokads/comments/123/title"
        )
        self.assertEqual(hunter_db.clean_url_str(""), "")

    def test_log_interaction_arg_parsing_and_isolation(self):
        # 1. 8-args call: default routing 'bio_routing', empty target_user
        hunter_db.log_interaction("niche_a", "reddit", 1, "https://reddit.com/post_1", "reply", "snippet 1")
        conn = hunter_db.get_db()
        r = conn.execute("SELECT * FROM interactions WHERE niche='niche_a'").fetchone()
        self.assertIsNotNone(r)
        self.assertEqual(r["target_user"], "")
        self.assertEqual(r["routing_mode"], "bio_routing")

        # 2. Multi-niche URL isolation: niche_b can interact with the same URL without collision
        hunter_db.log_interaction("niche_b", "reddit", 1, "https://reddit.com/post_1", "reply", "snippet 2", "user_b", "profile_only")
        r2 = conn.execute("SELECT * FROM interactions WHERE niche='niche_b'").fetchone()
        self.assertIsNotNone(r2)
        self.assertEqual(r2["target_user"], "user_b")
        self.assertEqual(r2["routing_mode"], "profile_only")
        conn.close()

    def test_check_karma_gate(self):
        # Commercial subreddits < 50 karma
        with patch('builtins.print') as mock_print:
            hunter_db.check_karma_gate(10, "/r/tiktokads/")
            data = json.loads(mock_print.call_args[0][0])
            self.assertFalse(data["allowed"])
            self.assertEqual(data["clean_subreddit"], "tiktokads")

            hunter_db.check_karma_gate(10, "https://reddit.com/r/dropship/comments/123")
            data2 = json.loads(mock_print.call_args[0][0])
            self.assertFalse(data2["allowed"])
            self.assertEqual(data2["clean_subreddit"], "dropship")

            # Commercial sub with >= 50 karma
            hunter_db.check_karma_gate(60, "tiktokads")
            data3 = json.loads(mock_print.call_args[0][0])
            self.assertTrue(data3["allowed"])

            # Non-commercial sub with low karma
            hunter_db.check_karma_gate(5, "golfcarts")
            data4 = json.loads(mock_print.call_args[0][0])
            self.assertTrue(data4["allowed"])

    def test_multilingual_jaccard_similarity(self):
        # English
        hunter_db.log_interaction("niche_en", "reddit", 1, "https://reddit.com/1", "reply", "Agency accounts bypass daily spend cap holds.")
        with patch('builtins.print') as mock_print:
            hunter_db.check_similarity("Agency accounts bypass the daily spend cap holds.", "niche_en")
            data = json.loads(mock_print.call_args[0][0])
            self.assertFalse(data["allowed"])
            self.assertGreaterEqual(data["max_similarity"], 0.50)

        # Chinese / CJK
        hunter_db.log_interaction("niche_cn", "reddit", 1, "https://reddit.com/2", "reply", "求梯子，请问现在还有能用的稳定节点推荐吗")
        with patch('builtins.print') as mock_print:
            hunter_db.check_similarity("求梯子，请问现在还有能用的靠谱节点推荐吗", "niche_cn")
            data = json.loads(mock_print.call_args[0][0])
            self.assertFalse(data["allowed"])
            self.assertGreaterEqual(data["max_similarity"], 0.50)

            hunter_db.check_similarity("今天天气不错，适合出去跑步锻炼身体", "niche_cn")
            data2 = json.loads(mock_print.call_args[0][0])
            self.assertTrue(data2["allowed"])

    def test_keyword_case_insensitivity(self):
        hunter_db.log_keyword("TikTok Agency Account", "test_niche")
        with patch('builtins.print') as mock_print:
            hunter_db.check_keyword("tiktok agency account", "test_niche")
            data = json.loads(mock_print.call_args[0][0])
            self.assertTrue(data["used_last_24h"])

    def test_dm_and_reply_coexistence_and_routing_modes(self):
        # 1. Log a public reply with direct_link
        hunter_db.log_interaction("niche_dm", "reddit", 1, "https://reddit.com/post_dm_1", "reply", "Check this link", "user_1", "direct_link")
        
        # 2. Log a private DM on the SAME post/author with inbound_dm
        hunter_db.log_interaction("niche_dm", "reddit", 1, "https://reddit.com/post_dm_1", "dm", "Here is your sheet", "user_1", "inbound_dm")
        
        conn = hunter_db.get_db()
        rows = conn.execute("SELECT action, routing_mode FROM interactions WHERE niche='niche_dm'").fetchall()
        self.assertEqual(len(rows), 2)
        actions = {r["action"] for r in rows}
        self.assertIn("reply", actions)
        self.assertIn("dm", actions)
        conn.close()

        # 3. Check stats breakdown
        with patch('builtins.print') as mock_print:
            hunter_db.stats("niche_dm")
            st = json.loads(mock_print.call_args[0][0])
            self.assertEqual(st["replies_today"], 1)
            self.assertEqual(st["dms_today"], 1)
            self.assertEqual(st["total_interactions"], 2)
            self.assertEqual(st["by_routing_mode"]["direct_link"], 1)
            self.assertEqual(st["by_routing_mode"]["inbound_dm"], 1)

        # 4. Check duplicate reply prevention
        with patch('builtins.print') as mock_print:
            hunter_db.check_url("https://reddit.com/post_dm_1", "niche_dm", "reply")
            ck = json.loads(mock_print.call_args[0][0])
            self.assertTrue(ck["duplicate"])

    def test_karma_gate_critical_and_high_risk(self):
        with patch('builtins.print') as mock_print:
            hunter_db.check_karma_gate("10", "TikTokAds")
            data = json.loads(mock_print.call_args[0][0])
            self.assertFalse(data["allowed"])
            self.assertTrue(data.get("is_critical"))
            self.assertIn("CRITICAL 极危门禁", data["reason"])

        with patch('builtins.print') as mock_print:
            hunter_db.check_karma_gate("10", "dropship")
            data = json.loads(mock_print.call_args[0][0])
            self.assertFalse(data["allowed"])
            self.assertFalse(data.get("is_critical"))

        with patch('builtins.print') as mock_print:
            hunter_db.check_karma_gate("60", "TikTokAds")
            data = json.loads(mock_print.call_args[0][0])
            self.assertTrue(data["allowed"])

    def test_humanize_and_strip_solicitation(self):
        from scripts.humanize import humanize_text, strip_ai_solicitation, strip_bio_hooks
        raw = "Agency accounts bypass threshold holds. Let me know if you need any help!"
        cleaned = strip_ai_solicitation(raw)
        self.assertEqual(cleaned, "Agency accounts bypass threshold holds.")

        raw_bio = "Here is the calculation. Pinned a breakdown on my profile."
        cleaned_bio = strip_bio_hooks(raw_bio)
        self.assertNotIn("pinned a breakdown", cleaned_bio.lower())

        humanized = humanize_text(raw, lowercase_prob=1.0, strip_period_prob=1.0, contractions_prob=0.0)
        self.assertTrue(humanized.startswith("a"))
        self.assertFalse(humanized.endswith("."))

    @patch("urllib.request.urlopen")
    def test_bio_readiness_check(self, mock_urlopen):
        from scripts.bio_checker import check_reddit_bio
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps({
            "data": {
                "name": "tester",
                "link_karma": 100,
                "comment_karma": 60,
                "total_karma": 160,
                "subreddit": {
                    "public_description": "Verified TikTok Ads whitelist guides pinned."
                }
            }
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        res = check_reddit_bio("tester")
        self.assertTrue(res["bio_ready"])
        self.assertTrue(res["routing_allowed"])

    @patch("urllib.request.urlopen")
    def test_visibility_inspection(self, mock_urlopen):
        from scripts.visibility import check_reddit_visibility
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b"""
        <html>
            <body>
                <div class="comment" thingid="t1_c999" id="t1_c999">
                    <p>Live comment content</p>
                </div>
            </body>
        </html>
        """
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        res = check_reddit_visibility("https://reddit.com/r/test/comments/123", "c999")
        self.assertTrue(res["visible"])
        self.assertEqual(res["status"], "VISIBLE")


if __name__ == '__main__':
    unittest.main()
