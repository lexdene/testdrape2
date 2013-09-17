do(jq=jQuery)->
  jq ->
    jq('#focus_tag_btn').click (e)->
      e.preventDefault()

      tag_id = jq(this).data('tagid')
      jq.post(
        WEB_ROOT + '/focus/ajaxFocus',
          type: 'tag'
          target: tag_id
          dire: 'add'
        ,(data)->
          if data.result == 'success'
            alert '关注成功'
          else
            alert data.msg
        ,'json'
      )
