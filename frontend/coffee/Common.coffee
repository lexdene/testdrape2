do ->
  dje.loading_html = '''
    <div>
      <div class="jf_spin jf_icon" data-icon="loading"></div>
      载入中...
    </div>
  '''
  dje.error_msg_html = _.template '''
    <div>
      <div class="jf_icon" data-icon="error"></div>
      <span>载入失败!</span>
      <span><%- msg %></span>
    </div>
  '''
  dje.avatar = (a) ->
    a or "#{WEB_ROOT}/static/image/avatar.jpg"
