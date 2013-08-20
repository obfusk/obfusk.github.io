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

  class Pygments < Redcarpet::Render::HTML
    def block_code(code, lang)
      Pygments.highlight code, lexer: lang
    end
  end

  MD = Redcarpet::Markdown.new(
    Pygments, no_intra_emphasis: true, fenced_code_blocks: true,
    autolink: true, lax_spacing: true
  )

  Page  = Struct.new :file, :order
  Post  = Struct.new :file, :dir, :date, :tags, :cat

  # --

  def self.build                                                # {{{1
    c = YAML.load_file 'config.yml'
    layout            = get_layout :index
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
      x = load_page(p, File.read p)
      File.write "html/#{x.file}", render_page(x, layout)
      x
    end.sort_by { |x| x.order }
  end                                                           # }}}1

  def self.build_posts(c, layout)                               # {{{1
    cats = []; tags = []
    ps = Dir['posts/*.md'].sort.each do |p|
      x = load_post(p, File.read p)
      FileUtils.mkdir_p "html/#{p.dir}"
      File.write "html/#{x.file}", render_post(x, layout)
      (cats[x.cat] ||= []) << x
      x.tags.each |t| do
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
  end

  # --

  def self.load_page(p, s)
    hdr, md, title = load_yaml_md p, s
    Page.new "#{title}.html", hdr[:order]
  end

  def self.load_post(p, s)                                      # {{{1
    hdr, md, title  = load_yaml_md p, s
    cat             = hdr[:category]
    date            = DateTime.parse hdr[:date]
    dir             = [cat,date]*'/'
    file            = "#{[dir,title]*'/'}.html"
    Post.new file, dir, date, hdr[:tags], cat
  end                                                           # }}}1

  def self.load_yaml_md(p, s)
    hdr, md = s.split '\n\n', 2
    title   = File.basename(s, '.md').gsub(/[^A-Za-z0-9_-]/, '_')
    [hdr, md, title]
  end

  # --

  def self.render_page(p, layout)
    render_view :page, layout, page: p
  end

  def self.render_post(p, layout)
    render_view :post, layout, post: p
  end

  # --

  def self.render_view(name, layout, locals = {})
    render_haml layout, locals do
      render_haml get_haml(File.read("views/#{name}.haml")), locals
    end
  end

  def self.get_layout(name)
    get_haml File.read("views/_#{name}.haml")
  end

  # --

  def self.render_md(s)
    MD.render s
  end

  def self.render_haml(h, locals = {}, &b)
    h.render Object.new locals: locals, &b
  end

  def self.get_haml(s)
    Haml::Engine.new s
  end

end; end

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
