do(jq=jQuery)->
  jq ->
    form = jq '#post_form'
    form.ajax_form
      validate:
        title:
          title: '标题'
          validates: [
            ['notempty']
          ]
        text:
          title: '内容'
          validates: [
            ['notempty']
          ]
        tags:
          title: '标签'
          validates: [
            ['len', 1, 5]
          ]
      before_submit: ->
        submit_tag_input()

    tags_input = jq '#tags_input'

    tag_template = _.template '''
      <span class="tag_item jf_tag">
        <span><%- val %></span>
        <a href="#" class="remove_button">x</a>
        <input name="tags[]" type="hidden" value="<%- val %>" />
      </span>'''
    submit_tag_input = ->
      val = jq.trim tags_input.val()
      if val.length > 0
        tags_input.val ''
        jq('#tag_line').append(tag_template
          val: val
        ).click()

    # bind events
    jq('#tag_line').on 'click', '.remove_button', ->
      jq(this).closest('.tag_item').remove()

    tags_input.keyup ->
      val = tags_input.val()
      lastcode = val.substr -1
      if ' ' == lastcode
        submit_tag_input()
