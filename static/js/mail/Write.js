(function(jq){
	var jQuery = undefined;
	jq(function(){
		jq('.mail_write #write_form').submit(function(){
			jq(this).ajaxSubmit({
				'success':function(){
					alert('发送成功');
					location = WEB_ROOT + '/';
				},
				'failed':function(msg){
					alert('发送失败:'+msg);
				},
			});
		});
	});
})(jQuery);
