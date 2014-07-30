do(jq=jQuery)->
  jq ->
    # check user login
    if my_userid < 0
      alert '请先登录'
      window.location = WEB_ROOT + '/user/Login'
      return

    # content area
    dje.newsfeed jq('#content-area'), '/home'
