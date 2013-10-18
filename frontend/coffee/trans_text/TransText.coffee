do (jq=jQuery) ->
  emoji_base_path = dje.libcdn + '/emoji/public/graphics/emojis/'
  emoji_regexp = new RegExp ':([-+_a-zA-Z0-9]+):','g'
  markdown_converter = new Showdown.converter()

  transText = (text)->
    markdown emoji text
  emoji = (text)->
    text.replace emoji_regexp, (aword, word)->
      if is_emoji word
        "<img class='jf_emoji' title='#{word}' alt='#{word}' src='#{emoji_base_path}#{word}.png' align='absmiddle' />"
      else
        aword
  is_emoji = (word)->
    if word of dje.emoji_dict then true else false
  markdown = (origin)->
    markdown_converter.makeHtml origin

  dje.transText = transText
