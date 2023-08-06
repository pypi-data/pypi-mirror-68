import Input from './UIcomponents/input.coffee'
import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

withDeleteButton = (onDelete, children)->
  L.div className:'wrapper',
    L.div
      className:'delete-card'
      onClick:onDelete
      'x'
    children

withName = (name, onNameChange, children)->
  L.div className:'wrapper',
    L.div className:'title',
      "Name: "
      L_ Input, value:name, onChange:onNameChange
    children

export default Widget = (props, children)->
  {variable, name, onNameChange, onDelete} = props
  L.div className:'widget', key:props.key,
    withDeleteButton onDelete,
      withName name, onNameChange,
        L.div className:'container',
          children
