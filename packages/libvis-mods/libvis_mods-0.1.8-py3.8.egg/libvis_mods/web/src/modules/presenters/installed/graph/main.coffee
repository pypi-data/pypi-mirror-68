import React from 'react'
import * as Gv from './graph.coffee'
import './style.css'

export default Presenter = ({data, setattr}) =>
  console.log 'data is', data
  if data?.graph
    vis = Gv.start
        data:JSON.parse data.graph
        style:
          nodeColor: 'blue'
          lineColor: 'red'

  
  Gv.Ui w:'100%', h:'100%'
