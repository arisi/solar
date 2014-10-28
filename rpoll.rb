#!/usr/bin/env ruby
#encoding: UTF-8

require 'redis'
require 'bcm2835'
include Bcm2835

$tick=0
$spi=0

$redis = Redis.new(:host => 'localhost' )

loop do
  sleep 1
  pin = 17
  GPIO.output(pin)
  SPI.begin do |spi| 
    $spi=spi.read       # returns 1 byte
    #puts spi.read(1) # returns an array of 1024 bytes 
  end
  puts "poll: #{$tick} #{$spi}"
  $redis.set "tick",$tick
  $redis.set "spi",$spi
  $tick+=1
end
