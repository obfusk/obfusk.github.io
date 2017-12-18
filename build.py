from datetime import date
from jinja2   import Environment, FileSystemLoader, Markup, \
                     select_autoescape
from markdown import Markdown

def blog_header(date, title):
  anchor = "t_" + "_".join( "".join( c for c in s if c.isalnum() )
                            for s in title.lower().split() )
  return Markup(
    """<div class="anchor" id="{0}"></div>\n"""
    """## [{1}](#{0})\n"""
    """<small>[{2}]</small>"""
  .format(anchor, title, date))

templates = "index blog repos gists".split()
data      = dict(
  title       = "/var/log/obfusk",
  tagline     = "hacking ⇒ ¬sleeping",
  name        = "Felix C. Stegerman",
  year        = date.today().year,
  navs        = [
    dict(page = "index"   , link = "/"          , text = "Home"),
    dict(page = "blog"    , link = "/blog.html" , text = "Blog"),
    dict(page = "repos"   , link = "/repos.html", text = "Repositories"),
    dict(page = "gists"   , link = "/gists.html", text = "Gists"),
    dict(page = "old-blog", link = "/old"       , text = "Old Blog"),
  ],
  blog_header = blog_header,
  blog_sep    = Markup("""<hr class="blog_sep" />"""),
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
    template.stream(page = t, **data).dump(f)
    f.write("\n")
