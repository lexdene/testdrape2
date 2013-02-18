(function(jq){
	jq(function(){
		jq('#changePassword_form').submit(function(){
			var form = jq(this);
			form.ajaxSubmit({
				'success':function(){
					alert('修改成功');
					location.reload();
				},
				'failed':function(msg){
					alert('修改失败:'+msg);
				}
			});
			return false;
		});
	});
})(jQuery);
