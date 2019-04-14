import sys 
import feedparser
from markdownify import markdownify as md
import hashlib
from pyjekyll import * 

url = sys.argv[1]
site_path = sys.argv[2]

NewsFeed = feedparser.parse(url)
entries = NewsFeed.entries
site = JekyllSite(site_path)
post_container = site.get_post_container()
for entry in entries:
    # print(entry.title)
    tohash = entry.title
    contents = ""
    for c in entry.content:
        m = md(c["value"])
        # print(m)
        tohash += m
        contents += m
    hash_object = hashlib.md5(tohash.encode())
    res = (hash_object.hexdigest())
    #print("Hash: %s" % res)
    # print("-" * 20)
    if res not in [post.get_filename() for post in post_container.get_posts()]:
        print("Creating new post: %s" % entry.title)
        my_post = post_container.get_post(res)
        my_post.set_title(entry.title)
        my_post.set_contents(contents)
        my_post.save()