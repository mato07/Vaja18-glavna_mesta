#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


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
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class GlavnoMesto:
    def __init__(self, gl_mesto, drzava, slika):
        self.gl_mesto = gl_mesto
        self.drzava = drzava
        self.slika = slika

def vnos_podatkov():
    lj = GlavnoMesto("Ljubljana", "Slovenija", "/assets/slike/ljubljana.jpg")
    bu = GlavnoMesto("Budimpesta", "Madzarska", "/assets/slike/budimpesta.jpg")
    du = GlavnoMesto("Dunaj", "Avstrija", "/assets/slike/dunaj.jpeg")
    be = GlavnoMesto("Berlin", "Nemcija", "/assets/slike/berlin.jpg")
    pa = GlavnoMesto("Pariz", "Francija", "/assets/slike/pariz.jpg")
    ri = GlavnoMesto("Rim", "Italija", "/assets/slike/rim.jpg")

    return [lj, bu, du, be, pa, ri]


class MainHandler(BaseHandler):
    def get(self):
        gl_mestece = vnos_podatkov()[random.randint(0,5)]
        info = {"mestece": gl_mestece}
        return self.render_template("zacetna_stran.html",info)

class UgibajHandler(BaseHandler):
    def post(self):
        ugibano = self.request.get("mesto")
        preveri_drzavo = self.request.get("preveri")

        glavna_mesta = vnos_podatkov()
        for item in glavna_mesta:
            if item.drzava == preveri_drzavo:
                if item.gl_mesto.lower() == ugibano.lower():
                    result = True
                else:
                    result = False
                info = {"rezultat": result, "enota": item}

                return self.render_template("ugibalna_stran.html", info)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/ugibaj', UgibajHandler),
], debug=True)
