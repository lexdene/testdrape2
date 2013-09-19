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
      this.addClass('jf_flash_out')
      this.bind(
        "animationend webkitAnimationEnd oAnimationEnd MSAnimationEnd",
        ->
          me.removeClass('jf_flash_out')
      )

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

    delay: (time, action, finish)->
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

  true
