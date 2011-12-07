import json
import logging
import webapp2
from models import Entry
from markupsafe import escape
from google.appengine.api import users


# =============================================================================
# Resources

class JsonResource(webapp2.RequestHandler):
    def is_admin(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return False
        if not users.is_current_user_admin():
            logging.info('Non-admin user attempted privileged operation:')
            logging.info('User: [%s]' % user.email())
            self.response.set_status(403)
            self.send_json({'error': 'must be logged in as an administrator'})
            return False
        return True

        
    def send_json(self, struct):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(struct))


class EntriesResource(JsonResource):
    def get(self):
        entry_id = self.request.get('entry_id')
        if entry_id:
            try:
                entry_id = int(entry_id)
            except:
                self.response.set_status(400)
                return
            entry = Entry.get_by_id(entry_id)
            if not entry:
                self.response.set_status(404)
                return
            self.send_json(entry.to_dict())
            return
        
        count = self.request.get('count')
        page = self.request.get('page')
        try:
            count = int(count) if count else 20
            page = int(page) if page else 0
        except:
            self.response.set_status(400)
            return
        entries = Entry.get_latest(count, page)
        self.send_json([e.to_dict() for e in entries])

    def post(self):
        if not self.is_admin():
            return
        slug = self.request.get('slug')
        title = self.request.get('title')
        content = self.request.get('content')
        if not slug or not title or not content:
            self.response.set_status(400)
            return
        try:
            entry = Entry.new(slug, title, content)
        except Exception as e:
            logging.info('Failed to create new entry: %s' % e)
            self.response.set_status(403)
            self.send_json({'error': str(e)})
            return
        self.send_json(entry.to_dict())

    def put(self):
        if not self.is_admin():
            return
        try:
            entry_id = int(self.request.get('entry_id'))
        except:
            self.response.set_status(400)
            return
        slug = self.request.get('slug')
        title = self.request.get('title')
        content = self.request.get('content')
        if not slug or not title or not content:
            self.response.set_status(400)
            return
        entry = Entry.get_by_id(entry_id)
        if not entry:
            self.response.set_status(404)
            return
        try:
            entry.update(slug, title, content)
        except Exception as e:
            logging.info('Failed to update entry %s: %s' % (entry_id, e))
            self.response.set_status(403)
            self.send_json({'error': str(e)})
            return
        self.send_json(entry.to_dict())

    def delete(self):
        if not self.is_admin():
            return
        try:
            entry_id = int(self.request.get('entry_id'))
        except:
            self.response.set_status(400)
            return
        entry = Entry.get_by_id(entry_id)
        if not entry:
            self.response.set_status(404)
            return
        entry.delete()


# =============================================================================
# Routes

app = webapp2.WSGIApplication([('/entries', EntriesResource)])
