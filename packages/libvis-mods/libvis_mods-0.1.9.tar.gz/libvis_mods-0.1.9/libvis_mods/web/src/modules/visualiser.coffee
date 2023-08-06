import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement
import Input from './UIcomponents/input.coffee'
import LineGraph from './presenters/lineGraph_recharts.coffee'
import MplD3 from './presenters/mpld3.coffee'
import Image from './presenters/image.coffee'
import * as Modules from './presenters'
import {installed} from './presenters'
Object.assign( Modules, installed )
console.log(Modules)

get_var_type = (type, val)->
  if type=='mpl'
    return 'MplD3'
  if type=='img'
    return 'Image'
  if val is null
    return 'Raw'
  try
    if val.length>10
      if val[0].length>10
        return 'Image'
  catch
  if Array.isArray(val)
    return 'LineGraph'
  if type=='raw'
    return 'Raw'
    
  return type

export choosePresenter = (type, val)->
  type = get_var_type type, val
  console.log "Choosing presenter for '#{type}' value", val, "from", Modules
  presenter = Modules[type]
  if presenter
    return presenter
  else
    return ({data})->L.div 0,JSON.stringify data

export LibvisModule = ({object, addr})->
  if object is undefined
    type= 'Raw'
    value = null
  else
    {type, value} =  object

  Pres = choosePresenter type, value
  L.div className:'libvismod',
    L_ Pres, data:value, addr:addr
