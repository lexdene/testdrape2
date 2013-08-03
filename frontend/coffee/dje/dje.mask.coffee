do(jq=jQuery)->
  template = _.template(
    '''
    <div class="dje_mask jf_blackmask">
      <%= loading_html %>
    </div>
    ''', {})
  jq.fn.extend
    add_mask: (options)->
      this.append template
      this

    remove_mask: (options)->
      this.find('.dje_mask').remove()
      this
