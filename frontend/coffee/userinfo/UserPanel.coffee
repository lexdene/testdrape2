do(jq=jQuery)->
  jq ->
    jq('body').on 'click', '.username_btn', (event)->
      event.preventDefault()
      event.stopPropagation()

      btn = jq this
      userid = btn.data 'userid'

      dialog = get_dialog_object()
      dialog.html dje.loading_html

      # position and show
      pos = btn.offset()
      pos.left += 20
      pos.position = 'absolute'
      dialog.css pos
      dialog.show()

      jq.delay 1000, (set_result)->
        jq.getJSON(
          WEB_ROOT + '/userinfo2/ajax_user_info',
            uid: userid
          ,(data)->
            set_result data
        ).error ->
          set_result
            'result': 'failed',
            'msg': '系统错误'
      ,(data)->
        if data.result == 'success'
          dialog.html template
              userinfo: data.userinfo
        else
          dialog.html dje.error_msg_html
            msg: data.msg

    get_dialog_object = ->
      if get_dialog_object.__dialog_singleton == undefined
        d = jq '<div class="userpanel"></div>'
        jq('body').append d

        # stopPropagation
        d.click (e)->
          e.stopPropagation()

        # close dialog when click on body
        jq('body').click ->
          d.hide()

        get_dialog_object.__dialog_singleton = d

      get_dialog_object.__dialog_singleton

    template = _.template '''
      <div class="userinfo_userpanelpage">
        <div class="common_layout_column left_column">
          <div class="common_avatar_block">
            <img class="avatar" src="<%- dje.avatar(userinfo.avatar) %>" alt="avatar" title="<%- userinfo.nickname %>" />
          </div>
          <div class="button_block">
            <a href="<%- WEB_ROOT %>/mail/Write/to_uid/<%- userinfo.id %>">发送私信</a>
            <a href="<%- WEB_ROOT %>/userinfo/MainPage/id/<%- userinfo.id %>">个人主页</a>
          </div>
        </div>
        <div class="common_layout_column right_column jdmd_form">
          <div class="jf_line">
            <span class="jf_hint">昵称</span>
            <span class="content"><%- userinfo.nickname %></span>
          </div>
          <div class="jf_line">
            <span class="jf_hint">注册时间</span>
            <span class="content"><%- userinfo.ctime %></span>
          </div>
          <div class="jf_line">
            <span class="jf_hint">发帖数</span>
            <span class="content"><%- userinfo.topic_count %></span>
          </div>
          <div class="jf_line">
            <span class="jf_hint">回复数</span>
            <span class="content"><%- userinfo.reply_count %></span>
          </div>
        </div>
      </div>
    '''
