#!/usr/bin/python3

import json
from collections import OrderedDict

from . import gh

cat = lambda t, e: OrderedDict([("title", t), ("elems", e)])

with open("data/contribs-blacklist.json") as f:
  blacklist = set(json.load(f))

def info(contrib):
  x = gh.renamed(gh.get_repo_info(contrib["name"], verbose = True),
                 gh.repo_info_fields, gh.rename)
  assert x["link"] == gh.GH + "/" + x["name"]
  return x

def contributions(contribs):
  contribs_ = [ c for c in contribs if c["name"] not in blacklist ]
  direct    = [ info(c) for c in contribs_ if c["contrib"] ]
  indirect  = [ info(c) for c in contribs_ if not c["contrib"] ]
  return [cat("Direct Contributions", direct),
          cat("Indirect Contributions (e.g. Issues)", indirect)]

if __name__ == "__main__":
  with open("data/gh-contribs.json") as f:
    gh_contribs = json.load(f)
  with open("data/gh-contribs-add.json") as f:
    gh_contribs += json.load(f)
  gh_contribs.sort(key = lambda x: x["name"])
  contribs = list(contributions(gh_contribs))
  with open("data/contribs.json", "w") as f:
    json.dump(contribs, f, indent = 2); f.write("\n")
