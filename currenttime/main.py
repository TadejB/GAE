#!/usr/bin/env python
import os
import jinja2
import webapp2
from datetime import datetime

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        now = datetime.now()
        hour = now.hour+1
        minute = now.minute
        sec = now.second

        if hour < 10:
            hour = "%s%s" % ("0", hour)
        if minute < 10:
            minute = "%s%s" % ("0", minute)
        if sec < 10:
            sec = "%s%s" % ("0", sec)
        if hour == 24:
            hour = "00"

        params = {
            "sporocilo": "%s:%s:%s" % (hour, minute, sec)
        }
        return self.render_template("index.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
