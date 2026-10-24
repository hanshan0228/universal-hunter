import os
import unittest
import sqlite3
import tempfile
import json
from unittest.mock import patch

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


if __name__ == '__main__':
    unittest.main()
