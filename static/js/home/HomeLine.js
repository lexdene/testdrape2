(function(jq){
	var jQuery = undefined;
	jq(function(){
		// check user login
		if(my_userid < 0){
			alert('请先登录' + my_userid);
			location = WEB_ROOT + '/user/Login';
			return;
		}

		// content area
		newsfeed.load(
			jq('#content-area'),
			function(from_id,r){
				jq.getJSON(
					WEB_ROOT + '/home/AjaxHomeLine',
					{
						from_id: from_id,
					},
					function(data){
						r(data);
					}
				).error(function(){
					r({
						'errormsg': '系统错误，请联系网站管理员',
						'data': []
					});
				});
			}
		);
	});
})(jQuery);
