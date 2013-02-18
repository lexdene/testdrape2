(function(jq){
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
	});
})(jQuery);
