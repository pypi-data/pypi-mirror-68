import React from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

export default Vis = (props)->
  {data} = props
  if typeof data == 'object'
    data = JSON.stringify data
  data
