(function(jq){
	var jQuery = undefined;

	jq(function(){
		var focus_button = jq('#focus_button');
		function loadText(){
			if( 'True' == focus_button.attr('isfocused') ){
				focus_button.html('取消关注');
			}else{
				focus_button.html('关注Ta');
			}
		}
		function getDire(){
			if( 'True' == focus_button.attr('isfocused') ){
				return 'remove';
			}else{
				return 'add';
			}
		}
		loadText();
		focus_button.click(function(){
			jq.post(
				WEB_ROOT + '/focus/ajaxFocus',
				{
					type: 'user',
					target: user_id,
					dire: getDire(),
				},
				function(data){
					console.log(data);
					if('success' == data.result){
						if( 'True' == focus_button.attr('isfocused') ){
							focus_button.attr('isfocused', 'False');
							alert('取消关注成功');
						}else{
							focus_button.attr('isfocused', 'True');
							alert('关注成功');
						}
						loadText();
					}else{
						alert(data.msg);
					}
				},
				'json'
			);
			return false;
		});
		jq('#tabs').tabs({
			'pages': {
				'topic': {
					'onload': function(){
						jq(this).delay_load(
							1000,
							WEB_ROOT + '/userinfo/UserTopicList/uid/' + user_id
						);
					}
				},
				'newsfeed': {
					'onload': function(){
						var jthis = jq(this);
						newsfeed.load(
							jthis,
							function(from_id,r){
								jq.get(
									WEB_ROOT + '/userinfo/ajaxUserActionList/uid/' + user_id,
									{
										'from_id': from_id
									},
									undefined,
									'json'
								).success(function(data){
									r(data);
								}).error(function(){
									r({
										'errormsg': '系统错误，请联系网站管理员',
										'data': []
									});
								});
							}
						);
					}
				}
			}
		});
	});
})(jQuery);
