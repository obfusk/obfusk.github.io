#!/usr/bin/python3

import json, time
from collections import OrderedDict
from pathlib import Path

from . import gh

cat   = lambda t, e: OrderedDict([("title", t), ("elems", e)])
out   = Path("data/contribs.json")
cache = {}

def load_cache():
  with out.open() as f:
    for cat in json.load(f):
      for x in cat["elems"]: cache[x["name"]] = x

if out.exists() and time.time() - out.stat().st_mtime < 3600:
  print("*** using contribs cache ***")
  load_cache()

with open("data/contribs-blacklist.json") as f:
  blacklist = set(json.load(f))

def info(contrib):
  if contrib["name"] in cache:
    x = cache[contrib["name"]]
  else:
    x = gh.renamed(gh.get_repo_info(contrib["name"], verbose = True),
                   gh.repo_info_fields, gh.rename)
  assert x["link"] == gh.GH + "/" + x["name"]
  return x

def contributions(contribs):
  contribs_ = [ c for c in contribs if c["name"] not in blacklist ]
  direct_s  = set( c["name"] for c in contribs_ if c["contrib"] )
  direct    = [ info(c) for c in contribs_ if c["contrib"] ]
  indirect  = [ info(c) for c in contribs_ if not c["contrib"]
                        and not c["name"] in direct_s ]
  return [cat("Direct Contributions", direct),
          cat("Indirect Contributions | (e.g. Issues)", indirect)]

if __name__ == "__main__":
  with open("data/gh-contribs.json") as f:
    gh_contribs = json.load(f)
  with open("data/gh-contribs-add.json") as f:
    gh_contribs += json.load(f)
  gh_contribs.sort(key = lambda x: x["name"])
  contribs = list(contributions(gh_contribs))
  with out.open("w") as f:
    json.dump(contribs, f, indent = 2); f.write("\n")
