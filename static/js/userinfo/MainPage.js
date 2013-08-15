(function(jq){
	var jQuery = undefined;

	jq(function(){
		// focus
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

		var current_page = 0;
		var total_page = 0;
		var template = _.template(jq('#msg_template').html());
		var msg_list = jq('#msg_list');

		// tabs
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
				},
				'msg': {
					'onload': function(){
						refresh_msglist();
					}
				}
			}
		});

		function refresh_msglist(page){
			if(page == null){
				page = 0;
			}

			jq.delay(
				1000,
				function(r){
					msg_list.html(loading_html);
					jq.get(
						WEB_ROOT + '/usermsg/AjaxMsgList/to_uid/' + user_id,
						{'page':page},
						undefined,
						'json'
					).success(function(data){
						r(data);
					}).error(function(){
						r({
							'errormsg': '系统错误',
							'data': []
						});
					});
				},
				function(data){
					if( '' === data['errormsg'] ){
						current_page = data.page;
						total_page = Math.ceil(data.count / data.per_page);

						msg_list.html(template({
							'msg_list': data.data,
							'formate_date': jq.create_format_date(data.now)
						}));
						var page_str = current_page + 1;
						jq('#page_count').html('共' + page_str + '/' + total_page + '页');
					}else{
						msg_list.html(error_html + data['errormsg']);
					}
				}
			);
		}

		jq('#page_buttons').find('.jf_button').click(function(e){
			e.preventDefault();
			var target_page;
			if( 'prev' == jq(this).attr('action') ){
				target_page = current_page - 1;
			}else{
				target_page = current_page + 1;
			}
			if( target_page < 0 || target_page >= total_page ){
				return;
			}

			refresh_msglist(target_page);
		});

		// msg
		(function(){
			var form = jq('#msg_form');
			form.submit(function(){
				form.ajaxSubmit({
					'success': function(){
						form.find('textarea').val('');
						alert('留言成功');
						refresh_msglist();
					},
					'error': function(msg){
						l(msg);
					},
					'validate': {
						'form_area': [
							{
								'key': 'text',
								'name': '留言内容',
								'validates': [
									['len', 1, 200]
								]
							}
						]
					}
				});
			});
		})();
	});
})(jQuery);
