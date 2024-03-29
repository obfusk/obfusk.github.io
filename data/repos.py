#!/usr/bin/python3

import json, sys
from collections import OrderedDict

with open("data/repos-cats.json") as f:
  cats = OrderedDict(json.load(f))
with open("data/repos-tags.json") as f:
  tags = json.load(f)
with open("data/repos-blacklist.json") as f:
  blacklist = set(json.load(f))

non_cat_tags  = set("clj cpp crate gem inactive js kt on-hold pypi " \
                    "unfinished uni wip 日本語".split())
unused_tags   = set("uni".split())
keys          = "name desc link lang info warn".split()

badges = dict(
  lang = "clj cpp hs js kt py rb rs sh crate gem pypi 日本語".split(),
  info = "inactive unfinished".split(),
  warn = "on-hold wip".split()
)

assert non_cat_tags & set(cats) == set()
assert all( any( c in v for c in cats ) for v in tags.values() )
assert all( t in cats or t in non_cat_tags
            for v in tags.values() for t in v )
assert (non_cat_tags - unused_tags) <= \
       set( t for ts in badges.values() for t in ts )

def repositories(repos):
  data = { x["name"]: OrderedDict( (k,x[k]) for k in keys if k in x )
           for x in repos }
  for k, v in data.items():
    if k not in tags and k not in blacklist:
      print("untagged (and not blacklisted):", k, file = sys.stderr)
    for c, bs in badges.items():
      l = [ b for b in bs if b in tags.get(k, ()) ]
      if l: v[c] = l
  for c, title in cats.items():
    elems = [ v for k,v in data.items() if c in tags.get(k, ()) ]
    yield OrderedDict([("title", title), ("elems", elems)])

GH_PRE = "https://github.com/obfusk/"

if __name__ == "__main__":
  with open("data/gh-repos.json") as f:
    gh_repos = json.load(f)
  gh_repos.sort(key = lambda x: x["name"])
  assert all( x["link"] == GH_PRE + x["name"] for x in gh_repos )
  repos = list(repositories(gh_repos))
  with open("data/repos.json", "w") as f:
    json.dump(repos, f, indent = 2); f.write("\n")
