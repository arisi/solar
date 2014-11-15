#!/usr/bin/env ruby
#encoding: UTF-8

require 'redis'

$redis = Redis.new(:host => '127.0.0.1' ) #the address of rpoll's redis server '20.20.20.215'

kl=$redis.keys("teho:*")

kl.each do |k|
  stamp=k.gsub(/\D/,"")
  teho=$redis.get(k)
  
  i=$redis.get("i:#{stamp}")
  u=$redis.get("u:#{stamp}")
  valinta=$redis.get("valinta:#{stamp}")
  
  
  puts "#{stamp}00;#{teho};#{i};#{u};#{valinta}"

end

