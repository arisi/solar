
task = () ->
  $.ajax
    url: "/ajax" 
    type: "POST"
    success: (data) ->
      obj = jQuery.parseJSON(data)
      $("#teho").html(obj.teho)
      $("#kwh").html(obj.kwh)
      $("#pannu").html(obj.pannu)
      $("#patteri").html(obj.patteri)      
      $("#vertailuteho").html(obj.vertailuteho)
      $("#valinta").html(obj.valinta)
      $("#u").html(obj.u)
      $("#i").html(obj.i)
      $("#now").html(obj.now)

ennuste = () ->
  $.simpleWeather
    zipcode: ""
    woeid: "564851" #2357536
    location: ""
    unit: "c"
    success: (weather) ->
      html = "<h2>" + weather.temp + "&deg;" + weather.units.temp + "</h2>"
      html += "<ul>"
      html += "<li class=\"currently\">" + weather.currently + " -> " + weather.text + "</li>"
      html += "<li class=\"currently\">" + weather.humidity + "%</li>"
      html += "<li class=\"currently\">" + weather.wind.speed + " " + weather.wind.direction + "</li>"
      html += "</ul>"
      $("#weather").html html
      console.log weather
      return

    error: (error) ->
      $("#weather").html "<p>" + error + "</p>"
      return

$(document).ready ->
  setInterval (->
    task()
  ), 500
  ennuste()		  
  setInterval (->
    ennuste()
  ), 600000
