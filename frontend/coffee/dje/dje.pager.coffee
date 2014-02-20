do(jq=jQuery)->
  _template = _.template(
    '''
    <div class="buttons">
      <% if(page>0){ %>
        <a href="#" data-page="<%- page -1 %>">上一页</a>
        <a href="#" data-page="0">1</a>
      <% }else{ %>
        <span>上一页</span>
        <span>1</span>
      <% } %>
      <% if (page_begin > 1){ %>
        <span>...</span>
      <% } %>
      <% _(_.range(page_begin, page_end)).each(function(i){
        if(i==page){ %>
          <span><%- i+1 %></span>
        <% }else{ %>
          <a href="#" data-page="<%- i %>"><%- i+1 %></a>
        <% }
        }) %>
      <% if(page_end < page_count -1){ %>
        <span>...</span>
      <% } %>
      <% if(page_count > 1){ %>
        <% if(page < page_count-1){ %>
          <a href="#" data-page="<%- page_count-1 %>"><%- page_count %></a>
        <% }else{ %>
          <span><%- page_count %></span>
        <% } %>
      <% } %>
      <% if(page < page_count -1){ %>
        <a href="#" data-page="<%- page+1 %>">下一页</a>
      <% }else{ %>
        <span>下一页</span>
      <% } %>
    </div>
    '''
  )
  Pager = (element, options)->
    _current_page = 0
    _total_page = 100
    _page_width = 5

    _options =
      on_page_change: (to_page)->
        to_page

    jq.extend _options, options

    this.page = ->
      return _current_page

    this.total_page = ->
      return _total_page

    this.setData = (page, total_page)->
      if page != undefined
        _current_page = parseInt page

      if total_page != undefined
        _total_page = parseInt total_page

      this.update()

    this.setDataByResp = (resp)->
      # 后端统一使用这些响应头来返回page相关数据
      headers =
        'X-Record-Page': 'page'
        'X-Record-PerPage': 'per_page'
        'X-Record-Count': 'count'

      data = {}
      for header, key of headers
        data[key] = resp.getResponseHeader header

      this.setData(
        data['page'],
        Math.ceil(data['count'] / data['per_page'])
      )

    this.update = ->
      page_begin = _current_page - Math.floor(_page_width/2)
      page_end = page_begin + _page_width

      if page_begin < 1
        page_begin = 1
        page_end = Math.min(_page_width, _total_page-2)+1
      else if page_end >= _total_page
        page_end = _total_page-1
        if _total_page < _page_width+2
          page_begin = 1
      else
        page_begin = page_end - _page_width

      element.html _template {
        page: _current_page
        page_count: _total_page
        page_begin: page_begin
        page_end: page_end
      }

    me = this
    element.on 'click', 'a[data-page]', (e)->
      e.preventDefault()
      to_page = parseInt jq(this).attr 'data-page'
      _options.on_page_change to_page
      me.setData to_page

    this.update()
    return this

  jq.fn.extend {
    pager: (options)->
      this.each ->
        el = jq(this)
        if not el.data('pager')
          el.data 'pager', new Pager el, options

      return this.data('pager')
  }
