do ->
  window.loading_html = '''
    <div>
      <div class="jf_spin jf_icon" data-icon="loading"></div>
      载入中...
    </div>
  '''
  window.error_html = '''
    <div>
      <div class="jf_icon" data-icon="error"></div>
      载入失败!
    </div>
  '''
  window.avatar = (a) ->
    a or "#{WEB_ROOT}/static/image/avatar.jpg"
