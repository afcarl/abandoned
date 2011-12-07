import datetime
from google.appengine.ext import db


# =============================================================================
# Exceptions

class InvalidSlugError(Exception):
    def __init__(self, slug):
        self.slug = slug

    def __str__(self):
        return 'Invalid slug: %s' % self.slug


class SlugCollisionError(Exception):
    def __init__(self, slug):
        self.slug = slug

    def __str__(self):
        return 'Slug exists for this month/year: %s' % self.slug


# =============================================================================
# Helper functions

def validate_slug(slug):
    # TODO: check slug content
    now = datetime.datetime.now()
    if Entry.get_by_path(now.year, now.month, slug):
        raise SlugCollisionError(slug)


# =============================================================================
# Datastore entities

class Entry(db.Model):
    slug = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)

    def to_dict(self):
        return {
            'slug': self.slug,
            'title': self.title,
            'content': self.content,
            'created': str(self.created),
            'updated': str(self.updated),
            'entry_id': self.key().id()
            }

    def update(slug, title, content):
        validate_slug(slug)
        self.slug = slug
        self.title = title
        self.content = content
        self.put()

    @staticmethod
    def new(slug, title, content):
        validate_slug(slug)
        e = Entry(slug=slug, title=title, content=content)
        e.put()
        return e

    @staticmethod
    def get_by_path(year, month, slug):
        q = Entry.all()
        q.filter('slug =', slug)
        for entry in q:
            date = entry.created
            if date.month == month and date.year == year:
                return entry

    @staticmethod
    def get_latest(count=20, page=0):
        q = Entry.all()
        q.order('-created')
        return q.fetch(count, page * count)
