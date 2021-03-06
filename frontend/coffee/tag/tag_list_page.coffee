do (jq=jQuery)->
  jq ->
    tag_list_container = jq '#tag-list'

    fetch_tag_list = (want_page=0)->
      # show loading
      tag_list_container.html dje.loading_html

      # ajax tag list
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

    render_tag_list = (tag_list)->
      tag_list_container.html tag_list_template tag_list: tag_list

    page_widget = jq('#tag-pager').pager(
      on_page_change: (to_page)->
        fetch_tag_list to_page
    )

    tag_list_template = _.template(
      '''
        <div class="tag_item header">
          <span class="col_content">标签名称</span>
          <span class="col_reply_count">回复数</span>
          <span class="col_topic_count">主题数</span>
          <span class="col_ctime">创建时间</span>
        </div>
        <% _(tag_list).each(function(tag){ %>
          <div class="tag_item">
            <span class="col_content">
              <a href="<%- WEB_ROOT %>/discuss/List/tag/<%- tag.id %>"><%- tag.content %></a>
            </span>
            <span class="col_reply_count"><%- tag.cache.reply_count %></span>
            <span class="col_topic_count"><%- tag.cache.topic_count %></span>
            <span class="col_ctime"><%- tag.ctime %></span>
          </div>
        <% }); %>
      '''
    )

    fetch_tag_list()
