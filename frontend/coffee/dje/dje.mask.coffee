do(jq=jQuery)->
  template = _.template(
    '''
    <div class="dje_mask jf_blackmask">
      <div class="place_holder"></div>
      <%= loading_html %>
    </div>
    ''', {})
  jq.fn.extend
    add_mask: (options)->
      this.addClass 'jf_mask_wrap'
      this.append template
      this

    remove_mask: (options)->
      this.removeClass 'jf_mask_wrap'
      this.find('.dje_mask').remove()
      this
