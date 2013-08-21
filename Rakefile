require 'haml'

$:.unshift File.expand_path('../lib', __FILE__)
require 'obfusk/vlo'

desc 'new post'
task :post do                                                   # {{{1
  title = ENV['TITLE'].to_s ; raise 'empty TITLE' if title.empty?
  cat   = ENV['CAT'].to_s   ; raise 'empty CAT'   if cat.empty?
  tags  = ENV['TAGS'].to_s.split /[\s,]+/
  date  = Time.now.strftime '%F_%T'
  safe  = Obfusk::VLO.safe_title title
  f     = "posts/#{date}-#{safe}.md"
  y     = { 'title' => title, 'category' => cat, 'tags' => tags } \
            .to_yaml
  p     = "...\n"
  raise "existing file: #{f}" if File.exists? f
  Obfusk::VLO.write_file f, "#{y}\n#{p}"
end                                                             # }}}1

desc 'new page'
task :page do                                                   # {{{1
  name  = ENV['NAME'].to_s  ; raise 'empty NAME' if name.empty?
  title = ENV['TITLE'].to_s ; title = name if title.empty?
  f     = "pages/#{name}.md"
  y     = { 'title' => title } .to_yaml
  p     = "...\n"
  raise "existing file: #{f}" if File.exists? f
  Obfusk::VLO.write_file f, "#{y}\n#{p}"
end                                                             # }}}1

desc 'new special'
task :special do                                                # {{{1
  name  = ENV['NAME'].to_s  ; raise 'empty NAME' if name.empty?
  title = ENV['TITLE'].to_s ; title = name if title.empty?
  f     = "specials/#{name}.haml"
  y     = { 'title' => title } .to_yaml
  p     = <<-END .gsub(/^ {4}/, '')
    %h1&= special.title
    %hr
    %p ...
  END
  raise "existing file: #{f}" if File.exists? f
  Obfusk::VLO.write_file f, "#{y}\n#{p}"
end                                                             # }}}1

desc 'build website'
task :build do
  Obfusk::VLO.build
end

desc 'cleanup'
task :clean do
  sh 'rm -fr _/ *.html'
end

desc 'serve w/ sinatra'
task sinatra: :build do
  require 'sinatra'
  set :public_folder, File.expand_path('..', __FILE__)
  get('/') { redirect '/index.html' }
  Sinatra::Application.run!
end
