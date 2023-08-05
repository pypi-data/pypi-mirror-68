from defusedxml.ElementTree import XML

from myprss import logger


def parse_rss_content(data):
    rss = XML(data)

    if rss.get("version") != "2.0":
        logger.error("Only rss version 2.0 are supported for now")
        return

    channel = rss.find("channel")

    data = {}

    data["site"] = channel.find("title").text
    data["items"] = []

    for item in channel.findall("item"):
        data["items"].append(
            {
                "date": item.find("pubDate").text,
                "title": item.find("title").text,
                "url": item.find("link").text,
                "description": item.find("description").text,
            }
        )

    return data
