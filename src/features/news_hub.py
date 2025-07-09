import feedparser

NEWS_SOURCES = {
    "hackernews": "https://news.ycombinator.com/rss",
    "techcrunch": "https://techcrunch.com/feed/",
}

def get_news(source_name="hackernews", limit=7):
    """
    Fetches the latest news from a specified source's RSS feed.

    Args:
        source_name (str): The nickname of the news source from out dictionary.
                           Defaults to 'hackernews'.
        limit (int): The maximum number of articles to return. Defaults to 7.

    Returns:
        A list of formatted news headlines or an error string.
    """

    # look up the URL from out dictionary using the provided source_name
    # .get() is a safe way to access a dictionary.
    source_url = NEWS_SOURCES.get(source_name.lower())

    if not source_url:
        return [f"Error: Unkown news source '{source_name}'. Available sources are: {list(NEWS_SOURCES.keys())}"]


    try:
        # This is the main feedparser command.
        print(f"Fetching latest news from {source_name.title()}...")
        news_feed = feedparser.parse(source_url)

        # We need an empty list to hold the formatted headlines.
        headlines = []

        # Loop though the entries in feed, up to limit.
        # news_feed.entries[:limit] is a python "slice" that gets first 'limit' items.
        for entry in news_feed.entries[:limit]:
            title = entry.get("title", "No Title")
            link = entry.get("link", "#")

            # We add the formatted headlines to out list.
            headlines.append(f"  - {title}\n    Link: {link}")

        # if we successfully found headlines, return them.
        if headlines:
            return headlines
        else:
            return [f"No articles found for source '{source_name}'."]

    except Exception as e:
        return [f"An error occurred while fetching news: {e}"]
