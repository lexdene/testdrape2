do (jq=jQuery) ->
  template_str = '''
  <% _(msg_list).each(function(msg){ %>
    <div class="msg_item" msg_id="<%- msg.id %>">
      <div class="first_line">
        <a class="from_user username_btn" href="#" data-userid="<%- msg.from_ui.id %>">
          <%- msg.from_ui.nickname %>
        </a>

        <% if (msg.to_uid > 0){ %>
          回复
          <a class="to_user username_btn" href="#" data-userid="<%- msg.to_ui.id %>">
            <%- msg.to_ui.nickname %>
          </a>
        <% } %>
        :
        <span><%- msg.text %></span>
      </div>
      <div class="second_line">
        <span class="ctime"><%- format_date(msg.ctime) %></span>
        <% if(msg.from_ui.id != my_userid){ %>
          <a class="reply_btn" href="#">回复</a>
        <% } %>
      </div>
    </div>
  <% }) %>
  '''

  class Usermsg
    container: null
    page_hint: null
    form: null

    to_uid: -1
    current_page: 0
    total_page: 0
    template: null

    set_container: (c) ->
      me = @
      @container = c
      @container.on('click', '.reply_btn', (event) ->
        event.preventDefault()
        msg_item = jq(this).closest('.msg_item')
        from_user_btn = msg_item.find '.from_user'

        from_userid = from_user_btn.attr 'userid'
        from_username = from_user_btn.text().trim()

        me.reply_to(from_userid, from_username)
      )

    set_page_hint: (h) ->
      @page_hint = h

    set_to_uid: (t) ->
      @to_uid = t

    set_form: (f) ->
      @from = f
      @from.submit =>
        @from.ajaxSubmit(
          success: =>
            alert '回复成功'
            location.reload()
          error: (msg)=>
            alert '回复失败：' + msg
          validate:
            form_area: [
              {
                key: 'text'
                name: '留言内容'
                validates: [
                  ['len', 1, 200]
                ]
              }
            ]
        )
      true

    reply_to: (userid, username) ->
      if @from
        @from.find('input[name=to_uid]').val userid
        @from.find('.reply_to_hint').html(
          "回复#{username}"
        )

      true

    render: (data) ->
      if '' == data['errormsg']
        @current_page = data.page
        @total_page = Math.ceil data.count / data.per_page

        #@render data
        if null == @template
          @template = _.template template_str

        @container.html @template {
          msg_list: data.data
          format_date: jq.create_format_date data.now
          my_userid: my_userid
        }

        page_str = @current_page + 1
        @page_hint.html "共#{page_str}/#{@total_page}页"

      else
        @container.html error_html + data['errormsg']

    refresh: (page=0) ->
      jq.delay(
        1000,
        (r) =>
          @container.html loading_html

          jq.get(
            WEB_ROOT + "/usermsg/AjaxMsgList/to_uid/#{@to_uid}",
            {page: page},
            undefined,
            'json'
          ).success (data) ->
            r data
            true
          .error ->
            r {
                errormsg: '系统错误'
                data: []
            }
            true
        ,(data) =>
          @render data

          true
      )

    set_page_buttons: (buttons) ->
      me = @
      buttons.click (e)->
        e.preventDefault()
        switch jq(this).attr 'action'
          when 'prev'
            target_page = me.current_page - 1
          when 'next'
            target_page = me.current_page + 1
        if target_page < 0 or target_page >= me.total_page
          return

        me.refresh target_page

  window.Usermsg = Usermsg
  true
