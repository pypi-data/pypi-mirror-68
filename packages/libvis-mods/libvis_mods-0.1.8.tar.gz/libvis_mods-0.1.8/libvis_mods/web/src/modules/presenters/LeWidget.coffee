import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

import LeClient from 'legimens'

export wrapModuleWithLegimens = (Pres) => ({data, addr}) =>
  console.log 'wrapping pres', Pres
  L.div className:'wrapper',
    L_ LeClient, addr:addr, refval:data,
      (variable, setattr) =>
        console.log "in wrapper of #{Pres} variable #{variable}"
        if variable is undefined
          variable = value:'Loading', type:'raw'
          return "Loading"
        else
          try
            variable = JSON.parse variable
          catch
        L_ Pres, data:variable, addr:addr, setattr:setattr

