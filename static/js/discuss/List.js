(function(jq){
	var jQuery = undefined;
	jq(function(){
		jq('#post_form').submit(function(){
			var form = jq(this);
			submit_tag_input();
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
			if( ' ' === lastcode ){
				submit_tag_input();
			}
		});

		function submit_tag_input(){
			var input = tags_input;
			var val = input.val();
			var trim_val = val.replace(/(^\s*)|(\s*$)/g, "");
			if( trim_val.length > 0){
				console.log(trim_val);
				
				// remove val
				input.val('');
				
				// create buttons
				var button = jq('<span class="tag_item jf_tag"><span class="tag_val">'+trim_val+'</span><a href="#" class="remove_button">x</a></span>');
				button.find('.remove_button').click(function(){
					jq(this).closest('.tag_item').remove();
					return false;
				});
				$('#tag_line').append(button);
				
				// set value to real tags
				update_value_for_real_tags();
				
				return false;
			}
		}

		function update_value_for_real_tags(){
			var val_list = [];
			jq('#tag_line').find('.tag_val').each(function(){
				var sv = jq(this).text();
				val_list.push(sv);
			});
			console.log('val list:', val_list);
			jq('#real_tags').val( val_list.join(' ') );
		}

		// focus tag
		jq('#focus_tag_btn').click(function(e){
			e.preventDefault();

			var tagid = jq(this).attr('tagid');
			jq.post(
				WEB_ROOT + '/focus/ajaxFocus',
				{
					type: 'tag',
					target: tagid,
					dire: 'add'
				},
				function(data){
					if('success' == data.result){
						alert('关注成功');
					}else{
						alert(data.msg);
					}
				},
				'json'
			);
		});
	});
})(jQuery);
