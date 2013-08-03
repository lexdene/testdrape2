do(jq=jQuery)->
  jq.extend
    version_cmp: (a,b)->
      arr_a = a.split('.')
      arr_b = b.split('.')
      while arr_a.length > 0
        if arr_b.length == 0
          return 1

        top_a = parseInt arr_a.shift()
        top_b = parseInt arr_b.shift()
        if top_a > top_b
          return 1
        else if top_a < top_b
          return -1

      if arr_b.length > 0
        return -1
      else
        return 0