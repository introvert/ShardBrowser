"""Phone profiles get Chrome for Android's API set through Blink's own switches.

Run: python3 -m unittest discover -s sdks/python/tests (or pytest)."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path

# runtime.py on its own, as in test_runtime_swap.py: no browser driver needed.
if "httpx" not in sys.modules:
    try:
        import httpx  # noqa: F401
    except ImportError:
        sys.modules["httpx"] = types.ModuleType("httpx")
RUNTIME_PY = Path(__file__).resolve().parents[1] / "shardx" / "runtime.py"
_spec = importlib.util.spec_from_file_location("shardx_runtime_blink_test", RUNTIME_PY)
rt = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = rt
_spec.loader.exec_module(rt)


class AndroidBlinkTest(unittest.TestCase):
    def test_a_phone_turns_off_the_desktop_only_apis(self):
        switches, rest = rt.android_blink_switches([])
        self.assertEqual(switches, [
            "--disable-blink-features=" + ",".join(rt.DESKTOP_ONLY_BLINK_FEATURES),
            "--enable-blink-features=" + ",".join(rt.ANDROID_ONLY_BLINK_FEATURES),
        ])
        self.assertEqual(rest, [])

    def test_the_callers_blink_switches_are_folded_in_and_win(self):
        switches, rest = rt.android_blink_switches([
            "--disable-blink-features=AutomationControlled,OrientationEvent",
            "--lang=de",
            "--enable-blink-features=NotificationConstructor",
        ])
        self.assertEqual(rest, ["--lang=de"])
        off = switches[0].split("=", 1)[1].split(",")
        self.assertIn("AutomationControlled", off)
        self.assertIn("OrientationEvent", off)
        self.assertIn("WebHID", off)
        self.assertNotIn("NotificationConstructor", off)
        self.assertEqual(switches[1:], ["--enable-blink-features=NotificationConstructor"])


if __name__ == "__main__":
    unittest.main()
