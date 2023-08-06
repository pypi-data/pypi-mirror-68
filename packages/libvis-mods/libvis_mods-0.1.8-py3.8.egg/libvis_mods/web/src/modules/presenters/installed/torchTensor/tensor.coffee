import React from 'react'
import './style.less'

export default Presenter = ({data, setattr}) =>
  console.log 'data t', data
  if data is undefined
    return 'Connecting...'

  {tensor} = data
  if tensor is undefined
    return 'Waiting for tensor...'


  getMax = (a)=>
    return Math.max(...a.map((e) => if Array.isArray(e) then getMax(e) else e))
  getMin = (a)=>
    return Math.min(...a.map((e)=> if Array.isArray(e) then getMin(e) else e))

  getDimSum= (a)=>
    return if Array.isArray(a) then a.length + getDimSum(a[0]) else 1

  len = (getDimSum tensor)/10

  max = getMax(tensor)
  min = getMin(tensor)
  console.log 'max min', max, min
  range = max - min

  get_style=(val)=>
    return
      backgroundColor:"hsl(0,0%,#{20 + (val-min)/range*80}%)"
      fontSize: "#{25/len}px"
      padding: "#{20//len}px"
      margin: "#{20//len}px"
  <div className="torch-presenter">
    Torch tensor:
    <table>
      <tbody>
        {
            tensor.map (row, i)=>
              if Array.isArray row
                <tr key={i}>
                {
                  row.map (val, j) =>
                    <td style={get_style val} key={j}>{val.toFixed(3)}</td>
                }
                </tr>
              else
                <tr style={get_style row} key={i}>{row}</tr>
        }
      </tbody>
    </table>
  </div>
