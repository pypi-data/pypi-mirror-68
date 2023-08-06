import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement
import Input from './UIcomponents/input.coffee'
import Button from './UIcomponents/button.coffee'

export default class WebSocketWrapper extends React.Component
  constructor:(props)->
    super(props)
    @state =
      status:0
      addr:"#{window.location.hostname}:7700"


    @onError = props.onError
    {@onConnect, @onMessage} = props
    {@onDisconnect} = props


  handleMessage:(msg)=>
    @onMessage? msg

  handleError:(error)=>
    @setState status:3
    @onError? error
    console.error error

  handleConnect:()=>
    console.log 'ws connected'
    @setState status:2
    @onConnect? @ws

  handleDisconnect:()=>
    console.log 'ws disconnected'
    @setState status:0
    @onDisconnect?()

  disconnect:()=>
    @ws.close()
    @setState status:0

  connect:()=>
    {addr} = @state
    @setState status:1
    @ws = new WebSocket 'ws://'+addr
    @ws.onerror = @handleError
    @ws.onmessage = @handleMessage
    @ws.onclose = @handleDisconnect
    @ws.onopen = @handleConnect

  makeAction:=>
    switch @state.status
      when 0 then @connect()
      when 1 then @disconnect()
      when 2 then @disconnect()

  get_status_text:->
    switch @state.status
      when 0 then 'Connect'
      when 1 then 'Connecting...'
      when 2 then 'Disconnect'
      when 3 then 'Error'

  render:() ->
    L.div className:'webSocket '+@props.className,
      if @state.status!=2
        L_ Input,
          value:@state.addr
          onChange:(val)=>@setState addr:val
      else
        L.span style:color:'green',margin:10,
        "Connected"
      L_ Button,
        onPress:@makeAction
        text:@get_status_text()
