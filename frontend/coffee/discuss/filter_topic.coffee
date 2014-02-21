do(jq=jQuery)->
  jq ->
    loading_icon = (el)->
      el.html dje.loading_html

    # tag list
    do ->
      all_tag_list = jq '#all-tag-list'
      selected_tag_list = jq '#selected-tag-list'

      # download tag list from server
      fetch_tag_list = (want_page=0)->
        # show loading icon
        loading_icon all_tag_list
        jq.getJSON(
          "#{WEB_ROOT}/tag/ajax_tag_list",
          {
            page: want_page
          }
        ).success (tag_list_data, status, resp)->
          # page
          page_widget.setDataByResp resp

          # render data
          render_tag_list tag_list_data

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

        # request data
        data = ({
          'name': 'tags[]',
          'value': tag_id
        } for tag_id in topic_list_params.tag_list)
        data.push(
          'name': 'page'
          'value': topic_list_params.page
        )

        # send request
        jq.getJSON(
          "#{WEB_ROOT}/discuss/ajax_topic_list", data
        ).success (topic_list_data, status, resp)->
          # page
          page_widget.setDataByResp resp

          # read now from header
          now = Date resp.getResponseHeader 'Date'
          if now == null
            jtopic_list.html dje.error_msg_html
              msg: '服务器错误: 未返回正确的Date信息'
            return

          # render data
          render_topic_list topic_list_data, now

      # render topic list
      template = _.template jq('#topic_list_template').html()
      render_topic_list = (topic_list, now)->
        html = template
          topic_list: topic_list
          format_date: jq.create_date_formater now
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
