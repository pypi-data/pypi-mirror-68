import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

import GridLayout from 'react-grid-layout'
#import ResponsiveGL from 'react-grid-layout'
import {Responsive, WidthProvider} from 'react-grid-layout'

ResponsiveGrid = WidthProvider Responsive

getFromLS = (key) ->
  if global.localStorage
    try
      ls = JSON.parse global.localStorage.getItem 'rgl'
    catch e
      log.error e
  ls?[key] or {}

saveToLS = (key, value) ->
  if global.localStorage
    x = [key]:value
    global.localStorage.setItem 'rgl',
      JSON.stringify( x )

originalLayouts = getFromLS("layouts") || {}

export default class ResponsiveGL extends React.PureComponent
  defaultProps =
    breakpoints:{lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0}
    cols:{lg: 18, md: 12, sm: 10, xs: 4, xxs: 2}
    rowHeight:60
    width:1000

  onLayoutChange: (layout, layouts)=>
    saveToLS 'layouts', layouts
    @setState layouts:layouts

  constructor:(props)->
    super(props)
    this.state = layouts: JSON.parse(JSON.stringify(originalLayouts))

  render: ->
    props = {
      @props...
      layouts:@state.layouts,
      onLayoutChange:@onLayoutChange,
    }
    L.div '',
      L_ ResponsiveGrid, props, @props.children
