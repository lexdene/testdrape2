do(jq=jQuery)->
  jq ->
    # check user login
    if my_userid < 0
      alert '请先登录'
      window.location = WEB_ROOT + '/user/Login'
      return

    # content area
    newsfeed.load jq('#content-area'), (from_id, r)->
      jq.getJSON(WEB_ROOT + '/home/AjaxHomeLine',
        from_id: from_id
      ,(data)->
        r data
      ).error ->
        r
          errormsg: '系统错误'
          data: []
