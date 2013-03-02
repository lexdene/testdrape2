(function(jq){
	function getBrowserVersion(){
		var Sys = {};
		var ua = navigator.userAgent.toLowerCase();
		var s;
		(s = ua.match(/msie ([\d.]+)/)) ? Sys.ie = s[1] :
		(s = ua.match(/firefox\/([\d.]+)/)) ? Sys.firefox = s[1] :
		(s = ua.match(/chrome\/([\d.]+)/)) ? Sys.chrome = s[1] :
		(s = ua.match(/opera.([\d.]+)/)) ? Sys.opera = s[1] :
		(s = ua.match(/version\/([\d.]+).*safari/)) ? Sys.safari = s[1] : 0;
		
		if (Sys.ie) return('IE:' + Sys.ie);
		if (Sys.firefox) return('Firefox:' + Sys.firefox);
		if (Sys.chrome) return('Chrome:' + Sys.chrome);
		if (Sys.opera) return('Opera:' + Sys.opera);
		if (Sys.safari) return('Safari:' + Sys.safari);
	}
	function fuckIE(){
		jq.post(
			WEB_ROOT+'/fuckie',
			function(data){
				var fuckie_block = jq('<div class="fuckie" style="display:none">'+data+'</div>');
				jq('.layout_head_line').append(fuckie_block);
				var jwin = jq(window);
				fuckie_block.height( jwin.height() - 100 );
				fuckie_block.slideDown('slow');
				// fuckie_block.find('.fuckie_index').centerInWindow();
			},
			'html'
		);
	}
	var bv = getBrowserVersion();
	var s = bv.split(':');
	switch(s[0]){
	case 'IE':
		fuckIE();
		break;
	}
})(jQuery);
