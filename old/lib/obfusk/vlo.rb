# --                                                            ; {{{1
#
# File        : obfusk/vlo.rb
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2013-08-21
#
# Copyright   : Copyright (C) 2013  Felix C. Stegerman
# Licence     : GPLv2
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

  def self.struct(*keys)                                        # {{{1
    s = Struct.new(*keys.map(&:to_sym))
    s.class_eval do
      def initialize(h = {})
        h.each_pair { |k,v| self[k] = v }
      end
      def check!
        each_pair { |k,v| v.nil? and raise 'empty!' }
        self
      end
    end
    s
  end                                                           # }}}1

  # --

  POSTNAME = /^
    (?<date> \d\d\d\d - \d\d - \d\d ) _
    (?<time> \d\d : \d\d : \d\d ) - (?<rest> .* )
  $/x

  FIX_PATH = -> x { x.gsub(%r{/{2,}}, '/').sub(%r{^\./}, '') }

  Config  = struct(*%w{ title tagline copyright })
  Extra   = struct(*%w{ posts cats tags pages specials nav })
  Post    = struct(*%w{ hdr md   name file link dir date
                        title cat tags })
  Page    = struct(*%w{ hdr md   name file link title nav order
                        view })
  Special = struct(*%w{ hdr haml name file link title nav order })

  # --

  def self.build                                                # {{{1
    c = Config.new(YAML.load(read_file('config.yml'))).check!
    x = Extra.new
    x.posts, x.cats, x.tags = load_posts
    x.pages                 = load_pages
    x.specials              = load_specials
    x.nav                   = (x.pages + x.specials) \
                                .reject { |x| !x.nav } \
                                .sort_by { |x| x.order }
    x.check!
    layout                  = get_layout :layout
    FileUtils.mkdir_p 'html'
    write_file 'css/pygments.css',
      Pygments.css('.highlight', style: 'autumn') \
        unless File.exists? 'css/pygments.css'
    build_posts     c, x, x.posts   , layout
    build_pages     c, x, x.pages   , layout
    build_specials  c, x, x.specials, layout
  end                                                           # }}}1

  # --

  def self.build_posts(c, x, ps, layout)
    ps.each do |p|
      FileUtils.mkdir_p "html/#{p.dir}"
      write_html p.file, render_post(c, x, p, layout)
    end
  end

  def self.build_pages(c, x, ps, layout)
    ps.each do |p|
      write_html p.file, render_page(c, x, p, layout)
    end
  end

  def self.build_specials(c, x, ss, layout)
    ss.each do |s|
      write_html s.file, render_special(c, x, s, layout)
    end
  end

  # --

  def self.load_posts                                           # {{{1
    cats = {}; tags = {}
    ps = Dir['posts/*.md'].sort.map do |f|
      load_post(f, read_file(f))
    end .sort_by { |p| p.date }
    ps.each do |p|
      (cats[p.cat] ||= []) << p
      p.tags.each { |t| (tags[t] ||= []) << p }
    end
    [ps.reverse, cats, tags]
  end                                                           # }}}1

  def self.load_pages
    Dir['pages/*.md'].sort.map do |f|
      load_page(f, read_file(f))
    end .sort_by { |p| p.order }
  end

  def self.load_specials
    ss = Dir['specials/*.haml'].sort.map do |f|
      load_special(f, read_file(f))
    end .sort_by { |s| s.order }
  end

  # --

  def self.load_post(p, s)                                      # {{{1
    hdr, md, nm   = load_yaml_data p, s, '.md'
    m = nm.match(POSTNAME) or raise "invalid post name: #{nm}"
    name          = m[:rest]
    date          = DateTime.parse "#{m[:date]} #{m[:time]}"
    cat           = hdr['category']
    dir           = ['_',cat,m[:date]]*'/'
    file          = "#{[dir,name]*'/'}.html"
    link          = "/#{file}"
    Post.new(
      hdr: hdr, md: md, name: name, file: file, link: link, dir: dir,
      date: date, title: hdr['title'], cat: cat, tags: hdr['tags']
    ).check!
  end                                                           # }}}1

  def self.load_page(p, s)                                      # {{{1
    hdr, md, name = load_yaml_data p, s, '.md'
    path          = hdr['path'] || '.'
    file          = FIX_PATH["#{path}/#{name}.html"]
    link          = "/#{file}"
    nav           = hdr['nav'].nil? ? true : hdr['nav']
    order         = hdr['order'] || 999
    view          = hdr['view'] || :page
    Page.new(
      hdr: hdr, md: md, name: name, file: file, link: link,
      title: hdr['title'], nav: nav, order: order, view: view
    ).check!
  end                                                           # }}}1

  def self.load_special(p, s)                                   # {{{1
    hdr, haml, name = load_yaml_data p, s, '.haml'
    path            = hdr['path'] || '.'
    file            = FIX_PATH["#{path}/#{name}.html"]
    link            = "/#{file}"
    nav             = hdr['nav'].nil? ? true : hdr['nav']
    order           = hdr['order'] || 999
    Special.new(
      hdr: hdr, haml: haml, name: name, file: file, link: link,
      title: hdr['title'], nav: nav, order: order
    ).check!
  end                                                           # }}}!

  def self.load_yaml_data(p, s, ext)
    hdr, data = s.split "\n\n", 2
    name      = File.basename(p, ext)
    [YAML.load(hdr), data, name]
  end

  # --

  def self.render_post(c, x, p, layout)
    render_view :post, layout, config: c, extra: x,
      title: p.title, html: render_md(p.md),
      link: p.link, post: p
  end

  def self.render_page(c, x, p, layout)
    render_view p.view, layout, config: c, extra: x,
      title: p.title, html: render_md(p.md),
      link: p.link, page: p
  end

  def self.render_special(c, x, s, layout)
    render_haml_w_layout s.haml, layout, config: c, extra: x,
      title: s.title, link: s.link, special: s
  end

  # --

  def self.render_view(name, layout, locals = {})
    render_haml_w_layout read_file("views/#{name}.haml"), layout,
      locals
  end

  def self.render_haml_w_layout(s, layout, locals = {})
    p = render_haml get_haml(s), locals
    render_haml(layout, locals) { p }
  end

  def self.get_layout(name)
    get_haml read_file("views/#{name}.haml")
  end

  # --

  def self.render_md(s)
    MD.render s
  end

  def self.render_haml(h, locals = {}, &b)
    h.render Object.new, locals, &b
  end

  def self.get_haml(s)
    Haml::Engine.new s, escape_html: true
  end

  # --

  def self.read_file(f)
    File.read(f).force_encoding 'utf-8'
  end

  def self.write_html(f, s)
    write_file "html/#{f}", s
  end

  def self.write_file(f, s)
    puts "--> #{f}"
    File.write f, s
  end

  def self.safe_title(s)
    s.gsub /[^A-Za-z0-9_-]/, '_'
  end

  def self.replace(c, s)
    s.gsub('*TITLE*', c.title).gsub('*TAGLINE*', c.tagline)
  end

end; end

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
