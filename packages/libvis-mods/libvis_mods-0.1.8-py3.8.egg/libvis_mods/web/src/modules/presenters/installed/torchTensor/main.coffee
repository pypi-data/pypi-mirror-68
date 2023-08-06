import React from 'react'
import Tensor from './tensor.coffee'
import './style.less'
import {Widget} from 'libvis'

export default ModelPresenter = ({data, setattr, addr}) =>
  {model} = data

  if model is undefined
    return 'Wait...'

  console.log 'model', model

  style = width:'100%',height:'100%', overflow: 'auto'
  <div style={style} className="torch-model-presenter">
    Torch model:
      {JSON.stringify model}
    <div>
        {
          model.value.map (item, idx) =>
            <div>
              <p> {item[0]} </p>
              <Widget addr={addr} refval={item[1]}>
              {
                (variable, setattr) -> <Tensor data={variable}/>
              }
              </Widget>
            </div>
        }
    </div>
  </div>
