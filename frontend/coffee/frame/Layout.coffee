do(jq=jQuery) ->
  ua = navigator.userAgent.toLowerCase()
  s = ua.match /msie ([\d.]+)/
  if s
    version = s[1]
    require_version = '10.0'
    if jq.version_cmp(version, require_version) < 0
      template = _.template(
        '''<div class="fuckie" style="display:none">
          <div class="fuckie_index">
            <div>
              检测到您的浏览器器是 <b>IE</b> ，
              版本是 <b><%- version %></b> </div>
            <div>您的浏览器版本过低，无法正常浏览本网站</div>
            <div>请升级到 <b>IE <%- require_version %></b> 或更高版本</div>
            <div>给您造成的不便，敬请谅解</div>
            <hr />
            <div>推荐使用chrome或者firefox浏览器</div>
            <div>chrome浏览器下载地址：<a href="http://www.google.cn/Chrome">http://www.google.cn/Chrome</a></div>
            <div>firefox浏览器下载地址：<a href="http://firefox.com.cn/download/">http://firefox.com.cn/download</a></div>
          </div>
        </div>''',
        version: version
        require_version: require_version
      )

      block = jq template
      jq('.layout_head_line').append block
      jwin = jq window
      block.height jwin.height() - 100
      block.slideDown 'slow'
