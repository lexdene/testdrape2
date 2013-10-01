do(jq=jQuery)->
  extend_option = (options)->
    default_option =
      success: ->
        action = get_action_name this
        alert "#{action}成功"
        window.location.reload()
      failed: (type, msg)->
        '''
          type: post/network/validate
        '''
        action = get_action_name this
        switch type
          when 'post'
            alert "#{action}失败: #{msg}"
          when 'network'
            alert "网络错误，请联系网站管理员"
          when 'validate'
            true
        true
      validate: {}
      before_submit: ->
        true
      loading_text: 'loading'
      validate_code: false

    jq.extend default_option, options

  bind_events = (jobj, options)->
    # submit
    jobj.submit (e)->
      e.preventDefault()
      ajax_submit jq(this), options

    # remove error hint
    jobj.on 'click focus', '.jf_line', remove_error_hint

    # refresh val code
    if options.validate_code
      jobj.find('.jf_valcode_btn').click (e)->
        e.preventDefault()

        jobj.find('.jf_valcode_input').val ''
        jobj.find('.jf_valcode_img').refresh_img()

    true

  ajax_submit = (form, options)->
    options.before_submit.call form
    params = get_form_params form
    validate_result = validate_params params, options.validate
    if not validate_result.result
      show_all_error_hint form, validate_result
      on_failed form, 'validate', '填写内容不合格', options
      return

    form.add_mask
      type: 'loading'
      text: options.loading_text

    jq.post(
      form.attr('action'),
      jq.param(params),
      null,
      'json'
    ).success( (data)->
      form.remove_mask()
      if data.result == 'success'
        options.success.call form
      else
        on_failed form, 'post', data.msg, options
    ).error( ->
      form.remove_mask()
      on_failed form, 'network', '系统错误', options
    )

  get_form_params = (form)->
    return form.serializeArray()

  validate_methods =
    notempty: (val)->
      if val == ''
        return '内容不能为空'
      else
        return true
    int: (val)->
      if val.match /^[0-9]+$/
        return true
      else
        return '内容必须为数字'
    len: (val, argv)->
      bottom = argv[0]
      top = argv[1]
      if val == undefined
        length = 0
      else
        length = val.length
      if length < bottom or length > top
        return "长度必须在[#{bottom}, #{top}]之间，您输入的长度为#{length}"
      else
        return true
    equal: (val, argv, form_data)->
      equal_name = argv[0]
      equal_title = argv[1]
      equal_val = form_data[equal_name]
      if val == equal_val
        return true
      else
        return "内容必须和#{equal_title}相同"

  validate_params = (origin_params, validate_option)->
    params = {}
    jq.each origin_params, (index, area)->
      name = area.name

      # 以[]结尾的是一个list
      if '[]' == name.substr -2
        list_name = name.substr 0, name.length-2
        if list_name not of params or not _.isArray params[list_name]
          params[list_name] = []
        params[list_name].push area.value
      else
        params[name] = area.value

    result =
      result: true
      illegal_area: []

    jq.each validate_option, (area_name, area_validate)->
      area_val = params[area_name]
      area_title = area_validate['title']
      jq.each area_validate.validates, (index, validate_method)->
        method_name = validate_method[0]
        method = validate_methods[method_name]
        if method == undefined
          result.result = false
          result.illegal_area.push
            name: area_name
            msg: "未知认证: #{method_name}"
        else
          r = method area_val, validate_method.slice(1), params
          if r != true
            result.result = false
            result.illegal_area.push
              name: area_name
              msg: r

    result

  remove_error_hint = ->
    line = jq this
    line.find('.jf_error').remove()
    clear_form_error line.closest('form')

  show_error_hint = (msg)->
    line = jq this
    line.append "<span class='jf_error'>#{msg}</span>"

  show_all_error_hint = (form, validate_result)->
    jq.each validate_result.illegal_area, (index, area)->
      line = form.find(".jf_input[name=#{area.name}]").closest('.jf_line').get(0)
      if line
        remove_error_hint.call line
        show_error_hint.call line, area.msg

  on_failed = (form, type, msg, options)->
    clear_form_error form
    show_form_error form, type, msg

    if options.validate_code
      form.find('.jf_valcode_input').val ''
      form.find('.jf_valcode_img').refresh_img()

    options.failed.call form, type, msg

  show_form_error = (form, type, msg)->
    form.append "<div class='jf_form_error'>#{msg}</div>"

  clear_form_error = (form)->
    form.find('.jf_form_error').remove()

  get_action_name = (form)->
    form.find('input[type=submit]').val()

  jq.fn.extend
    ajax_form: (options={})->
      options = extend_option options
      bind_events this, options
      this
