#!/usr/bin/python3

import json, sys
from collections import OrderedDict

cats = OrderedDict([                                            # {{{1
  ("!"          , "Featured"),
  (">"          , "Latest"),
  ("util"       , "Utilities"),
  ("dev"        , "Development"),
  ("py"         , "Python"),
  ("rb"         , "Ruby"),
  ("sh"         , "Bash"),
  ("lib"        , "Libraries"),
  ("fp"         , "Functional Programming"),
  ("game"       , "Games"),
  ("admin"      , "Server Administration"),
  ("fs"         , "Free Software & Privacy"),
  ("pres"       , "Presentations"),
  ("misc"       , "Miscellaneous"),
  ("nap"        , "Nap"),
  ("unfinished" , "Unfinished"),
])                                                              # }}}1

# non-category tags: clj cpp gem inactive js on-hold pypi uni wip

tags = {                                                        # {{{1
  "achatwithsinatra":               "rb pres".split(),
  "active-dump":                    "rb lib gem inactive".split(),
  "algorithms.cpp":                 "cpp inactive unfinished".split(),
  "algorithms.py":                  "py uni inactive".split(),
  "autossh-init":                   "sh admin !".split(),
  "baktogit":                       "sh admin".split(),
  "bash-cheatsheet":                "sh !".split(),
  "bash-presentation":              "sh pres".split(),
  "bigbang-examples":               "js fp game".split(),
  "bigbang-snake":                  "js fp game".split(),
  "bigbang.coffee":                 "js fp game lib inactive !".split(),
  "buffer-overflows-101":           "pres".split(),
  "bundler-fu":                     "rb lib gem inactive".split(),
  "clj-obfusk-data":                "clj lib inactive unfinished".split(),
  "cpbak":                          "sh admin".split(),
  "cryptanalysis.py":               "py uni inactive".split(),
  "cryptoparty-privacycafe-menu":   "fs !".split(),
  "cryptoparty-privacycafe-slides": "fs pres".split(),
  "dev-misc":                       "misc".split(),
  "dev-vm-ruby":                    "dev admin inactive".split(),
  "dns.py":                         "py uni".split(),
  "dotfiles":                       "misc".split(),
  "ds-lunch-talk-foss":             "fs pres".split(),
  "eft":                            "rb lib gem !".split(),
  "eft.sh":                         "sh lib !".split(),
  "eftcmdr":                        "rb lib gem".split(),
  "eftcmdr-nap":                    "rb lib nap".split(),
  "fnjs":                           "clj js dev unfinished on-hold".split(),
  "gitbak":                         "rb util gem !".split(),
  "gpg":                            "misc !".split(),
  "httpony":                        "py uni".split(),
  "i3-config":                      "misc".split(),
  "iot-tdose":                      "fs pres".split(),
  "keep-it-private":                "fs pres unfinished on-hold".split(),
  "koneko":                         "py dev wip >".split(),
  "localconfig-rails-example":      "rb lib inactive".split(),
  "m":                              "py util pypi ! >".split(),
  "mail-config":                    "misc !".split(),
  "mailer":                         "sh admin".split(),
  "manifest-dl":                    "rb lib gem inactive".split(),
  "map.sh":                         "sh util !".split(),
  "mdview":                         "rb util gem inactive".split(),
  "nametag":                        "rb util gem !".split(),
  "nap":                            "nap sh admin inactive".split(),
  "nap-app":                        "nap rb admin inactive".split(),
  "nap-hello":                      "nap inactive".split(),
  "napp":                           "nap rb admin unfinished on-hold".split(),
  "napp-hello-compojure":           "nap unfinished on-hold".split(),
  "napp-hello-express":             "nap unfinished on-hold".split(),
  "napp-hello-flask":               "nap unfinished on-hold".split(),
  "napp-hello-jetty":               "nap unfinished on-hold".split(),
  "napp-hello-nc":                  "nap unfinished on-hold".split(),
  "napp-hello-ncat":                "nap unfinished on-hold".split(),
  "napp-hello-rails":               "nap unfinished on-hold".split(),
  "napp-hello-sinatra":             "nap unfinished on-hold".split(),
  "napp-puppet":                    "nap admin unfinished on-hold".split(),
  "napp-server":                    "nap admin unfinished on-hold".split(),
  "netcat.py":                      "py uni".split(),
  "obfusk.coffee":                  "js fp inactive unfinished".split(),
  "obfusk.github.io":               "misc >".split(),
  "obfusk.py":                      "py fp pypi inactive unfinished".split(),
  "obfusk.rb":                      "rb fp gem inactive unfinished".split(),
  "open_uri_w_redirect_to_https":   "rb lib gem".split(),
  "phonegap-android-coffee-haml":   "misc".split(),
  "play-galgje":                    "js misc".split(),
  "pypride":                        "py uni".split(),
  "rb-localconfig":                 "rb lib gem inactive".split(),
  "rb-obfusk-data":                 "rb lib gem inactive unfinished".split(),
  "rb-obfusk-util":                 "rb lib gem inactive unfinished".split(),
  "scripts":                        "misc".split(),
  "sh-config":                      "misc".split(),
  "simple-stack-exploit":           "misc".split(),
  "siresta":                        "rb lib gem unfinished on-hold".split(),
  "snake.coffee":                   "js fp game".split(),
  "sniffer.py":                     "py uni".split(),
  "sokobang":                       "js fp game !".split(),
  "srvbak":                         "sh admin".split(),
  "stat":                           "sh admin".split(),
  "taskmaster":                     "sh admin util !".split(),
  "trcrt.py":                       "py uni".split(),
  "trstools.py":                    "py uni inactive unfinished".split(),
  "venv":                           "py dev util".split(),
  "webrtc-xftv":                    "misc".split(),
  "xuggle-frames-to-video":         "misc".split(),
}                                                               # }}}1

blacklist = set(                                                # {{{1
"""
  2des-attack __obfusk-cljs __test-cljs-2 ansible aruba-obfusk
  awesome-config belasting-vm bthesis bundler clj.rkt
  comfortable-mexican-sofa cryptanalysis dlthing flx-docs fnjs-app
  fnxnl fsfe-blog fsfe-business-card gastcollege_avans_20150313
  git-boot homebrew homebrew-devtap homebrew-tap hs-flx i3 ib2013vm
  mgit misc nap-misc nap-puppet obfusk.github.io-OLD
  open-ath9k-htc-firmware open_uri_redirections perl6intro
  phantomjs-gem play-chat play-cryptanalysis playing-with-factor
  pp-gitolite pp-meta pp-misc privacycafe-misc rack refactor.py remark
  rubies-bugs rvm-site sprockets stsffap vagrant vim-niji waltz
""".split())                                                    # }}}1

assert all( any( c in tags[k] for c in cats ) for k in tags )

keys    = "name desc link lang info warn".split()
badges  = dict(lang = "clj cpp js py rb sh gem pypi".split(),
               info = "inactive unfinished".split(),
               warn = "on-hold wip".split())

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
    elems = [ v for k,v in data.items() if c in tags.get(k, ())
              and (c == "nap" or "nap" not in tags[k]) ]
    yield OrderedDict([("title", title), ("elems", elems)])

if __name__ == "__main__":
  with open("data/gh-repos.json") as f:
    repos = list(repositories(json.load(f)))
  with open("data/repos.json", "w") as f:
    json.dump(repos, f, indent = 2); f.write("\n")
