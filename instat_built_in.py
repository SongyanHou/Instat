__author__ = 'Jane'
from instagram.client import InstagramAPI
from show_function import show_image

def show(tag_name):
    api = InstagramAPI(client_id='fae19a5f499c4aff820f71ce869e5579', client_secret='c3a8e0773e174a8caa2f785e9120d5b5')
    tag_search, next_tag = api.tag_search(q=tag_name)
    tag_recent_media, next_media = api.tag_recent_media(tag_name=tag_search[0].name)
    media = []
    for tag_media in tag_recent_media:
        media.append(tag_media.get_standard_resolution_url())
    show_image(media[0])
    print media[0]

if __name__ == '__main__':
    show("helloworld")

def search(user=None, location=None, tag_name=None, start_time=None, end_time=None):
    api = InstagramAPI(client_id='fae19a5f499c4aff820f71ce869e5579', client_secret='c3a8e0773e174a8caa2f785e9120d5b5')
    media = set()
    if user:
        user_search, next_ = api.user_search(q=user.name)
        user_recent_media, next_media = api.user_recent_media(user_id=user_search[0].id)
        user_set = set()
        for user_media in user_recent_media:
            user_set.add(user_media.get_standard_resolution_url())
        if user_set:
            media = media | user_set
    if location:
        location_search, next_ = api.location_search(lat=location.lat, lng=location.long)
        location_recent_media, next_media = api.location_recent_media(location_id=location_search[0].id)
        location_set = set()
        for location_media in location_recent_media:
            location_set.add(location_media.get_standard_resolution_url())
        if location_set:
            if not media:
                media = media | location_set
            else:
                media = media & location_set
    if tag_name:
        tag_search, next_ = api.tag_search(q=tag_name)
        tag_recent_media, next_media = api.tag_recent_media(tag_name=tag_search[0].name)
        tag_set = set()
        for tag_media in tag_recent_media:
            tag_set.add(tag_media.get_standard_resolution_url())
        if tag_set:
            if not media:
                media = media | tag_set
            else:
                media = media & tag_set
    return media