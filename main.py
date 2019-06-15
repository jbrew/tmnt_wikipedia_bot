import os
import sys
import time
import wikipedia

from lib import images
from lib import twitter
from lib import words

# TODO:
#   - Drop titles with words unknown to CMU rather than countin them as 0 stress
#   - More docstrings
#   - README
#   - CLI arguments
#   - use real file format for keys
#   - Integration tests
#   - more unit tests
#   - actually enable option to run doctests
# Super bonus points:
#   - CI
#   - Mastodon
#   - archive posts locally
#   - cache of titles : stresses


def main():
    MAX_ATTEMPTS = 1000
    BACKOFF = 1

    title = searchForTMNT(MAX_ATTEMPTS, BACKOFF)
    logo = images.getLogo(title)

    try:
        tweet_status = twitter.sendTweet(title, logo)
    except OSError as e:
        sys.stderr.write(f"Unable to read logo file {logo}. Error: {e}")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error: {e}")
        sys.exit(1)

    # print(tweet_status)
    sys.exit(0)


def searchForTMNT(ATTEMPTS=1000, BACKOFF=1):
    """Loop MAX_ATTEMPT times, searching for a TMNT meter wikipedia title.

    Args:
        Integer: ATTEMPTS, retries remaining.
        Integer: BACKOFF, seconds to wait between each loop.
    Returns:
        String or False: String of wikipedia title in TMNT meter, or False if
                         none found.
    """
    for ATTEMPT in range(ATTEMPTS):
        print(f"\r{str(ATTEMPT * 10)} articles fetched...", end="")
        sys.stdout.flush()
        title = checkTenPagesForTMNT()

        if type(title) == str and len(title) > 1:
            print(f"\nMatched: {title}")
            return title

        time.sleep(BACKOFF)

    print(f"\nNo matches found.")
    sys.exit(1)


def checkTenPagesForTMNT():
    """Get 10 random wiki titles, check if any of them isTMNT().

    We grab the max allowed Wikipedia page titles (10) using wikipedia.random().
    If any title is in TMNT meter, return the title. Otherwise, return False.

    Args:
        None
    Returns:
        String or False: The TMNT compliant title, or False if none found.
    """
    wikipedia.set_rate_limiting(True)
    try:
        titles = wikipedia.random(10)
    except wikipedia.exceptions.HTTPTimeoutError as e:
        print(f"Wikipedia timout exception: {e}")
        time.sleep(120)
        main()
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Wikipedia exception: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Exception while fetching wiki titles: {e}")
        sys.exit(1)

    for title in titles:
        if words.isTMNT(title):
            return title
    return False


if __name__ == "__main__":
    main()
