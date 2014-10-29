require 'eye-http'

Eye.config do
  http :enable => true, :host => "0.0.0.0", :port => 12345
  logger '/var/log/eye.log'
  mail :host => "mail.voicestream.fi", :port => 25, :domain => "lnx.fi", :from_mail => "eye@lnx.fi"
  contact :errors, :mail, 'kristola.ari@gmail.com', :from_mail => "eye@lnx.fi"
  contact :dev, :mail, 'kristola.ari@gmail.com', :from_mail => "eye@lnx.fi"
end

Eye.load('/etc/eye/*.eye')
