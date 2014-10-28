
task = () ->
  $.ajax
    url: "/ajax" 
    type: "POST"
    success: (data) ->
      obj = jQuery.parseJSON(data)
      $("#tick").html(obj.tick)
      $("#temp").html(obj.temp)
      $("#now").html(obj.now)

$(document).ready ->
  timer=setInterval (->
    task()
  ), 500
			  
  
