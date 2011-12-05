import datetime
import cgi
import webapp2
import logging
import json
from google.appengine.api import users
from google.appengine.ext import db


MAX_KEY_LENGTH = 20


class Entry(db.Model):
    created = db.DateTimeProperty(required=True, auto_now_add=True)
    content = db.TextProperty(required=True)
    title = db.StringProperty(required=True)
    labels = db.ListProperty(db.Category)
    links = db.StringListProperty()
    prev_entry = db.SelfReferenceProperty(collection_name='Prev')
    next_entry = db.SelfReferenceProperty(collection_name='Next')

    def to_dict(self):
        data = {'created': str(self.created),
                'content': self.content,
                'title': self.title,
                'labels': self.labels,
                'links': self.links,
                'keyname': str(self.key().name())}
        if self.prev_entry:
            data['prev'] = str(self.prev_entry.key().name())
        if self.next_entry:
            data['next'] = str(self.next_entry.key().name())
        return data

    @staticmethod
    def get_recent(count):
        q = Entry.all()
        q.order('-created')
        return q.fetch(count)

    @staticmethod
    def build_key(title):
        replace = '!@#$%^&*()_+<>?:",./;\'[]\\{}|-='
        keyname = reduce(lambda s, r: s.replace(r, ''), replace, title)
        keyname = keyname.replace(' ', '-')
        keyname = keyname.lower()
        keyname = cgi.escape(keyname)[:MAX_KEY_LENGTH]
        if Entry.get_by_key(keyname):
            count = 1
            while Entry.get_by_key('%s-%d' % (keyname, count)):
                count += 1
            keyname = '%s-%d' % (keyname, count)
        return keyname

    @staticmethod
    def get_by_key(keyname):
        key = db.Key.from_path('Entry', keyname)
        return Entry.get(key)

    @staticmethod
    def new(title, content, labels, links):
        keyname = Entry.build_key(title)
        entry = Entry(key_name=keyname,
                      title=title,
                      content=content,
                      labels=[db.Category(l) for l in labels],
                      links=links)

        store = [entry]
        
        results = Entry.get_recent(1)
        if results:
            prev = results[0]
            entry.prev_entry = prev.key()
            prev.next_entry = db.Key.from_path('Entry', keyname)
            store.append(prev)

        db.put(store)
        return entry


class EntriesResource(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        params = self.request.params
        if 'keyname' in kwargs:
            keyname = kwargs['keyname']
            entry = Entry.get_by_key(keyname)
            if not entry:
                msg = 'Failed to get entry %s (does not exist)' % keyname
                logging.debug(msg)
                self.response.status = '404 %s' % msg
                return

            self.response.out.write(json.dumps([entry.to_dict()]))
        else:
            try:
                count = int(params['count']) if 'count' in params else 3
            except Exception as e:
                msg = 'Failed to get entries (bad request)'
                logging.debug('%s: %s' % (msg, e))
                self.response.status = '400 %s' % msg
                return

            results = Entry.get_recent(count)
            entries = [entry.to_dict() for entry in results]
            self.response.out.write(json.dumps(entries))


    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        if not users.is_current_user_admin():
            msg = 'Attempted post by unauthorized user: %s' % user.email()
            logging.debug(msg)
            self.response.status = '401 %s' % msg
            return

        params = self.request.params
        try:
            data = json.loads(params['data'])
            title = data['title']
            content = cgi.escape(data['content'])
            labels = data['labels']
            links = data['links']
        except Exception as e:
            msg = 'Failed to create entry (bad request)'
            logging.debug('%s: %s' % (msg, e))
            self.response.status = '400 %s' % msg
            return

        entry = Entry.new(title, content, labels, links)
        self.response.out.write(json.dumps(entry.to_dict()))

    def delete(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        if not users.is_current_user_admin():
            msg = 'Attempted post by unauthorized user: %s' % user.email()
            logging.debug(msg)
            self.response.status = '401 %s' % msg
            return

    def put(self, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        if not users.is_current_user_admin():
            msg = 'Attempted post by unauthorized user: %s' % user.email()
            logging.debug(msg)
            self.response.status = '401 %s' % msg
            return


app = webapp2.WSGIApplication([
        webapp2.Route('/api/entries', handler=EntriesResource),
        webapp2.Route('/api/entries/<keyname>', handler=EntriesResource),
        ], debug=True)
