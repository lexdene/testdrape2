do ->
  window.loading_html = "<div><img class='jf_spin' src='#{WEB_ROOT}/static/image/loading.png' />载入中...</div>"
  window.error_html = "<div><img src='#{WEB_ROOT}/static/image/error.png' />载入失败!</div>"
  window.avatar = (a) ->
    a or "#{WEB_ROOT}/static/image/avatar.jpg"
