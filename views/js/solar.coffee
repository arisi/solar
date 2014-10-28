
task = () ->
  $.ajax
    url: "/ajax" 
    type: "POST"
    success: (data) ->
      obj = jQuery.parseJSON(data)
      $("#kwh").html(obj.kwh)
      $("#pannu").html(obj.pannu)
      $("#now").html(obj.now)

$(document).ready ->
  timer=setInterval (->
    task()
  ), 500
			  
  
