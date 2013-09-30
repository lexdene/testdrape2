do(jq=jQuery)->
  change_page = (obj, pagename)->
    # tab page , hide and show
    selected_page = obj.find(".tab_page[tab_page=#{pagename}]")

    index = selected_page.index()
    width = selected_page.outerWidth()
    margin_left = - index * width
    obj.find(".tab_page_wrap").css 'margin-left', margin_left + 'px'

    # tab nav active
    obj.find(".tab_nav_area .nav_btn[tab_page=#{pagename}]").closest('.nav_btn_wrap').addClass('nav_btn_active').siblings().removeClass('nav_btn_active')

    # trigger page_change
    obj.trigger 'page_change', [pagename, selected_page]

  show_default_page = (obj)->
    change_page obj, obj.find('.tab_page').first().attr('tab_page')

  change_page_by_hash = (obj)->
    hash = window.location.hash
    tab_page = hash.substr 2
    if tab_page == ''
      show_default_page obj
    else
      if hash.indexOf('#!') == 0
        change_page obj, tab_page

  jq.fn.extend
    tabs: ->
      jq(window).on 'hashchange', =>
        change_page_by_hash this

      # delay change page
      setTimeout =>
        change_page_by_hash this
      ,50

      # return this
      this
