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
								['len',4,5000]
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
			jq(this).closest('.floor').find('.floor_edit').toggle(500);
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
								['len',4,5000]
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
	});
})(jQuery);
