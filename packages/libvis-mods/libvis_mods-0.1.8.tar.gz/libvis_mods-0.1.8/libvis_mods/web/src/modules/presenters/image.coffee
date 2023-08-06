import React, { Component, createRef, useEffect} from 'react'
import L from 'react-dom-factories'
L_ = React.createElement



#export default class Vis extends React.Component
export default Vis = (props)->
  {data} = props
  ref = createRef()

  useEffect ()->
    {data} = props
    canvas = ref.current
    ctx = canvas.getContext "2d"
    
    if typeof(data[0])=='object'
      w = data[0].length
      h = data.length
      concat = (x,y)->x.concat y
      a = [255]
      if typeof(data[0][0])!='object'
        im = data
          .reduce concat
          .map (v)->[v,v,v,255]
          .reduce concat
      else
        im = data
          .reduce concat
          .map (v)->v.concat a
          .reduce concat
    else
      [w,h] = data[...2]

      im = data[2...]

    canvas.width =w
    canvas.height = h

    img = new ImageData(Uint8ClampedArray.from(im),w,h)
    ctx.putImageData img,0,0
    
  L.div className:'image',
    L.canvas ref:ref
