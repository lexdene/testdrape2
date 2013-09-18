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
		delay: function(time, action, finish){
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
})(jQuery);
