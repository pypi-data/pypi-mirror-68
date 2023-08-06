import React from 'react'
import './style.css'

export default Presenter = ({data, setattr}) =>
  if data is undefined
    return "Loading..."
  <div className="{{cookiecutter.name}}-presenter">
    Random quote: `<p>{data.quote}</p>`
  </div>
