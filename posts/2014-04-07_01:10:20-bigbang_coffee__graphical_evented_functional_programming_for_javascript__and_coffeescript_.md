---
title: 'bigbang.coffee: graphical/evented functional programming for
        javascript (and coffeescript)'
category: dev
tags:
- dev
- lib
- fp
- functional
- coffeescript
- javascript
- bigbang

<style scoped> img[src*="bigbang"] {
  width: 100%; padding: 15px 100px;
} </style>

[bigbang.coffee](https://github.com/obfusk/bigbang.coffee) is a
coffeescript library that allows you to create graphical and evented
programs (like games) in coffeescript or javascript using plain
mathematical functions.  It was inspired by the 2htdp library for
racket.

![bigbang](/img/bigbang.svg)

The `bigbang` function starts a new universe whose behaviour is
specified by the options and handler functions designated.

* Purely functional event handlers like `on_tick` transform the world
  from one state to the next.
* The world is drawn on the appropriate canvas by the `to_draw`
  function.
* Clock ticks are optional and also provide "clock mode", where
  changes are queued and drawing happens every actual clock tick
  (which is useful for games).

&rarr; [annotated source](http://obfusk.github.io/bigbang.coffee)

---

## Examples

  &rarr; https://github.com/obfusk/bigbang-examples
  <br/>
  &rarr; http://bigbang-examples.herokuapp.com

#### bigbang-snake

  snake game w/ bigbang.coffee

  &rarr; https://github.com/obfusk/bigbang-snake
  <br/>
  &rarr; http://bigbang-snake.herokuapp.com

---

\- Felix

&rarr; [Comments](https://github.com/obfusk/obfusk.github.io/issues/3)
