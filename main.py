#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

import jinja2
import webapp2

from google.appengine.api import urlfetch


# Settings
DEVELOPMENT = True
DEFAULT_URL = "http://0.tqn.com/d/altreligion/1/0/_/1/-/-/circle.jpg" # "http://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Persian_Cat_%28kitten%29.jpg/411px-Persian_Cat_%28kitten%29.jpg"


# Initialise the templating system and load our main template
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
if not DEVELOPMENT:
    main_template = jinja_env.get_template("main.html")


class MainHandler(webapp2.RequestHandler):
    def get(self):
        if DEVELOPMENT:
            main_template = jinja_env.get_template("main.html")
        params = {"url": DEFAULT_URL}
        params.update(self.request.params)
        self.response.out.write(main_template.render(params))


class ImageHandler(webapp2.RequestHandler):
    def get(self):
        """Fetch an image from the specified URL, and return it.
        
        This pointless operation is needed to circumvent the
        browser’s same-origin policy.
        """
        url = self.request.get("url")
        response = urlfetch.fetch(url, deadline=60)
        if response.status_code != 200:
            self.response.status = 500
            self.response.out.write("Failed to fetch URL: response status "+str(response.status_code))
            return
        
        self.response.headers["Content-Type"] = response.headers["Content-Type"]
        self.response.out.write(response.content)


app = webapp2.WSGIApplication(
    [
        ('/',    MainHandler),
        ('/img', ImageHandler),
    ],
    debug=DEVELOPMENT
)
