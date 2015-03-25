__author__ = 'Jane'
from instagram.client import InstagramAPI


def show(tag_name):
    api = InstagramAPI(client_id='fae19a5f499c4aff820f71ce869e5579', client_secret='c3a8e0773e174a8caa2f785e9120d5b5')
    tag_search, next_tag = api.tag_search(q=tag_name)
    tag_recent_media, next_media = api.tag_recent_media(tag_name=tag_search[0].name)
    photos = []
    for tag_media in tag_recent_media:
        photos.append(tag_media.get_standard_resolution_url())
    print photos[0]

