do (jq=jQuery) ->
  f = jq('#mymsglist')
  um = new Usermsg

  um.set_container f.find('.msg_list')
  um.set_page_hint f.find('.page_count')
  um.set_to_uid -1

  um.refresh()
