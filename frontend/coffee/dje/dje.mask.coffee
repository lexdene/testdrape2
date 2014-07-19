do(jq=jQuery)->
  template = _.template(
    '''
    <div class="dje_mask jf_blackmask">
      <div class="content-wrapper">
        <div class="content">
          <%= content_html %>
        </div>
      </div>
    </div>
    ''')

  jq.fn.extend
    add_mask: (options)->
      this.addClass 'jf_mask_wrap'
      this.append template
        content_html: options['content_html']
      this

    remove_mask: (options)->
      this.removeClass 'jf_mask_wrap'
      this.find('.dje_mask').remove()
      this
