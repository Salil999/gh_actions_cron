import requests
from time import sleep
from waybackpy import WaybackMachineCDXServerAPI
from waybackpy import WaybackMachineSaveAPI
from waybackpy.exceptions import NoCDXRecordFound


def get_url_stories(post_id):
    print(f"Making request for post: {post_id}")
    post = requests.get(
        f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json"
    ).json()
    if post.get("type", None) != "story":
        return None
    if post.get("url", None) is None:
        return None
    return post


def archive_post(post):
    try:
        # post is already archived
        checker = WaybackMachineCDXServerAPI(post["url"], max_tries=20)
        archive_url = checker.newest().archive_url
        post["archive_url"] = archive_url
    except NoCDXRecordFound as e:
        # post needs to be archived
        save_api = WaybackMachineSaveAPI(post["url"], max_tries=20)
        save_api.save()
        post["archive_url"] = save_api.archive_url
    except Exception as e:
        print(f'Failed to archive post: {post["url"]}', e)
        post["archive_url"] = None
    return post
