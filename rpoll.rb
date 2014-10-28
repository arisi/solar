#!/usr/bin/env ruby
#encoding: UTF-8

require 'redis'
require 'bcm2835'
require 'time'
include Bcm2835

$tick=0
$temp=0

$redis = Redis.new(:host => 'localhost' )

$mode=ARGV[0]||="sim"
puts "rpoll starting in mode #{$mode}"

def stamp
  return DateTime.now.strftime.gsub(/\D/,'')[0..11]
end

loop do
  sleep 1
  if $mode=='sim'
    $temp=40+Random.rand(10)
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
  $redis.set "KWH",$tick
  $redis.set "PANNU",$temp
  $redis.set "NOW",ss
  $tick+=1
end
