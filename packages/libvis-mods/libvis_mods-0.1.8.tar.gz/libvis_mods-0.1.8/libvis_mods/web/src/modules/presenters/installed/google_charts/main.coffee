import React from 'react'
import Chart from 'react-google-charts'

export default Presenter = ({data, setattr}) =>
  # Google charts redraw on 'resize' event
  # Since our chart is in a resizable container
  # Need to emulate resize event
  console.log data
  document.addEventListener('mouseup',
    ()=>window.dispatchEvent(new Event('resize'))
    )
  <Chart
    width="100%"
    height="100%"
    className="google-charts-presenter"
    chartType={data.type}
    data={data.data}
    options={{
      title:data.title
      hAxis: {title:data.hAxis}
      vAxis: {title:data.vAxis}
      chartArea: {'width': '90%', 'height': '80%'},
      legend: {'position': 'bottom'}
    }}
    />
