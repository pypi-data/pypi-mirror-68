export get_nb_name=()->
  n = window.location.href.match(/p=(.+)&?/)?[1]
  n || ''



