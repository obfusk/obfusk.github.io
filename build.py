import json

from datetime import date
from jinja2   import Environment, FileSystemLoader, Markup, \
                     select_autoescape
from markdown import Markdown

def anchor(t):
  return "a_" + "_".join( "".join( c for c in s if c.isalnum() )
                          for s in t.lower().split() )

with open("data/repos.json") as f: repos = json.load(f)
with open("data/gists.json") as f: gists = json.load(f)

templates = "index blog repos".split()  # TODO: gists
data      = dict(
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
