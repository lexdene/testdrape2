(function(jq){
    var jQuery = undefined;
	jq(function(){
		jq('#post_form').submit(function(){
			var form = jq(this);
			form.ajaxSubmit({
				'success':function(){
					alert('发表成功');
					location.reload();
				},
				'failed':function(msg){
					alert('发表失败:'+msg);
				},
				'validate':{
					'form_area':[
						{
							'key' : 'title',
							'name' : '标题',
							'validates' : [
								['notempty'],
								['len',4,50]
							]
						},
						{
							'key' : 'text',
							'name' : '内容',
							'validates' : [
								['notempty'],
								['len',4,500]
							]
						}
					]
					,
					'callback':function(result,msg){
						if( ! result ){
							alert(msg);
						}
					}
				}
			});
		});
	    var tags_input = jq('#tags_input');
	    tags_input.keyup(function(event){
		var input = jq(this);

		var val = input.val();
		var lastcode = val.substr(-1);
		var trim_val = val.replace(/(^\s*)|(\s*$)/g, "");
		if( trim_val.length > 0 && ' ' == lastcode ){
		    console.log(trim_val);
		    
		    // remove val
		    input.val('');
		    
		    // create buttons
		    var button = jq('<span class="tag_item"><span class="tag_val">'+trim_val+'</span><a href="#" class="remove_button">X</a></span>');
		    button.find('.remove_button').click(function(){
			jq(this).closest('.tag_item').remove();
			return false;
		    });
		    input.closest('.tag_wrap').find('.tag_list').append(button);
		    
		    // set value to real tags
		    update_value_for_real_tags();
		    
		    return false;
		}
	    });
	    function update_value_for_real_tags(){
		var val_list = [];
		tags_input.closest('.tag_wrap').find('.tag_list>.tag_item>.tag_val').each(function(){
		    var sv = jq(this).text();
		    val_list.push(sv);
		});
		console.log(val_list);
		jq('#real_tags').val( val_list.join(' ') );
	    }
	});
})(jQuery);
