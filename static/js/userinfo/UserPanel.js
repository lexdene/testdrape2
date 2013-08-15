(function(jq){
	var jQuery = undefined;
	jq(function(){
		var d;
		function userpanel(btn, event){
			event.preventDefault();
			var userid = btn.attr('userid');
			
			// create
			if( undefined == d ){
				d = jq('<div class="userpanel"></div>');
				jq('body').append(d);
				
				// close
				jq('body').click(function(event){
					// 判断一个dom元素是否等于或包含另一个dom元素
					function is_inside(container, element){
						if( container === element ){
							return true;
						}
						if( jq.contains(container, element) ){
							return true;
						}
						return false;
					}

					// 点击在d内部
					var is_event_in_dialog = is_inside(d[0], event.target);

					// 点击在username_btn内部
					// 由于username_btn有多个
					// 不能直接通过判断是否等于btn来决定
					var is_event_in_btn = jq(event.target).hasClass('username_btn');

					var isd = (!is_event_in_dialog && !is_event_in_btn);
					if(isd){
						d.hide();
					}
				});
			}
			
			d.html(loading_html);
			
			// position
			var pos = btn.position();
			pos.left += 20;
			pos.position = 'absolute';
			d.css(pos);
			d.show();
			
			// at least 0.3 second
			// loading的画面至少要显示0.3秒
			var pageData;
			var isTimerFinished = false;
			function showPage(){
				if( pageData && isTimerFinished ){
					d.html(pageData);
				}
			}
			jq.post(
				WEB_ROOT+'/userinfo/UserPanelPage/uid/'+userid,
				{},
				function(){},
				'html'
			)
			.success(function(data){
				pageData = data;
				showPage();
			})
			.error(function(){
				d.html(error_html);
			})
			var timer = setTimeout(
				function(){
					isTimerFinished = true;
					showPage();
				},
				300
			);
		}

		jq('body').on('click', '.username_btn', function(event){
			userpanel(jq(this), event);
		});
	});
})(jQuery);
