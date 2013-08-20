# --                                                            ; {{{1
#
# File        : obfusk/vlo.rb
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2013-08-20
#
# Copyright   : Copyright (C) 2013  Felix C. Stegerman
# Licence     : GPLv2 or EPLv1
#
# --                                                            ; }}}1

require 'date'
require 'fileutils'
require 'pygments'
require 'redcarpet'
require 'yaml'

module Obfusk; module VLO

  class RedPyg < Redcarpet::Render::HTML
    def block_code(code, lang)
      Pygments.highlight code, lexer: lang
    end
  end

  MD = Redcarpet::Markdown.new(
    RedPyg, no_intra_emphasis: true, fenced_code_blocks: true,
    autolink: true, lax_spacing: true
  )

  # --

  def self.struct(*keys)
    s = Struct.new(*keys.map(&:to_sym))
    s.class_eval do
      def initialize(h = {})
        h.each_pair { |k,v| self[k] = v }
      end
      def check!
        each_pair { |k,v| v or raise 'empty!' }
        self
      end
    end
    s
  end

  # --

  POSTNAME = /^
    (?<date> \d\d\d\d - \d\d - \d\d ) _
    (?<time> \d\d : \d\d : \d\d ) - (?<rest> .* )
  $/x

  Config  = struct(*%w{ title tagline })
  Page    = struct(*%w{ hdr md name file order })
  Post    = struct(*%w{ hdr md name file dir title date tags cat })

  # --

  def self.build                                                # {{{1
    c = Config.new(YAML.load_file('config.yml'))
    FileUtils.mkdir_p 'html'
    layout            = get_layout :layout
    pages             = build_pages c, layout
    posts, cats, tags = build_posts c, layout
    build_archive_page  c, posts
    build_cats_page     c, cats
    build_tags_page     c, tags
    build_pages_page    c, pages
    build_index_page    c
  end                                                           # }}}1

  def self.build_pages(c, layout)                               # {{{1
    ps = Dir['pages/*.md'].sort.map do |p|
      x = load_page(p, File.read(p))
      write_file "html/#{x.file}", render_page(c, x, layout)
      x
    end.sort_by { |x| x.order }
  end                                                           # }}}1

  def self.build_posts(c, layout)                               # {{{1
    cats = {}; tags = {}
    ps = Dir['posts/*.md'].sort.each do |p|
      x = load_post(p, File.read(p))
      FileUtils.mkdir_p "html/#{x.dir}"
      write_file "html/#{x.file}", render_post(c, x, layout)
      (cats[x.cat] ||= []) << x
      x.tags.each do |t|
        (tags[t] ||= []) << x
      end
      x
    end
    [ps.reverse, cats, tags]
  end                                                           # }}}1

  def self.build_archive_page(c, posts)
  end

  def self.build_cats_page(c, cats)
  end

  def self.build_tags_page(c, tags)
  end

  def self.build_pages_page(c, pages)
  end

  def self.build_index_page(c)
    # render_page, load_page(
  end

  # --

  def self.load_page(p, s)                                      # {{{1
    hdr, md, name = load_yaml_md p, s
    Page.new(
      hdr: hdr, md: md, name: name, file: "#{name}.html",
      order: hdr['order']
    ).check!
  end                                                           # }}}1

  def self.load_post(p, s)                                      # {{{1
    hdr, md, nm   = load_yaml_md p, s
    m = nm.match(POSTNAME) or raise "invalid post name: #{nm}"
    name          = m[:rest]
    date          = DateTime.parse "#{m[:date]} #{m[:time]}"
    cat           = hdr['category']
    dir           = [cat,m[:date]]*'/'
    file          = "#{[dir,name]*'/'}.html"
    Post.new(
      hdr: hdr, md: md, name: name, file: file, dir: dir,
      title: hdr['title'], date: date, tags: hdr['tags'], cat: cat
    ).check!
  end                                                           # }}}1

  def self.load_yaml_md(p, s)
    hdr, md = s.split "\n\n", 2
    name    = File.basename(p, '.md')
    [YAML.load(hdr), md, name]
  end

  # --

  def self.render_page(c, p, layout)
    render_view :page, layout, config: c, page: p,
      html: render_md(p.md)
  end

  def self.render_post(c, p, layout)
    render_view :post, layout, config: c, post: p,
      html: render_md(p.md)
  end

  # --

  def self.render_view(name, layout, locals = {})
    p = render_haml get_haml(File.read("views/#{name}.haml")), locals
    render_haml(layout, locals) { p }
  end

  def self.get_layout(name)
    get_haml File.read("views/_#{name}.haml")
  end

  # --

  def self.render_md(s)
    MD.render s
  end

  def self.render_haml(h, locals = {}, &b)
    h.render Object.new, locals, &b
  end

  def self.get_haml(s)
    Haml::Engine.new s
  end

  # --

  def self.write_file(f, s)
    puts "--> #{f}"
    File.write f, s
  end

  def self.safe_title(s)
    s.gsub /[^A-Za-z0-9_-]/, '_'
  end

end; end

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
