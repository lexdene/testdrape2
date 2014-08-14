do(jq=jQuery)->
  jq ->
    userinfo.init()
    focus.init()
    newsfeed_page.init()
    topic_page.init()
    msg_page.init()
    tabs.init()

  userinfo =
    id: null
    init: ->
      this.id = jq(".user_homepage").data('user-id')

  focus =
    button: null
    load_text: ->
      html = if this.button.data('is-focused') == 'True' then '取消关注' else '关注'
      this.button.html html

    init: ->
      this.button = jq '#focus_button'
      this.load_text()

      this.button.click (e)=>
        e.preventDefault()

        dire = if this.button.data('is-focused') == 'True' then 'remove' else 'add'
        jq.post WEB_ROOT + '/focuses',
          type: 'user'
          target: userinfo.id
          dire: dire
        ,(data)->
          if data.result = 'success'
            if dire == 'remove'
              focus.button.data 'is-focused', 'False'
              alert '取消关注成功'
            else
              focus.button.data 'is-focused', 'True'
              alert '关注成功'
            focus.load_text()
          else
            alert data.msg
        ,'json'

  newsfeed_page =
    area: null
    init: ->
      true
    load: (area)->
      if this.area == null
        this.area = area
        this.first_load()
    first_load: ->
      this.area.newsfeed
        url: "/userinfo/#{userinfo.id}/actions"

  topic_page =
    area: null
    template: null
    init: ->
      this.template = _.template jq('#topic_list_template').html()
    load: (area)->
      if this.area == null
        this.area = area
        this.first_load()
    first_load: ->
      me = this
      topic_list_area = me.area.find '.discuss_list .list'
      jq.delay
        action: (set_result)->
          topic_list_area.html dje.loading_html
          jq.getJSON(WEB_ROOT + '/userinfo2/ajax_user_topic_list',
            uid: userinfo.id
          ).success (data)->
            set_result data
          .error ->
            set_result
              result: 'failed'
              msg: '网络错误'
        finish: (result)->
          if result.result == 'success'
            topic_list_area.html me.template
              topic_list: result.topic_list
              format_date: jq.create_date_formater result.now
          else
            topic_list_area.html dje.error_msg_html
              msg: result.msg

  msg_page =
    area: null
    init: ->
      true
    load: (area)->
      if this.area == null
        this.area = area
        this.first_load()
    first_load: ->
      me = this

      # template
      this.template = _.template jq('#msg_template').html()

      # form
      form = this.area.find('form')
      form.ajax_form
        success: ->
          form.find('textarea').val ''
          form.add_mask
            type: 'success'
            text: '发表成功'
          me.fetch_msg_list()

          setTimeout ->
            form.remove_mask()
          ,1000

      # pager
      this.page_widget = this.area.find('.pager').pager
        on_page_change: (to_page)->
          me.fetch_msg_list to_page

      # first fetch
      this.fetch_msg_list 0
    fetch_msg_list: (to_page=0)->
      me = this
      msg_list_area = this.area.find '.msg_list'
      jq.delay_ajax
        action: ->
          msg_list_area.html dje.loading_html

          jq.getJSON WEB_ROOT + "/userinfo/#{userinfo.id}/messages",
            page: to_page
        finish: (data)->
          if data.errormsg == ''
            me.page_widget.setData data.page, Math.ceil data.count / data.per_page
            msg_list_area.html me.template
              msg_list: data.data
              format_date: jq.create_date_formater data.now
          else
            me.page_widget.setData 0, 1
            msg_list_area.html dje.error_msg_html
              msg: data.errormsg

  tabs =
    init: ->
      jq('#tabs').tabs().bind 'page_change', (e, pagename, page)->
        switch pagename
          when 'topic' then topic_page.load page
          when 'newsfeed' then newsfeed_page.load page
          when 'msg' then msg_page.load page
