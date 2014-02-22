do (jq=jQuery) ->
  emoji_base_path = dje.libcdn + '/emoji/public/graphics/emojis/'
  emoji_regexp = new RegExp ':([-+_a-zA-Z0-9]+):','g'
  markdown_converter = new Showdown.converter()
  code_regexp = new RegExp '<code>([^<>]*)</code>', 'mg'
  uncode_regexp = new RegExp "<code index='(\\d*)'>(\\d*)</code>", 'g'

  transText = (text)->
    unescape_code emoji escape_code markdown text

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

  code_list = []
  escape_code = (text)->
    text.replace code_regexp, (allMatch, word)->
      index = code_list.length
      code_list.push _.unescape allMatch
      "<code index='#{index}'>#{index}</code>"

  unescape_code = (text)->
    text.replace uncode_regexp, (allMatch, index)->
      code_list[parseInt index]

  dje.transText = transText

'''
# test

    <input />

<input />

:smile:


    <input />

    :smile:

aaa`xxx`aaa

aaa`xxx <input />`aaa

    int a;
    char b;
    count << a << b << endl;
'''
