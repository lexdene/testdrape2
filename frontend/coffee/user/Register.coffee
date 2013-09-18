do(jq=jQuery)->
  jq ->
    jq('#register_form').ajax_form
      success: ->
        window.location = WEB_ROOT + form.data 'redirect'
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
        repassword:
          title: '重复密码'
          validates: [
            ['notempty'],
            ['equal', 'password', '密码']
          ]
        valcode:
          title: '验证码'
          validates: [
            ['notempty'],
            ['len', 4, 4]
          ]
        nickname:
          title: '昵称'
          validates: [
            ['notempty'],
            ['len', 4, 20]
          ]
        email:
          title: '电子邮箱'
          validates: [
            ['notempty'],
            ['len', 4, 50]
          ]
      validate_code: true
