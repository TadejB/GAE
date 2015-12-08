#!/usr/bin/env python
import os
import jinja2
import webapp2


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
        return self.render_template("base.html")

    def post(self):
        if self.request.get('addition'):
            result = float(self.request.get('first_number')) + float(self.request.get('second_number'))
        if self.request.get('subtraction'):
            result = float(self.request.get('first_number')) - float(self.request.get('second_number'))
        if self.request.get('multiplication'):
            result = float(self.request.get('first_number')) * float(self.request.get('second_number'))
        if self.request.get('division'):
            result = float(self.request.get('first_number')) / float(self.request.get('second_number'))

        params = {"result":result}

        return self.render_template('base.html', params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)


