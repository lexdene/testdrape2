do(jq=jQuery)->
  no_more_html = '<div class="nomore">没有更多新鲜事了</div>'
  more_button_html = '<a href="#" class="load_more">更多新鲜事</a>'

  newsfeed_template = null

  jq ->
    newsfeed_template = _.template jq('#newsfeed_template').html()

  newsfeed_area = null
  request_url = null
  request_params = {}
  from_id = -1

  render = (data)->
    _(data.data).each (value)->
      if value.from_object_type == 'topic' and value.action_type == 'reply'
        value.action_type = 'replied'

    newsfeed_template
      newsfeed_list: data.data
      format_date: jq.create_date_formater data.now

  bind_events = ->
    newsfeed_area.on 'click', '.load_more', (e)->
      e.preventDefault()
      jq(this).remove()
      fetch()

  fetch = ->
    loading_obj = jq dje.loading_html
    jq.delay 1000, (set_result)->
      newsfeed_area.append loading_obj

      request_params['from_id'] = from_id
      jq.getJSON(
        WEB_ROOT + request_url,
        request_params
      ).success (data)->
        set_result
          errormsg: ''
          data: data
      .error ->
        set_result
          errormsg: '网络错误'
          data: []
    ,(data)->
      # remove loading
      loading_obj.remove()

      # error
      if data.errormsg != ''
        newsfeed_area.append dje.error_msg_html
          msg: data.errormsg
        return

      # empty
      if data.data.length == 0
        newsfeed_area.append no_more_html
        return

      # min from_id
      data.data.forEach (d)->
        if from_id == -1 or d.id < from_id
          from_id = d.id

      newsfeed_area.append render data
      newsfeed_area.append more_button_html

  dje.newsfeed = (area, url, params)->
    newsfeed_area = area
    request_url = url
    request_params = params || {}

    bind_events()
    newsfeed_area.html ''
    fetch()
