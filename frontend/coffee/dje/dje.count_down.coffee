do(jq=jQuery)->
  template = _.template '''
    <%- time %>秒钟后跳转至
    <a href="<%- WEB_ROOT %>/<%- location %>">
      /<%- location %>
    </a>
  '''
  jq.fn.extend
    count_down: ->
      time = parseInt this.data 'time'
      location = this.data 'location'
      me = this

      me.html template
        time: time
        location: location

      timer = setInterval ->
        --time
        me.html template
          time: time
          location: location

        if time <= 0
          clearInterval timer
          window.location = WEB_ROOT + '/' + location
      , 1000
      this
