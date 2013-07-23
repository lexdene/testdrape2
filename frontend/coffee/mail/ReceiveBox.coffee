do (jq=jQuery)->
  jq ->
    jq('.mail_receivebox .mail_item .body').each ->
      jq(this).find('.jf_markdown').html transText jq(this).find('script[type="text/markdown"]').html()
    jq('.mail_receivebox .mail_item .title').click ->
      jq(this).closest('.mail_item').find('.body').fadeToggle('slow')
