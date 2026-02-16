import feedparser
from datetime import datetime, timedelta, timezone
from config import PODCASTS


def fetch_recent_episodes(hours=24):
    """Fetch episodes published in the last `hours` hours from all configured podcasts."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    episodes = []

    for podcast in PODCASTS:
        try:
            feed = feedparser.parse(podcast["feed_url"])
            for entry in feed.entries:
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if not published:
                    continue

                from calendar import timegm
                pub_dt = datetime.fromtimestamp(timegm(published), tz=timezone.utc)

                if pub_dt >= cutoff:
                    description = (
                        entry.get("summary")
                        or entry.get("description")
                        or entry.get("subtitle", "")
                    )
                    # Strip HTML tags simply
                    import re
                    description = re.sub(r"<[^>]+>", "", description)

                    episodes.append({
                        "podcast": podcast["name"],
                        "title": entry.get("title", "Untitled"),
                        "description": description[:3000],  # cap length
                        "published": pub_dt.isoformat(),
                    })
        except Exception as e:
            print(f"Error fetching {podcast['name']}: {e}")

    episodes.sort(key=lambda x: x["published"], reverse=True)
    return episodes


if __name__ == "__main__":
    eps = fetch_recent_episodes()
    print(f"Found {len(eps)} new episodes in the last 24 hours:\n")
    for ep in eps:
        print(f"  [{ep['podcast']}] {ep['title']}")
        print(f"    Published: {ep['published']}")
        print(f"    Description: {ep['description'][:150]}...")
        print()
