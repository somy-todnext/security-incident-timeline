import tempfile
import unittest
from pathlib import Path

from timeline import merge


class TimelineTests(unittest.TestCase):
    def test_demo_orders_events_across_sources_and_timezones(self):
        examples = Path(__file__).parent / "examples"
        events = merge([examples / "logins.csv", examples / "email.csv"])
        self.assertEqual([event["event"] for event in events], [
            "Phishing reported", "Sign-in failed", "Sign-in failed", "Sign-in succeeded"
        ])
        self.assertEqual(events[0]["timestamp"], "2026-11-06T09:01:00Z")

    def test_missing_timezone_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("timestamp,source,event,details\n2026-11-06T09:01:00,identity,Login,demo\n")
            with self.assertRaisesRegex(ValueError, r"bad\.csv:2:.*timezone"):
                merge([path])

    def test_equal_instants_preserve_input_order(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tie.csv"
            path.write_text("timestamp,source,event,details\n"
                            "2026-11-06T10:01:00+01:00,helpdesk,First,\n"
                            "2026-11-06T09:01:00Z,identity,Second,\n")
            self.assertEqual([row["event"] for row in merge([path])], ["First", "Second"])
