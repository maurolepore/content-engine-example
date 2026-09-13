"""Google News RSS search — no API key, returns real dated headlines."""

import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

_RSS = "https://news.google.com/rss/search"
_UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def search(query, max_results=8):
    """Return [{title, url, source, date}] for one query."""
    params = {
        "q": query,
        "hl": "en-GB",
        "gl": "GB",
        "ceid": "GB:en",
    }
    url = f"{_RSS}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        root = ET.fromstring(resp.read())

    results = []
    for item in root.iter("item"):
        if len(results) >= max_results:
            break
        results.append(
            {
                "title": item.findtext("title", ""),
                "url": item.findtext("link", ""),
                "source": item.findtext("source", ""),
                "date": item.findtext("pubDate", ""),
            }
        )
    return results


def search_all(queries, max_results=8, pause=0.5):
    """Run a list of queries; return [{query, results}] nicely spaced."""
    out = []
    for q in queries:
        out.append({"query": q, "results": search(q, max_results)})
        time.sleep(pause)
    out = [q for q in out if q["results"]]
    return out
