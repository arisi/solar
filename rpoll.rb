#!/usr/bin/env ruby
#encoding: UTF-8

require 'redis'
require 'time'

$tick=0
$temp=0

$redis = Redis.new(:host => 'localhost' )

$mode=ARGV[0]||="sim"
puts "rpoll starting in mode #{$mode}"

def stamp
  return DateTime.now.strftime.gsub(/\D/,'')[0..11]
end

if $mode!='sim'
  require 'bcm2835'
  include Bcm2835
end

loop do
  sleep 1
  if $mode=='sim'
    $temp=40+Random.rand(10)
    $kwh=2.0+Random.rand(10)/10.0
  else
    pin = 17
    GPIO.output(pin)
    SPI.begin do |spi| 
      $spi=spi.read       # returns 1 byte
      #puts spi.read(1) # returns an array of 1024 bytes 
    end
    puts "poll: #{$tick} #{$spi}"
  end
  ss=stamp
  puts "loop #{$tick} #{ss}"
  
  $redis.set "tick",$tick
  $redis.set "kwh",$kwh
  $redis.set "pannu",$temp
  $redis.set "patteri",$temppatteri
  
  $redis.set "kwh:#{ss}",$kwh
  $redis.expire("kwh:#{ss}", 60*60*24*2)
  
  $redis.set "pannu:#{ss}",$temp
  $redis.expire("pannu:#{ss}", 60*60*24*2)

  $redis.set "patteri:#{ss}",$temppatteri
  $redis.expire("patteri:#{ss}", 60*60*24*2)
  
  $redis.set "now",ss
  $tick+=1
end
