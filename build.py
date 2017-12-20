#!/usr/bin/python3

import json

from datetime import date
from jinja2   import Environment, FileSystemLoader, Markup, \
                     select_autoescape
from markdown import Markdown
from pathlib  import Path

def anchor(t):
  return "a_" + "_".join( "".join( c for c in s if c.isalnum() )
                          for s in t.lower().split() )

def blog_post(t):
  head, body = t.split("\n---\n", 1)
  info       = { k.strip(): v.strip() for k,v in ( l.split(":", 1)
                 for l in head.splitlines() if l.strip() ) }
  return dict(date = info["date"], title = info["title"], body = body)

with open("data/repos.json") as f: repos = json.load(f)
with open("data/gists.json") as f: gists = json.load(f)

blog_posts    = [ blog_post(f.read_text())
                  for f in sorted(Path("blog").glob("*.md"),
                                  key = lambda f: f.name) ]
templates     = "index blog repos".split()  # TODO: gists
data          = dict(                       # TODO: declare in .json?
  title       = "/var/log/obfusk",
  tagline     = "hacking ⇒ ¬sleeping",
  name        = "Felix C. Stegerman",
  year        = date.today().year,
  navs        = [
    dict(page = "index"   , link = "/"          , text = "Home"),
    dict(page = "blog"    , link = "/blog.html" , text = "Blog"),
    dict(page = "repos"   , link = "/repos.html", text = "Repositories"),
#   dict(page = "gists"   , link = "/gists.html", text = "Gists"),
    dict(page = "old-blog", link = "/old"       , text = "Old Blog"),
  ],
  ptitles     = dict(repos = "repositories"),
  anchor      = lambda t: Markup(anchor(t)),
  repos       = repos,
  gists       = gists,
  blog_posts  = blog_posts,
)

md  = Markdown(output_format = "xhtml5",
               extensions = "extra codehilite".split())
env = Environment(loader = FileSystemLoader("templates"),
                  autoescape = select_autoescape())
env.filters["markdown"] = lambda s: Markup(md.convert(s))

for t in templates:
  print("building {}.html ...".format(t))
  template = env.get_template(t + ".html")
  with open("__html__/{}.html".format(t), "w") as f:
    template.stream(page = t, **data).dump(f); f.write("\n")
