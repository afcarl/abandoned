import os
import jinja2
from webapp2 import Route, RequestHandler, RedirectHandler, WSGIApplication
from models import Entry


# =============================================================================
# Configuration

PAGE_SIZE = 20
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))


# =============================================================================
# Web pages

class Page(RequestHandler):
    def not_found(self):
        self.response.set_status(404)
        template = jinja.get_template('404.html')
        self.response.out.write(template.render())


class MainPage(Page):
    def get(self):
        page = self.request.get('page')
        count = self.request.get('count')
        try:
            page = int(page) if page else 0
            count = int(count) if count else models.PAGE_SIZE
        except:
            self.response.set_status(400)
            return
        entries = Entry.get_latest(count, page)
        template = jinja.get_template('index.html')
        self.response.out.write(template.render(entries))


class EntryPage(Page):
    def get(self, *args, **kwargs):
        try:
            year = int(kwargs['year'])
            month = int(kwargs['month'])
            slug = kwargs['slug']
        except:
            self.response.set_status(400)
            return
        entry = Entry.get_by_path(year, month, slug)
        if not entry:
            self.not_found()
            return
        template = jinja.get_template('entry.html')
        self.response.out.write(template.render(entry))


class UnknownPage(Page):
    def get(self):
        self.not_found()


# =============================================================================
# Routes

app = WSGIApplication([
        Route('/entry/<year:\d{4}>/<month:\d{2}>/<slug>', EntryPage),
        ('/', MainPage),
        ('/.*', UnknownPage),
        ])
