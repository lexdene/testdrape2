do(jq=jQuery)->
  jq ->
    topic_page.init()

  topic_page =
    init: ->
      this.markdown.init()
      this.reply_form.init()
      this.reply_to_reply.init()
      this.edit.init()
      this.focus.init()

    markdown:
      init: ->
        me = this
        jq('script[type="text/markdown"]').each ->
          me.update_content jq this
      update_content: (obj)->
        obj.siblings('.jf_markdown').html transText obj.html()

    reply_form:
      from: null
      init: ->
        this.form = jq '#reply_form'
        this.form.ajax_form
          validate:
            text:
              title: '回复'
              validates: [
                ['notempty'],
                ['len', 4, 50000]
              ]

        reply_to_hint = this.form.find('.reply_to_hint')
        reply_to_id_input = this.form.find('input[name=reply_to_id]')

        jq('.reply_button').click (e)->
          e.preventDefault()

          floor_obj = jq(this).closest '.floor'
          floor_id = floor_obj.data 'floor-id'
          reply_to_id_input.val floor_id

          floor_username_obj = floor_obj.find('.floor_left_column .username_btn')
          floor_username = jq.trim floor_username_obj.text()
          floor_content_obj = floor_obj.find('.floor_right_column .floor_content .jf_markdown')
          floor_content = floor_content_obj.html()

          reply_to_hint.find('.to_username').html floor_username
          reply_to_hint.find('.jf_markdown').html floor_content
          reply_to_hint.show()
          reply_to_hint.scroll_to()

        reply_to_hint.find('.cancel_reply_button').click (e)->
          e.preventDefault()

          reply_to_id_input.val -1
          reply_to_hint.hide()

    reply_to_reply:
      init: ->
        jq('.reply_to_reply').find('.jump_button').click (e)->
          e.preventDefault()
          reply_to_id = jq(this).closest('.reply_to_reply').data('reply-to-id')
          jq(".floor[data-floor-id=#{reply_to_id}]").scroll_to()

    edit:
      init: ->
        jq('.edit_button').click (e)->
          e.preventDefault()

          edit_button = jq this
          floor_content = edit_button.closest('.floor').find('.floor_content')
          edit_area = floor_content.find '.floor_edit'
          text = floor_content.find('script[type="text/markdown"]').text()
          if edit_area.is ':hidden'
            edit_area.find('textarea').val _.unescape text
            edit_button.text '取消编辑'
          else
            edit_area.find('textarea').val ''
            floor_content.find('.jf_markdown').html transText text
            edit_button.text '编辑'

          edit_area.slideToggle 'slow'

        jq('.floor .floor_edit textarea').keyup ->
          jq(this).closest('.floor').find('.floor_content .jf_markdown').html transText _.escape jq(this).val()

        jq('.edit_form').ajax_form
          validate:
            text:
              title: '回复'
              validates: [
                ['notempty'],
                ['len', 4, 25000]
              ]

    focus:
      init: ->
        focus_button = jq '#focus_topic_btn'
        topic_id = jq('.discuss_topic').data('topic-id')

        focus_button.click (e)->
          e.preventDefault()

          jq.post WEB_ROOT + '/focus/ajaxFocus',
            type: 'topic'
            target: topic_id
            dire: 'add'
          ,(data)->
            if data.result == 'success'
              alert '关注成功'
            else
              alert data.msg
          ,'json'
