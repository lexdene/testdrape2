(function(jq){
	var jQuery = undefined;
	jq(function(){
		var d;
		jq('.layout_head_line .notice_btn').click(function(e){
			e.preventDefault();
			var btn = jq(this);
			
			// create
			if( undefined == d ){
				d = jq('<div class="notice_dialog" style="display:none"></div>');
				jq('body').append(d);
			}
			if(d.css('display') != 'none' ){
				d.hide();
				return ;
			}
			
			d.html(loading_html);
			
			// position
			var pos = btn.position();
			pos.left -= 100;
			pos.top += 20;
			pos.position = 'fixed';
			d.css( pos );
			d.show();
			
			// at least 0.3 second
			// loading的画面至少要显示0.3秒
			var pageData;
			var isTimerFinished = false;
			function showPage(){
				if( pageData && isTimerFinished ){
					d.html(pageData);
					d.append('<div><a href="#" class="close_btn">关闭</a></div>');
					
					// close
					d.find('.close_btn').click(function(e){
						e.preventDefault();
						d.hide();
					});
					
					// set is read
					d.find('.notice_item').click(function(){
						var notice_item = jq(this);
						var noticeid = notice_item.attr('noticeid');
						jq.post(
							WEB_ROOT+'/notice/setIsRead',
							{noticeid:noticeid},
							function(data){
								if( 'success' == data.result ){
									notice_item.remove();
									var count = btn.find('.count').html();
									btn.find('.count').html(count-1);
								}
							},
							'json'
						)
					});
				}
			}
			jq.post(
				WEB_ROOT+'/notice/Panel',
				{},
				function(){},
				'html'
			)
			.success(function(data){
				pageData = data;
				showPage();
			})
			.error(function(){
				d.html('载入失败');
			})
			var timer = setTimeout(
				function(){
					isTimerFinished = true;
					showPage();
				},
				300
			);
		});
	});
})(jQuery);
