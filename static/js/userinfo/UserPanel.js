(function(jq){
	jQuery = undefined;
	jq(function(){
		var d;
		jq('.username_btn').click(function(){
			var btn = jq(this);
			var userid = btn.attr('userid');
			
			// create
			if( undefined == d ){
				d = jq('<div class="userpanel"></div>');
				jq('body').append(d);
				
				// close
				d.mouseleave(function(){
					jq(this).hide();
				});
			}
			
			d.html('<img src="'+WEB_ROOT+'/static/image/loading.gif" />载入中...');
			
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
