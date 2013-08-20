require 'haml'

$:.unshift File.expand_path('../lib', __FILE__)
require 'obfusk/vlo'

desc 'new page'
task :page do                                                   # {{{1
  name  = ENV['NAME'].to_s  ; raise 'empty NAME' if name.empty?
  title = ENV['TITLE'].to_s ; title = name if title.empty?
  f     = "pages/#{name}.md"
  y     = { 'title' => title, 'order' => -1 } .to_yaml
  p     = <<-END .gsub(/^ {4}/, '')
    # My new page

    ...
  END
  raise "existing file: #{f}" if File.exists? f
  Obfusk::VLO.write_file f, "#{y}\n#{p}"
end                                                             # }}}1

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
  p     = <<-END .gsub(/^ {4}/, '')
    # My new post

    ...
  END
  raise "existing file: #{f}" if File.exists? f
  Obfusk::VLO.write_file f, "#{y}\n#{p}"
end                                                             # }}}1

desc 'build website'
task :build do
  Obfusk::VLO.build
end

desc 'build website'
task :clean do
  sh 'rm -fr html/ index.html'
end

desc 'serve w/ sinatra'
task sinatra: :build do
  require 'sinatra'
  set :public_folder, File.expand_path('..', __FILE__)
  get('/') { redirect '/index.html' }
  Sinatra::Application.run!
end
