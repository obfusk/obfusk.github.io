require 'haml'

desc 'serve w/ sinatra'
task :sinatra do
  require 'sinatra'
  set :public_folder, File.expand_path('..', __FILE__)
  get('/') { redirect '/index.html' }
  Sinatra::Application.run!
end
