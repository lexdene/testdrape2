do(jq=jQuery)->
  jq.fn.extend
    # options:
    #     url:
    #     params:
    newsfeed: (options={})->
      render_container this
      bind_events this, options
      fetch this, options
      this

  render_container = (jobj)->
    load_template()
    jobj.html container_template()
    jobj.data 'from_id', -1
    jobj

  bind_events = (jobj, options)->
    jobj.on 'click', '.load_more', (e)->
      e.preventDefault()

      $(this).hide()
      fetch jobj, options

  fetch = (jobj, options)->
    params = options['params'] || {}
    loading_obj = jobj.find('.loading')

    jq.delay
      action: (set_result)->
        loading_obj.show()

        params['from_id'] = jobj.data('from_id')
        jq.ajax
          url: WEB_ROOT + options['url'],
          data: params
          dataType: 'json'
          success: (data, status, xhr)->
            set_result
              errormsg: ''
              data: data
              now: xhr.getResponseHeader 'Date'
          error: ->
            set_result
              errormsg: '网络错误'
              data: []
      finish: (data)->
        loading_obj.hide()

        # error
        if data.errormsg != ''
          jobj.find('.errormsg').html(data.errormsg)
          jobj.find('.error').show()
          return

        # emtpy
        if data.data.length == 0
          jobj.find('.nomore').show()
          return

        # min from_id
        from_id = parseInt jobj.data('from_id')
        data.data.forEach (d)->
          if from_id == -1 or d.id < from_id
            from_id = d.id
        jobj.data 'from_id', from_id

        # render data
        jobj.find('.items-container').append render data
        jobj.find('.load_more').show()

  # global data
  container_template = null
  items_template = null

  load_template = ->
    if container_template == null
      container_template = _.template jq('#newsfeed-container-template').html()

    if items_template == null
      items_template = _.template jq('#newsfeed-items-template').html()

  render = (data)->
    _(data.data).each (value)->
      if value.from_object_type == 'topic' and value.action_type == 'reply'
        value.action_type = 'replied'

    items_template
      newsfeed_list: data.data
      format_date: jq.create_date_formater data.now
