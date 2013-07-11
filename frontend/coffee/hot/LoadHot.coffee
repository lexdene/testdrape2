do (jq=jQuery) ->
  load_hot_tag = (container) ->
    jq.getJSON(
      "#{WEB_ROOT}/tag/randomTagList",
    ).success (data) ->
      container.html load_hot_tag.template
        tag_list: data.tag_list

  load_hot_tag.template = _.template '''
    <div class="hot_tag_list">
      <div class="hint">热门标签</div>
      <% _(tag_list).each(function(tag){ %>
        <div class="tag_item">
          <a href="<%- WEB_ROOT %>/discuss/List/tag/<%- tag.id %>"><%- tag.content %></a>
        </div>
      <% }) %>
    </div>
  '''
  jq ->
    container = jq('#body_right')

    content_name_list = ['hot_tag']
    random_num = Math.floor( Math.random() * content_name_list.length )
    content_name = content_name_list[random_num]

    switch content_name
      when 'hot_tag'
        load_hot_tag container
