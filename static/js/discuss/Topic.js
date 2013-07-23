(function(jq){
	jq(function(){
		var form = jq('#reply_form');
		form.submit(function(){
			form.ajaxSubmit({
				'success':function(){
					alert('回复成功');
					location.reload();
				},
				'failed':function(msg){
					alert('回复失败:'+msg);
				},
				'validate':{
					'form_area':[
						{
							'key' : 'text',
							'name' : '回复',
							'validates' : [
								['notempty'],
								['len',4,25000]
							]
						},
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
		jq('.reply_button').click(function(){
			var floorObj = jq(this).closest('.floor');
			var floor_num = floorObj.attr('floor_num');
			var floor_id = floorObj.attr('floor_id');
			var reply_to_hint = form.find('.reply_to_hint');
			reply_to_hint.find('.floor_num').html(floor_num);
			form.find('input[name=reply_to_id]').val(floor_id);
			reply_to_hint.show();
			form.jump();
		});
		form.find('.cancel_reply_button').click(function(){
			var reply_to_hint = form.find('.reply_to_hint');
			reply_to_hint.hide();
			reply_to_hint.find('.floor_num').html(-1);
			form.find('input[name=reply_to_id]').val(-1);
		});
		jq('.reply_to_reply').find('.jump_button').click(function(){
			var reply_to_id = jq(this).closest('.reply_to_reply').attr('reply_to_id');
			jq('.floor[floor_id='+reply_to_id+']').jump();
		});
		jq('.edit_button').click(function(){
			var edit_button = jq(this);
			var floor = jq(this).closest('.floor').find('.floor_content');
			var edit = floor.find('.floor_edit');
			if( 'none' == edit.css('display') ){
				var text = floor.find(markdown_selector).text();
				edit.find('textarea').val( jq.htmlUnescape( text ) );
				edit_button.text('取消编辑');
			}else{
				// 取消编辑
				edit.find('textarea').val('');

				var text = floor.find(markdown_selector).text();
				floor.find('.jf_markdown').html( transText(text) );

				edit_button.text('编辑');
			}
			edit.slideToggle('slow');
		});
		jq('.floor .floor_edit textarea').keyup(function(event){
			var escape_text =  jq.htmlEscape( jq(this).val() ) ;
			jq(this).closest('.floor').find('.floor_content .jf_markdown').html( transText(escape_text) );
		});
		jq('.edit_form').submit(function(){
			jq(this).ajaxSubmit({
				'success':function(){
					alert('修改成功');
					location.reload();
				},
				'failed':function(msg){
					alert('修改失败:'+msg);
				},
				'validate':{
					'form_area':[
						{
							'key' : 'text',
							'name' : '回复',
							'validates' : [
								['notempty'],
								['len',4,25000]
							]
						},
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
		var markdown_selector = 'script[type="text/markdown"]';
		jq(markdown_selector).each(function(){
			var text = this.textContent;
			jq(this).parent().find('.jf_markdown').html(transText( text ));
		});

		// focus topic
		var focus_button = jq('#focus_topic_btn');
		focus_button.click(function(e){
			e.preventDefault();
			jq.post(
				WEB_ROOT + '/focus/ajaxFocus',
				{
					type: 'topic',
					target: topic_id,
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
