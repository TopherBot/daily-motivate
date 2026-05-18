#!/usr/bin/env python3
"""daily-motivate – print a random motivational quote.

If the ``--notify`` flag is supplied, a native desktop notification is shown
(using ``osascript`` on macOS, ``notify-send`` on Linux, and ``toast`` on
Windows via ``ctypes``). The script is deliberately tiny, has no third‑party
dependencies, and includes a minimal unit‑test suite at the bottom.
"""

import argparse
import random
import sys
import platform
import subprocess
from typing import List

# ---------------------------------------------------------------------------
# Quote database – a small curated list.
# ---------------------------------------------------------------------------
QUOTES: List[str] = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Dream big and dare to fail. – Norman Vaughan",
    "It does not matter how slowly you go as long as you do not stop. – Confucius",
    "You miss 100% of the shots you don’t take. – Wayne Gretzky",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Hard work beats talent when talent doesn’t work hard. – Tim Notke",
    "The future belongs to those who prepare for it today. – Malcolm X",
    "Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn’t just find you. You have to go out and get it.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Don’t stop when you’re tired. Stop when you’re done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for.",
    "Little things make big days.",
    "It’s going to be hard, but you’re harder."
]

# ---------------------------------------------------------------------------
# Core functionality.
# ---------------------------------------------------------------------------
def get_random_quote() -> str:
    """Return a random quote from the QUOTES list."""
    return random.choice(QUOTES)

def print_quote(quote: str) -> None:
    """Print the quote to stdout."""
    print(quote)

def send_notification(quote: str) -> None:
    """Show a native desktop notification containing *quote*.

    The implementation varies by OS. If the required tool is unavailable,
    the function falls back to printing a warning.
    """
    system = platform.system()
    try:
        if system == "Darwin":  # macOS – use osascript (AppleScript)
            script = f'display notification "{quote}" with title "Motivation"'
            subprocess.run(["osascript", "-e", script], check=True)
        elif system == "Linux":  # Linux – use notify-send (usually present)
            subprocess.run(["notify-send", "Motivation", quote], check=True)
        elif system == "Windows":  # Windows – use a simple toast via PowerShell
            ps_script = (
                "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;"
                "$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);"
                "$toastXml = $template.GetXml();"
                "$toastXml.GetElementsByTagName('text')[0].AppendChild($toastXml.CreateTextNode('Motivation')) > $null;"
                "$toastXml.GetElementsByTagName('text')[1].AppendChild($toastXml.CreateTextNode('{quote}')) > $null;"
                "$toast = [Windows.UI.Notifications.ToastNotification]::new($toastXml);"
                "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('daily-motivate').Show($toast)"
            )
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True)
        else:
            print("[warning] Notification not supported on this OS.", file=sys.stderr)
    except FileNotFoundError:
        print("[warning] Required notification tool not found; falling back to stdout.", file=sys.stderr)
        print_quote(quote)
    except subprocess.CalledProcessError:
        print("[warning] Failed to send notification; falling back to stdout.", file=sys.stderr)
        print_quote(quote)

# ---------------------------------------------------------------------------
# CLI handling.
# ---------------------------------------------------------------------------
def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random motivational quote.")
    parser.add_argument(
        "--notify",
        action="store_true",
        help="Show the quote as a desktop notification instead of stdout"
    )
    return parser.parse_args(argv)

def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv)
    quote = get_random_quote()
    if args.notify:
        send_notification(quote)
    else:
        print_quote(quote)

# ---------------------------------------------------------------------------
# Minimal unit‑test suite (tiny but covers the main functions).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # When the script is invoked directly without arguments, run the CLI.
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        import unittest

        class TestMotivator(unittest.TestCase):
            def test_get_random_quote(self):
                quote = get_random_quote()
                self.assertIn(quote, QUOTES)

            def test_print_quote(self):
                # Capture stdout
                from io import StringIO
                saved = sys.stdout
                try:
                    out = StringIO()
                    sys.stdout = out
                    print_quote("test")
                    self.assertEqual(out.getvalue().strip(), "test")
                finally:
                    sys.stdout = saved

        unittest.main(argv=["unittest"], exit=False)
    else:
        main()
