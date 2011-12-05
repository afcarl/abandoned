import webapp2
import logging


def entries_redirect(handler, *args, **kwargs):
    requested = handler.request.uri
    return requested.replace('entries', '#entries')


def handle_404(request, response, exception):
    logging.debug('Request for non-existent resource: %s' % request.uri)
    return webapp2.redirect('/404')


app = webapp2.WSGIApplication([
        webapp2.Route('/entries',
                      handler=webapp2.RedirectHandler,
                      defaults={'_uri': '/#entries'}),
        webapp2.Route('/entries/<keyname>',
                      handler=webapp2.RedirectHandler,
                      defaults={'_uri': entries_redirect}),
        webapp2.Route('/archive',
                      handler=webapp2.RedirectHandler,
                      defaults={'_uri': '/#archive'}),
        ], debug=True)


app.error_handlers[404] = handle_404
