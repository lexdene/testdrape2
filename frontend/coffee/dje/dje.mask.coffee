do(jq=jQuery)->
  template = _.template(
    '''
    <div class="dje_mask jf_blackmask">
      <div class="place_holder"></div>
      <div class="content">
        <%= icon_html %>
        <%- text %>
      </div>
    </div>
    ''')

  default_option =
    add_mask:
      type: 'loading'
      text: 'loading...'

  icon_html =
    loading: '<div class="jf_spin jf_icon" data-icon="loading"></div>'
    success: '<div class="jf_icon" data-icon="success"></div>'
  jq.fn.extend
    add_mask: (options)->
      options = jq.extend default_option.add_mask, options
      this.addClass 'jf_mask_wrap'
      this.append template
        icon_html: icon_html[options.type]
        text: options.text
      this

    remove_mask: (options)->
      this.removeClass 'jf_mask_wrap'
      this.find('.dje_mask').remove()
      this
