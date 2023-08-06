export default class Chainer
  constructor: ->
    @chain = []
  append:(func)=>
    @chain.push func
  call: (args...)->
    for f in @chain
      f(args...)


