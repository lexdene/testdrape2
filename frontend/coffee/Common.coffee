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

  window.gws = ->
    websocket = new WebSocket "ws://#{location.host}#{WEB_ROOT}/websocket/"

    websocket.onopen = ->
      console.log 'open'
      console.log arguments

    websocket.onclose = ->
      console.log 'close'
      console.log arguments

    websocket.onmessage = (e)->
      console.log 'message', e.data
      console.log arguments

    websocket.onerror = ->
      console.log 'error'
      console.log arguments

    window.gws.socket = websocket

    true
