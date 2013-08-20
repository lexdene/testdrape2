do(jq=jQuery)->
  jq ->
    loading_icon = (el)->
      el.html(loading_html)

    # tag list
    do ->
      all_tag_list = jq '#all-tag-list'
      selected_tag_list = jq '#selected-tag-list'

      # download tag list from server
      fetch_tag_list = (want_page=0)->
        # show loading icon
        loading_icon all_tag_list
        jq.getJSON(
          "#{WEB_ROOT}/discuss2/ajax_tag_list",
          {
            page: want_page
          }
        ).success (tag_list_data)->
          # page
          page_widget.setData(
            tag_list_data.page,
            Math.ceil(tag_list_data.total_count/tag_list_data.per_page)
          )

          render_tag_list tag_list_data.tag_list

      # render tag list
      template = _.template(
        '''
        <ul class="jf_label_list">
          <% _(tag_list).each(function(tag){ %>
            <li class="jf_label<%- tag.activeClass %>" data-id="<%- tag.id %>">
              <span class="jf_label_text"><%- tag.content %></span>
            </li>
          <% }) %>
        </ul>
        '''
      )
      render_tag_list = (tag_list)->
        selected_tag_id_list = []
        selected_tag_list.find('.jf_label').each ->
          selected_tag_id_list.push parseInt jq(this).attr('data-id')

        _(tag_list).each (tag)->
          if tag.id in selected_tag_id_list
            tag.activeClass = ' active'
          else
            tag.activeClass = ''
        all_tag_list.html template tag_list: tag_list

      # init pager
      page_widget = all_tag_list.siblings('.page').pager(
        on_page_change: (to_page)->
          fetch_tag_list to_page
      )

      # init label
      all_tag_list.on 'click', '.jf_label', ->
        jthis = jq this
        tag_id = jthis.attr('data-id')
        if jthis.hasClass 'active'
          jthis.removeClass 'active'
          selected_tag_list.find(".jf_label[data-id=#{tag_id}]").remove()
        else
          jq(this).addClass 'active'
          selected_tag_list.append jthis.clone()
        selected_tag_list.trigger 'list_change'

      selected_tag_list.on 'click', '.jf_label', ->
        jthis = jq this
        tag_id = jthis.attr('data-id')
        all_tag_list.find(".jf_label[data-id=#{tag_id}]").removeClass 'active'
        jthis.remove()
        selected_tag_list.trigger 'list_change'

      # load first page
      fetch_tag_list 0

    # topic list
    do ->
      selected_tag_list = jq '#selected-tag-list'
      jtopic_list = jq '#topic-list'
      topic_list_params =
        page: 0
        tag_list: []

      fetch_topic_list = ->
        # show loading icon
        loading_icon jtopic_list
        jq.getJSON(
          "#{WEB_ROOT}/discuss2/ajax_topic_list",
          {
            page: topic_list_params.page
            tag_list: topic_list_params.tag_list.join ','
          },
        ).success (topic_list_data)->
          # page
          page_widget.setData(
            topic_list_data.page,
            Math.ceil(topic_list_data.total_count/topic_list_data.per_page)
          )

          render_topic_list topic_list_data.topic_list, topic_list_data.now

      # render topic list
      template = _.template(
        '''
          <% _(topic_list).each(function(topic_item){ %>
            <div class="item">
              <div class="title_line clearfix">
                <div class="common_layout_column">
                  <div class="avatar_block">
                    <img class="avatar" src="<%= avatar(topic_item["topic_ui.avatar"]) %>" alt="avatar" title="<%- topic_item["topic_ui.nickname"] %>" />
                  </div>
                  <div class="author_nickname">
                    <a class="username_btn" href="#" userid="<%- topic_item["topic_ui.id"] %>">
                      <%- topic_item["topic_ui.nickname"] %>
                    </a>
                  </div>
                </div>
                <div class="common_layout_column">
                  <div class="title">
                    <a href="<%= WEB_ROOT %>/discuss/Topic/id/<%- topic_item["id"] %>">
                      <%- topic_item["title"] %>
                    </a>
                  </div>
                  <div class="jf_tag_line">
                    <% _(topic_item["tag_list"]).each(function(tag){ %>
                      <span class="jf_tag">
                        <a href="<%= WEB_ROOT %>/discuss/List/tag/<%- tag.id %>"><%- tag.content %></a>
                      </span>
                    <% }) %>
                  </div>
                </div>
              </div>
              <div class="topic_info_line">
                <span class="ctime">
                  发表时间：
                  <%- format_date(topic_item["ctime"]) %>
                </span>
                <span class="reply_count">
                  楼层数：
                  <%- topic_item["reply_count"] %>
                </span>
                <span class="last_reply">
                  最后回复：
                  <% if(topic_item["tc.first_reply_id"] != topic_item["tc.last_reply_id"]){ %>
                    <span class="time"><%- format_date(topic_item["last_reply.ctime"]) %></span>
                    <span class="user">
                      <img class="avatar" src="<%= avatar(topic_item["last_reply_ui.avatar"]) %>" alt="avatar" title="<%- topic_item["last_reply_ui.nickname"] %>" />
                    </span>
                  <% }else{ %>
                    <span class="time">-</span>
                    <span class="user"></span>
                  <% } %>
                </span>
              </div>
            </div>
          <% }) %>
        '''
      )
      render_topic_list = (topic_list, now)->
        html = template
          topic_list: topic_list
          format_date: jq.create_format_date(now)
        jtopic_list.html html

      # init pager
      page_widget = jtopic_list.siblings('.page').pager(
        on_page_change: (to_page)->
          topic_list_params.page = to_page
          fetch_topic_list()
      )

      # bind list change
      selected_tag_list.bind 'list_change', ->
        topic_list_params.page = 0
        tag_id_list = []
        selected_tag_list.find('.jf_label').each ->
          tag_id_list.push parseInt jq(this).attr('data-id')
        topic_list_params.tag_list = tag_id_list

        fetch_topic_list()

      fetch_topic_list()
