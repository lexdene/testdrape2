do(jq=jQuery) ->
  jq ->
    jq('.layout_head_line .notice_btn').click (e)->
      e.preventDefault()
      btn = jq this

      dialog = get_dialog_object()

      # if visible then close
      if dialog.is ':visible'
        dialog.hide()
        return

      # loading and show
      dialog.html dje.loading_html
      dialog.show()

      # delay data
      jq.delay 1000, (set_result)->
        jq.getJSON(
          WEB_ROOT + '/notices'
        ).success (data)->
          set_result
            result: 'success'
            notice_list: data
        .error ->
          set_result
            result: 'failed'
            msg: '网络错误'
      ,(data)->
        if data.result == 'success'
          dialog.html template
            notice_list: data.notice_list
        else
          dialog.html dje.error_msg_html
            msg: data.msg

    get_dialog_object = ->
      if get_dialog_object.__dialog_singleton == undefined
        d = jq '<div class="notice_dialog"></div>'
        d.css
          display: 'none'
        jq('body').append d

        # close btn event
        d.on 'click', '.close_btn', (e)->
          e.preventDefault()
          d.hide()

        d.on 'click', '.notice_item', (e)->
          notice_item = jq this
          notice_id = notice_item.data 'notice-id'

          jq.post WEB_ROOT + '/notice/ajax_set_is_read',
            notice_id: notice_id
          ,(data)->
            if data.result == 'success'
              notice_item.remove()

              count_obj = jq '.layout_head_line .notice_btn .count'
              unread_count = count_obj.html() - 1
              if unread_count == 0
                count_obj.remove()
              else
                count_obj.html unread_count
          ,'json'


        get_dialog_object.__dialog_singleton = d

      get_dialog_object.__dialog_singleton

    template = _.template '''
      <div>
        <a href="#" class="close_btn">关闭</a>
      </div>
      <div class="notice_list">
        <% if(notice_list.length == 0){ %>
          <div class="no_notice">无未读通知</div>
        <% }else{ %>
          <% _(notice_list).each(function(notice){ %>
            <div class="notice_item" data-notice-id="<%- notice.id %>">
            <% switch(notice.type){
              case "reply_topic": %>
                <a class="username_btn" data-userid="<%- notice.fromuser.id %>">
                  <%- notice.fromuser.nickname %>
                </a>
                回复了您的主题
                <a target="_blank" class="fromtopic" href="<%- WEB_ROOT %>/discuss/Topic/id/<%- notice.reply_info.dt.id %>#reply<%- notice.item_id %>">
                  <%- notice.reply_info.dt.title %>
                </a>
            <% break;
              case "reply_to_reply": %>
                <a class="username_btn" data-userid="<%- notice.fromuser.id %>">
                  <%- notice.fromuser.nickname %>
                </a>
                在主题
                <a target="_blank" class="fromtopic" href="<%- WEB_ROOT %>/discuss/Topic/id/<%- notice.reply_info.dt.id %>#reply<%- notice.item_id %>">
                  <%- notice.reply_info.dt.title %>
                </a>
                回复了您
            <% break;
              case "focus_user": %>
                <a class="username_btn" data-userid="<%- notice.fromuser.id %>">
                  <%- notice.fromuser.nickname %>
                </a>
                关注了您
            <% break;
              case "usermsg": %>
                <a class="username_btn" data-userid="<%- notice.fromuser.id %>">
                  <%- notice.fromuser.nickname %>
                </a>
                给您
                <a target="_blank" href="<%- WEB_ROOT %>/usermsg/MyMsgList">留言</a>
                了
            <% break;
            } %>
            </div>
        <% }) } %>
      </div>
    '''

