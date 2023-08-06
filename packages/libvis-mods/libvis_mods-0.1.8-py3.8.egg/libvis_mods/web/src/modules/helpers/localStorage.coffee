export default class LocalStorage
  constructor:(props)->
    @key = props.key

  get:(key) ->
    if global.localStorage
      try
        ls = JSON.parse global.localStorage.getItem @key
      catch e
        log.error e
    ls?[key]

  save:(key, value) ->
    if global.localStorage
      x = [key]:value
      global.localStorage.setItem @key,
        JSON.stringify( x )
  

