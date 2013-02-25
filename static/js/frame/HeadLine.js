(function(jq){
	jq(function(){
		var d;
		jq('.layout_head_line .notice_btn').click(function(){
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
			
			d.html('<img src="'+WEB_ROOT+'/static/image/loading.gif" />载入中...');
			
			// position
			var pos = btn.position();
			pos.left -= 100;
			pos.top += 20;
			d.dialog().show( {'position':pos } );
			d.css('position','fixed');
			
			// at least 0.3 second
			// loading的画面至少要显示0.3秒
			var pageData;
			var isTimerFinished = false;
			function showPage(){
				if( pageData && isTimerFinished ){
					d.html(pageData);
					d.append('<div><a href="#" onclick="return false" class="close_btn">关闭</a></div>');
					
					// close
					d.find('.close_btn').click(function(){
						d.hide();
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
