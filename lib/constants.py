import re

# Constants for use throughout the application.
# Someday maybe I'll use configs or CLI args. For now this is easier.

MAX_ATTEMPTS = 1000
MAX_STATUS_LEN = 280
BACKOFF = 1
TIMEOUT_BACKOFF = 240
LOGO_PATH = "/tmp/logo.png"
CHROME_PATH = "google-chrome-beta"
KEY_PATH = "/home/cat/src/wiki-turtles/.keys"
# Article titles the contain strings in BANNED_WORDS are skipped.
# Banned words are things that are very inappropriate, or things
# that are oversaturating the timeline, i.e. historic districts
BANNED_WORDS = ("rape", "nazi", "victim")
BANNED_PHRASES = ("rugby union", "historic district")
PRONUNCIATION_OVERRIDES = (("HD", "10"), ("U.S.", "10"))
TMNT_STRESSES = re.compile(r"1[02]1[02]1[02]1[02]")
CHARS_ONLY = re.compile("[^a-zA-Z]")
