import requests
import utils
import concurrent.futures


with concurrent.futures.ThreadPoolExecutor() as executor:
    top_stories = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    ).json()
    futures = []
    # Get top stories from Hacker News, filtering out already submitted posts
    for post_id in top_stories[:5]:
        print(f"Getting post: {post_id}")
        futures.append(executor.submit(utils.get_url_stories, post_id=post_id))

    print(f"Fetched {len(futures)} posts")
    story_posts = list(
        filter(
            None,
            [future.result() for future in concurrent.futures.as_completed(futures)],
        )
    )

    # Archive posts
    futures = []
    print(f"About to archive {len(list(story_posts))} posts")
    for post in story_posts:
        print(f"Archiving post: {post['id']}")
        futures.append(executor.submit(utils.archive_post, post=post))

print(f"Archived {len(futures)} posts")
archived_posts_to_submit = [
    future.result() for future in concurrent.futures.as_completed(futures)
]

for post in archived_posts_to_submit:
    print("Original url: ", post["url"], "Archived url: ", post["archive_url"])
