from tech_news.database import db, search_news


# Requisito 10
def top_5_news():
    results = []
    search = search_news({})
    if len(search) == 0:
        return []
    news_sorted = sorted(
        search,
        key=lambda news: news["comments_count"] + news["shares_count"],
        reverse=True,
    )
    results = [(news["title"], news["url"]) for news in news_sorted][:5]
    return results


# Requisito 11
def top_5_categories():
    categories = db.news.aggregate(
        [
            {"$unwind": "$categories"},
            {"$group": {"_id": "$categories", "total": {"$sum": 1}}},
            {"$sort": {"total": -1, "_id": 1}},
            {"$limit": 5},
            {"$project": {"category": "$_id"}},
        ]
    )
    return [news["category"] for news in categories]
