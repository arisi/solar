Eye.application :solar do
  working_dir "/home/pi/solar"
  stdall "/var/log/solar.log"
  notify :errors
  trigger :flapping, times: 2, within: 1.minute, retry_in: 5.minutes
  check :cpu, every: 10.seconds, below: 100, times: 3 # global check for all processes

  process :solar_6969 do
    notify :dev
    notify :errors
    start_command "bundle exec ./solar.rb"
    daemonize true
    pid_file "/tmp/solar.pid"
  end
#  process :aurinkosaato6 do
#    notify :dev
#    notify :errors
#    auto_start  false
#    start_command "bundle exec ./aurinkosaato6.py"
#    daemonize true
#    pid_file "/tmp/rpoll.pid"
#  end
end
