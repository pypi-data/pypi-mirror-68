import React from 'react'
import './style.css'
import {LibvisModule} from 'libvis'

export default Presenter = ({data, setattr, addr}) =>
  if data is undefined
    return "Loading..."
  console.log 'data', data
  <div className='wrapper'>
    <LibvisModule object={data.body} addr={addr}/>
  </div>
