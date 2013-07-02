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
			var initial = _(key_parted_list).initial();
			_(initial).each(function(key_parted){
				if(typeof part_data[key_parted] == 'undefined'){
					part_data[key_parted] = {}
				}
				part_data = part_data[key_parted];
			});
			var key_parted = _(key_parted_list).last();
			if('object' == typeof value){
				part_data[key_parted] = tile_data(value);
			}else{
				part_data[key_parted] = value;
			}
		});
		return target_data;
	}

	function template(data){
		var tdata = tile_list_data(data.data);
		_(tdata).each(function(value){
			if('topic' == value.from_object_type && 'reply' == value.action_type){
				value.action_type = 'replied';
			}
		});
		return newsfeed_template({
			'newsfeed_list': tdata,
			'format_date': jq.create_format_date(data.now),
		});
	}

	window.newsfeed = {
		'load': function(area, data_fun){
			var loading_obj = jq(loading_html);
			var more_button_obj = jq(more_button_html);
			var from_id = -1;

			area.on('click', '.username_btn', function(event){
				jq.userpanel(jq(this), event);
			});

			function load_newsfeed_list(){
				area.append(loading_obj);

				jq.delay(
					1000,
					function(r){
						data_fun(from_id,r);
					},
					function(data){
						// remove loading
						loading_obj.remove();

						// error
						if( data.errormsg != '' ){
							area.append(error_html + ':' + data.errormsg);
							return;
						}

						// empty
						if(0 == data.data.length){
							area.append(no_more_html);
							return;
						}

						// min form_id
						data.data.forEach(function(d){
							if(-1 == from_id || d.id < from_id){
								from_id = d.id;
							}
						});

						// add html
						try{
							area.append(template(data));
							area.append(more_button_obj);
							more_button_obj.click(load_more);
						}catch(e){
							console.log(e);
							area.append(error_html + ':模板解析出错');
						}
					}
				);
			}
			area.html('');
			load_newsfeed_list();

			function load_more(){
				jq(this).remove();
				load_newsfeed_list();
				return false;
			}
		}
	}
})(jQuery);
