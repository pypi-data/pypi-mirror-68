import React from 'react'
import {LibvisMod} from 'libvis'
import './style.css'

export default Meta = ({data, setattr, addr}) =>
  console.log 'data', data
  if data
    <div className="meta_module-presenter">
      List:
      <div className='submod' >
        <LibvisMod addr={addr} object={data.list}/>
      </div>
      Chart:
      <div className='submod' >
        <LibvisMod addr={addr} object={data.chart}/>
      </div>
    </div>
