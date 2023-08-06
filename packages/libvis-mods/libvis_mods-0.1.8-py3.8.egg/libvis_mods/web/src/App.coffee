import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

import {Responsive, WidthProvider} from 'react-grid-layout'

import LeClient from 'legimens'

import Notebook from './modules/notebook.coffee'
import {LibvisModule} from './modules/visualiser.coffee'
import ResponsiveGL from './modules/ResponsiveStorageGrid.coffee'
import Widget from './modules/Widget.coffee'
import TopBar from './modules/topbar.coffee'

import LocalStorage from './modules/helpers/localStorage.coffee'
import {get_nb_name} from './modules/helpers/argparser.coffee'
import {parse_message} from './Data/interface.coffee'

import './styles/grid.css'
import './styles/widget.less'
import './styles/graph.less'
import './styles/misc.less'
import './styles/top_bar.less'

visStorage = new LocalStorage key:'webvis'


export default class App extends React.Component
  state: {
    addr:'ws://localhost:7700/'
  }
  constructor:->
    super()
    @state.widgets = visStorage.get('widgets') or {}

  set_widgets:(widgets)->
    @setState {widgets}
    visStorage.save 'widgets', widgets

  nameChange: (id)=>(name)=>
    console.log 'namechange',@state.widgets
    @state.widgets[id].name = name
    @set_widgets @state.widgets

  addWidget: ()=>
    new_widget = name:'variable name'
    new_id = Date.now()
    @state.widgets[new_id] = new_widget
    @set_widgets @state.widgets

  deleteWidget: (id)->()=>
    console.log "Deleting widget #{id}"
    delete @state.widgets[id]
    @set_widgets @state.widgets

  _widget: (var_, name, idx) =>
    Widget
      key: idx
      onDelete: @deleteWidget idx
      onNameChange: @nameChange idx
      name: name
      LibvisModule object:var_, addr:@state.addr

  _get_widgets:(vars)=>
    nb = L.div key:'notebook', L_ Notebook, nb_name:get_nb_name()
    widgets = [nb]

    for idx, params of @state.widgets
      {name} = params
      variable = vars?[name] or value:'No value',type:'raw'

      widgets.push @_widget variable, name, idx
    return widgets

  _grid:(vars)->
    L_ ResponsiveGL,
      className:'grid'
      draggableCancel:".container, input"
      @_get_widgets vars

  render: ->
    {addr} = @state
    L.div className:'app',
      L_ TopBar,
        addr:addr
        addWidget:@addWidget
        addrChange:(addr)=>@setState {addr}
      L_ LeClient, addr:addr, refval:'',
      (root, setattr) =>
        console.log 'root ref', root
        if not root
          return @_grid()
        L_ LeClient, addr:addr, refval:root.root,
          (vars, setattr) =>
            console.log 'vars', vars
            if not vars
              return 'Loading...'
            @_grid vars
