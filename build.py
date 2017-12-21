#!/usr/bin/python3

import json

from collections  import OrderedDict
from datetime     import date
from jinja2       import Environment, FileSystemLoader, Markup, \
                         select_autoescape
from markdown     import Markdown
from pathlib      import Path

def anchor_id(t):
  return "a_" + "_".join( "".join( c for c in s if c.isalnum() )
                          for s in t.lower().split() )

def blog_post(t):
  head, body = t.split("\n---\n", 1)
  info       = { k.strip(): v.strip() for k,v in ( l.split(":", 1)
                 for l in head.splitlines() if l.strip() ) }
  return dict(date = info["date"], title = info["title"], body = body)

with open("data/repos.json")    as f: repos     = json.load(f)
with open("data/gists.json")    as f: gists     = json.load(f)
with open("data/contribs.json") as f: contribs  = json.load(f)

blog_posts    = [ blog_post(f.read_text())
                  for f in sorted(Path("blog").glob("*.md"),
                                  key = lambda f: f.name) ]

templates     = "index blog repos contribs".split() # TODO: gists
data          = dict(                               # TODO: .json?
  title       = "/var/log/obfusk",
  tagline     = "hacking ⇒ ¬sleeping",
  name        = "Felix C. Stegerman",
  year        = date.today().year,
  navs        = OrderedDict([
    ("index"    , dict(link = "/"             , text = "Home")),
    ("blog"     , dict(link = "/blog.html"    , text = "Blog")),
    ("repos"    , dict(link = "/repos.html"   , text = "Repositories")),
#   ("gists"    , dict(link = "/gists.html"   , text = "Gists")),
    ("contribs" , dict(link = "/contribs.html", text = "Contributions")),
    ("old-blog" , dict(link = "/old"          , text = "Old Blog")),
  ]),
  ptitles     = dict(repos    = "repositories",
                     contribs = "contributions"),
  repos       = repos,
  gists       = gists,
  contribs    = contribs,
  blog_posts  = blog_posts,
)

md  = Markdown(output_format  = "xhtml5",
               extensions     = "extra codehilite".split())
env = Environment(loader      = FileSystemLoader("templates"),
                  autoescape  = select_autoescape())
env.filters["markdown"]       = lambda s: Markup(md.convert(s))
env.globals["anchor_id"]      = lambda t: Markup(anchor_id(t))

for t in templates:
  print("building {}.html ...".format(t))
  template = env.get_template(t + ".html")
  with open("__html__/{}.html".format(t), "w") as f:
    template.stream(page = t, **data).dump(f); f.write("\n")
