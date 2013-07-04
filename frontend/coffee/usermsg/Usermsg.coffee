do (jq=jQuery) ->
  template_str = '''
  <% _(msg_list).each(function(msg){ %>
    <div class="msg_item" msg_id="<%- msg.id %>">
      <div class="first_line">
        <a class="username_btn" href="#" userid="<%- msg.from_ui.id %>" onclick="return false">
          <%- msg.from_ui.nickname %>
        </a>
        回复
        <a class="username_btn" href="#" userid="<%- msg.to_ui.id %>" onclick="return false">
          <%- msg.to_ui.nickname %>
        </a>
        :
        <span><%- msg.text %></span>
      </div>
      <div class="second_line">
        <span class="ctime"><%- format_date(msg.ctime) %></span>
      </div>
    </div>
  <% }) %>
  '''

  loading_html = "<div class=\"loading\"><img src=\"#{WEB_ROOT}/static/image/loading.gif\" />载入中...</div>"
  error_html = "<img src=\"#{WEB_ROOT}/static/image/error.png\" />载入失败！"

  class Usermsg
    container: null
    page_hint: null

    to_uid: -1
    current_page: 0
    total_page: 0
    template: null

    set_container: (c) ->
      @container = c

    set_page_hint: (h) ->
      @page_hint = h

    set_to_uid: (t) ->
      @to_uid = t

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
      buttons.click ->
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
