do(jq=jQuery)->
  jq.fn.extend
    refresh_img: ->
      src = jq(this).attr 'src'
      clean_src = src.split('?')[0]
      new_src = clean_src + '?t=' + (+new Date())
      jq(this).attr 'src', new_src

      this

    center_in_window: ->
      jwin = jq window
      jdoc = jq document
      jobj = this
      top = (jwin.height() - jobj.height()) / 2
      left = (jwin.width() - jobj.width()) / 2
      scroll_top = jdoc.scrollTop()
      scroll_left = jdoc.scrollLeft()

      jobj.css
        position: 'absolute'
        top: top + scroll_top
        left: left + scroll_left
      .show()

      this

    scroll_to: (elapse=300)->
      me = this
      target_top = this.offset().top - ($(window).height() - this.outerHeight(true)) / 2
      jq('body').animate
        scrollTop: target_top
      , elapse

      # flash out
      flash_out_class_name = 'jf_flash_out'
      this.removeClass flash_out_class_name
      this.css 'background-color', 'yellow'

      setTimeout =>
        this.addClass flash_out_class_name
        this.css 'background-color', ''
      ,100

      # return
      this

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

    delay: (options={})->
      # defaults
      time = options['time'] || 700
      action = options['action']
      finish = options['finish']

      result = undefined
      is_timer_finished = false

      load = ->
        if result and is_timer_finished
          finish result

      set_result = (r)->
        result = r
        load()

      action set_result

      timer = setTimeout ->
        is_timer_finished = true
        load()
      , time

    delay_ajax: (options={})->
      result = undefined
      is_timer_finished = false

      load = ->
        if result and is_timer_finished
          options['finish'].call this, result

      xhr = options['action'].call this
      xhr.success (data, status, xhr)->
        result =
          errormsg: ''
          data: data
          now: xhr.getResponseHeader 'Date'
          page: xhr.getResponseHeader 'X-Record-Page'
          per_page: xhr.getResponseHeader 'X-Record-PerPage'
          count: xhr.getResponseHeader 'X-Record-Count'
        load()
      .error (xhr)->
        result =
          errormsg: jq.error_msg xhr.status
        load()

      timer = setTimeout ->
        is_timer_finished = true
        load()
      , options['time'] || 700

    error_msg: (status_code)->
      map =
        401: '请先登录'
        500: '服务器错误，请联系客服'

      map[status_code] or "未知错误: #{status_code}"

  true
