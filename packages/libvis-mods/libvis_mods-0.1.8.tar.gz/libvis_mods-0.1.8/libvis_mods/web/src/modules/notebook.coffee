import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

export default Notebook = (props) ->
  {nb_name} = props
  addr = "http://#{window.location.hostname}:8888/notebooks/" + nb_name
  L.div className:'widget',
    L.div className:'container jupyter',
      L.iframe
       src:addr
       style:
         position:'relative'
         width:'100%'
         height:'100%'
