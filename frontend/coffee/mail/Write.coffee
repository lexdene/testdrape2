do(jq=jQuery)->
  jq ->
    form = jq '#write_form'
    form.ajax_form
      success: ->
        alert '发送成功'
        window.location = WEB_ROOT + '/mail/ReceiveBox'
      failed: (msg)->
        alert '发送失败' + msg
