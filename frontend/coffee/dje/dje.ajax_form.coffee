do(jq=jQuery)->
  extend_option = (options)->
    default_option =
      success: ->
        alert '提交成功'
      failed: (msg)->
        alert "提交失败: #{msg}"
      validate:
        form_area: {}
        failed: ()->
          alert "验证失败"
      before_submit: ->
        true

    jq.extend true, default_option, options

  bind_events = (jobj, options)->
    jobj.submit (e)->
      e.preventDefault()
      ajax_submit jq(this), options
    jobj.on 'click focus', '.jf_line', remove_error_hint
    true

  ajax_submit = (form, options)->
    options.before_submit.call form
    params = get_form_params(form)
    validate_result = validate_params params, options.validate.form_area
    if not validate_result.result
      show_all_error_hint form, validate_result
      options.validate.failed validate_result.msg
      return

    form.add_mask()

    setTimeout ->
      form.remove_mask()
      true
    , 1000
    true

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

  show_error_hint = (msg)->
    line = jq this
    line.append "<span class='jf_error'>#{msg}</span>"

  show_all_error_hint = (form, validate_result)->
    jq.each validate_result.illegal_area, (index, area)->
      line = form.find(".jf_input[name=#{area.name}]").closest('.jf_line').get(0)
      if line
        show_error_hint.call line, area.msg

  jq.fn.extend
    ajax_form: (options={})->
      options = extend_option options
      bind_events this, options
      this
