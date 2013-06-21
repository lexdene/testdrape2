(function(jq){
	var jQuery = undefined;

	var loading_html = '<div class="loading"><img src="'+WEB_ROOT+'/static/image/loading.gif" />载入中...</div>';
	var error_html = '<img src="'+WEB_ROOT+'/static/image/error.png" />载入失败！';
	var no_more_html = '<div class="nomore">没有更多新鲜事了</div>';
	var more_button_html = '<a href="#">更多新鲜事</a>';
	var newsfeed_template = _.template(jq('#newsfeed_template').html());

	function tile_list_data(source_list_data){
		var target_list_data = [];
		_(source_list_data).each(function(value){
			target_list_data.push(tile_data(value));
		});
		return target_list_data;
	}

	function tile_data(source_data){
		var target_data = {};
		_(source_data).each(function(value, key){
			var key_parted_list = key.split('.');
			var part_data = target_data;
			_(_(key_parted_list).initial()).each(function(key_parted){
				if(typeof part_data[key_parted] == 'undefined'){
					part_data[key_parted] = {}
				}
				part_data = part_data[key_parted];
			});
			var key_parted = _(key_parted_list).last();
			part_data[key_parted] = value;
		});
		return target_data;
	}

	function create_format_date(now){
		var today = new Date(now * 1000);
		today.setHours(0);
		today.setMinutes(0);
		today.setSeconds(0);
		today.setMilliseconds(0);
		var today_timestamp = today.getTime() / 1000;
		var yesterday_timestamp = today_timestamp - 24 * 3600;

		function format_number(n){
			if( 0 == n ){
				return '00';
			}else if(n < 10){
				return '0' + n;
			}else{
				return '' + n;
			}
		}

		function format_date(timestamp){
			var diff = now - timestamp;
			var f = format_number;
			if(timestamp < yesterday_timestamp){ // before yesterday
				var d = new Date(timestamp * 1000);
				return d.getFullYear() + '-'
					+ f((d.getMonth() + 1)) + '-'
					+ f(d.getDate()) + ' '
					+ f(d.getHours()) + ':'
					+ f(d.getMinutes());
			}else if(timestamp < today_timestamp){ // yesterday
				var d = new Date(timestamp * 1000);
				return '昨天'
					+ f(d.getHours()) + ':'
					+ f(d.getMinutes());
			}else{ // today
				if(diff < 60){ // less than 1 minute
					return '刚刚';
				}else if(diff < 3600){ // less than 1 hour
					return Math.floor(diff / 60) + '分钟前';
				}else{ // more than 1 hour
					var d = new Date(timestamp * 1000);
					return '今天'
						+ f(d.getHours()) + ':'
						+ f(d.getMinutes());
				}
			}
		}
		return format_date;
	}
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

						var loading_obj = jq(loading_html);
						var more_button_obj = jq(more_button_html);
						var from_id = -1;

						function load_newsfeed_list(){
							jthis.append(loading_obj);
							jq.delay(
								1000,
								function(r){
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
								},
								function(data){
									// remove loading
									loading_obj.remove();

									// error
									if( data.errormsg != '' ){
										jthis.append(error_html + ':' + data.errormsg);
										return;
									}

									// empty
									if(0 == data.data.length){
										jthis.append(no_more_html);
										return;
									}

									// min form_id
									data.data.forEach(function(d){
										if(-1 == from_id || d.id < from_id){
											from_id = d.id;
										}
									});

									// add html
									jthis.append(newsfeed_template({
										'newsfeed_list': tile_list_data(data.data),
										'format_date': create_format_date(data.now),
									}));
									jthis.append(more_button_obj);
									more_button_obj.click(load_more);
								}
							);
						}
						jthis.html('');
						load_newsfeed_list();

						function load_more(){
							jq(this).remove();
							load_newsfeed_list();
							return false;
						}
					}
				}
			}
		});
	});
})(jQuery);
