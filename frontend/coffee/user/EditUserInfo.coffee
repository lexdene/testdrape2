do(jq=jQuery)->
  jq ->
    form = jq '#edituserinfo_form'
    dialog = jq '#dialog'
    msg_area = jq('.msg_block').find('.msg')
    avatar_preview = jq('.avatar_preview').find('.avatar')

    show_error = (text)->
      msg_area.html text

    set_avatar = (avatar)->
      form.find('input[name=avatar]').val avatar
      avatar_preview.attr 'src', avatar

    avatar_preview.error ->
      show_error '无法载入图片'
    .load ->
      show_error ''

    jq('#upload_avatar_btn').click (e)->
      e.preventDefault()
      dialog.find('iframe').attr 'src', WEB_ROOT + '/common/UploadImage?accept=image/gif,image/jpeg,image/png'
      dialog.centerInWindow()
      dialog.show()

    dialog.find('.close_button').click (e)->
      e.preventDefault()
      dialog.find('iframe').attr 'src', ''
      dialog.hide()

    form.ajax_form()

    window.uploadCallBack = (result, savepath)->
      if 'success' == result
        set_avatar savepath
