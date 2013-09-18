/*
 * drape jquery extend
 * version 1.0
 */
(function(jq) {
	var jQuery = undefined;
	jq.fn.extend({
		centerInWindow : function(){
			return this.each(function(){
				var jwin = jq(window);
				var jdoc = jq(document);
				var obj = jq(this);
				var top = ( jwin.height() - obj.height() ) /2;
				var left = ( jwin.width() - obj.width() ) /2;
				var scrollTop = jdoc.scrollTop();
				var scrollLeft = jdoc.scrollLeft();
				obj.css({
					position : 'absolute',
					top : top + scrollTop,
					left : left + scrollLeft
				}).show();
			});
		}

		// 动画，将浏览器滚动至当前元素
		,jump: function(elapse){
			if( typeof elapse == 'undefined' ){
				elapse = 300;
			}
			if(this.length > 0 ){
				var _targetTop = this.offset().top - ($(window).height() - this.outerHeight(true)) / 2;
				jq("html,body").animate({scrollTop:_targetTop},elapse);
				this.addClass('jf_flash_out');
				var me = this;
				this.bind(
					"animationend webkitAnimationEnd oAnimationEnd MSAnimationEnd",
					function(){
						me.removeClass('jf_flash_out');
					}
				);
			}
		}
	});
	jq.extend({
		htmlEscape: function(str) {
			return String(str)
				.replace(/&/g, '&amp;')
				.replace(/"/g, '&quot;')
				.replace(/'/g, '&#39;')
				.replace(/</g, '&lt;')
				.replace(/>/g, '&gt;');
		}
		,htmlUnescape: function(value){
			return String(value)
				.replace(/&quot;/g, '"')
				.replace(/&#39;/g, "'")
				.replace(/&lt;/g, '<')
				.replace(/&gt;/g, '>')
				.replace(/&amp;/g, '&');
		}
		,delay: function(time, action, finish){
			var result = undefined;
			var isTimerFinished = false;

			function load(){
				if(result && isTimerFinished){
					finish(result);
				}
			}

			function setResult(r){
				result = r;
				load();
			}

			action(setResult);

			var timer = setTimeout(
				function(){
					isTimerFinished = true;
					load();
				},
				time
			);
		}
	});

	function format_number(n){
		if( 0 == n ){
			return '00';
		}else if(n < 10){
			return '0' + n;
		}else{
			return '' + n;
		}
	}

	function create_format_date(now){
		now = new Date(now);
		var today = new Date(now);
		today.setHours(0);
		today.setMinutes(0);
		today.setSeconds(0);
		today.setMilliseconds(0);
		var yesterday = today - 24 * 3600 * 1000;

		function format_date(to_time){
			to_time = new Date(to_time);
			var diff = (now - to_time) / 1000;
			var f = format_number;
			if(to_time < yesterday){ // before yesterday
				var d = to_time;
				return d.getFullYear() + '-'
					+ f((d.getMonth() + 1)) + '-'
					+ f(d.getDate()) + ' '
					+ f(d.getHours()) + ':'
					+ f(d.getMinutes());
			}else if(to_time < today){ // yesterday
				var d = to_time;
				return '昨天'
					+ f(d.getHours()) + ':'
					+ f(d.getMinutes());
			}else{ // today
				if(diff < 60){ // less than 1 minute
					return '刚刚';
				}else if(diff < 3600){ // less than 1 hour
					return Math.floor(diff / 60) + '分钟前';
				}else{ // more than 1 hour
					var d = to_time;
					return '今天'
						+ f(d.getHours()) + ':'
						+ f(d.getMinutes());
				}
			}
		}
		return format_date;
	}

	jq.extend({
		create_format_date: create_format_date
	});

})(jQuery);
