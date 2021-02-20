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
  if not contrib["gh"]:
    return { k: v for k, v in contrib.items()
                  if k in "name desc link".split() }
  elif contrib["name"] in cache:
    x = cache[contrib["name"]]
  else:
    x = gh.renamed(gh.get_repo_info(contrib["name"], verbose = True),
                   gh.repo_info_fields, gh.rename)
  assert x["link"] == gh.GH + "/" + x["name"]
  return x

def contributions(contribs):
  direct_s  = set( c["name"] for c in contribs if c["contrib"] )
  direct    = [ info(c) for c in contribs if c["contrib"] ]
  indirect  = [ info(c) for c in contribs if not c["contrib"]
                        and not c["name"] in direct_s ]
  return [cat("Direct Contributions", direct),
          cat("Indirect Contributions | (e.g. Issues)", indirect)]

if __name__ == "__main__":
  with open("data/gh-contribs.json") as f:
    contribs = json.load(f)
  contribs = [ c for c in contribs if c["name"] not in blacklist ]
  with open("data/gh-contribs-add.json") as f:
    contribs += json.load(f)
  for c in contribs: c["gh"] = True
  with open("data/non-gh-contribs.json") as f:
    non_gh = json.load(f)
    for c in non_gh: c["gh"] = False
    contribs += non_gh
  assert len(set( c["name"] for c in contribs )) == len(contribs)
  contribs.sort(key = lambda x: x["name"])
  data = contributions(contribs)
  with out.open("w") as f:
    json.dump(data, f, indent = 2); f.write("\n")
