do(jq=jQuery)->
  jq ->
    jq('#submit_form').ajax_form
      success: ->
        form = this
        # 在complete中会remove mask
        # 所以此时要延时到remove mask之后执行
        setTimeout(
          ->
            form.add_mask
              type: 'success'
              text: '登录成功'
            window.location = WEB_ROOT + form.data('redirect')
          ,100
        )
      validate:
        loginname:
          title: '登录名'
          validates: [
            ['notempty'],
            ['len', 4, 20]
          ]
        password:
          title: '密码'
          validates: [
            ['notempty'],
            ['len', 4, 20]
          ]
        valcode:
          title: '验证码'
          validates: [
            ['notempty'],
            ['len', 4, 4]
          ]
      validate_code: true
