from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape

templates = "index".split()
data      = dict(
  title     = '/var/log/obfusk',
  tagline   = 'hacking ⇒ ¬sleeping',
  name      = 'Felix C. Stegerman',
  year      = date.today().year,
  navs      = [
    dict(page = "index"   , link = "/"    , text = "Home"),
    dict(page = "old-blog", link = "/old" , text = "Old Blog"),
  ]
)

env = Environment(
  loader      = FileSystemLoader('templates'),
  autoescape  = select_autoescape()
)

for t in templates:
  print("building {}.html ...".format(t))
  template = env.get_template(t + '.html')
  with open('__html__/{}.html'.format(t), 'w') as f:
    template.stream(page = t, **data).dump(f)
