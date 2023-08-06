import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

export default class Vis extends React.Component
  constructor:(props)->
    super props

  set_contents:()->
    if not @refs.frame
      return
    doc = @refs.frame.contentWindow.document
    doc.open()
    doc.write @props.data
    doc.close()

  componentDidMount:()->
    @set_contents()

  render:->
    @set_contents()
    L.div className: 'container',
      L.iframe className:'mpl',ref:'frame',
