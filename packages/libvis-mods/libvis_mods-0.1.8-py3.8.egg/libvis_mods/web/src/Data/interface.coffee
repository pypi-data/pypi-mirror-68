
export parse_message = (jsonser) ->
  try
    message = JSON.parse jsonser
  catch
    message = jsonser
    console.error message
    return name:null, value: null
  variable =
    name:  message.args
    value: message.value
    type:  message.type

  return variable

