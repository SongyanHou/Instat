
class User:
    def __init__(self):
        self.id = ""
        self.username = ""
        self.full_name = ""
        self.profile_picture = ""
        self.bio = ""
        self.website = ""
        self.counts = ""
        self.recent_media = ""
        self.liked = ""
        self.follows = ""
        self.followed_by = ""


class Tag(object):
    """docstring for Tag"""
    def __init__(self):
        super(Tag, self).__init__()
        self.media_count = 5
        self.recent_media = []


class Location(object):
    """docstring for Location"""
    def __init__(self):
        super(Location, self).__init__()
        self.recent_media = []


class Media(object):
    """docstring for Media"""
    def __init__(self):
        super(Media, self).__init__()
        self.type = ""
        self.filter = ""
        self.users_in_photo = ""
        self.tags = ""
        self.comments = ""
        self.caption = ""
        self.likes = ""
        self.link = ""
        self.user = ""
        self.id = ""
        self.location = ""
        self.created_time = ""
        self.image_thumb = ""
        self.image_low = ""
        self.image_standard = ""
        self.video_low = ""
        self.video_standard = ""

class Comment(object):
    """docstring for Comment"""
    def __init__(self):
        super(Comment, self).__init__()
        self.id = ""
        self.text = ""
        self.user = ""
        self.created_time = ""
        