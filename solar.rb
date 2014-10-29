#!/usr/bin/env ruby
#encoding: UTF-8

require 'sinatra'
require 'haml'
require 'coffee_script'
require 'redis'

$redis = Redis.new(:host => '127.0.0.1' ) #the address of rpoll's redis server '20.20.20.215'


$port=6969
if ARGV[0]
  set :haml, :ugly => :true
  set :haml, :remove_whitespace => :true
  set :environment, :production 
  $port=ARGV[0]
end
set :bind => "0.0.0.0", :port => $port
set :public_folder, 'public'

def get_or_post(path, opts={}, &block)
  get(path, opts, &block)
  post(path, opts, &block)
end

get '/' do
  haml :index
end

get_or_post "/ajax" do
  {kwh: $redis.get("kwh"), pannu: $redis.get("pannu"), patteri: $redis.get("patteri"),  now: $redis.get("now")}.to_json
end

get '/js/:name.js' do
  content_type 'text/javascript', :charset => 'utf-8'
  coffee(:"js/#{params[:name]}")
end

