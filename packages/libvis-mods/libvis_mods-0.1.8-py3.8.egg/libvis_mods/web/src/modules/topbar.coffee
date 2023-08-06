import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

import Input from './UIcomponents/input.coffee'
import Button from './UIcomponents/button.coffee'

export default topbar=({addr,addWidget,addrChange})=>
    L.div className:'top-bar',
      L.div className:'address inline',
        L_ Input,
          value: addr
          onChange:addrChange
      L_ Button,
        className: 'add-widget'
        text: 'Add widget'
        onPress: addWidget
