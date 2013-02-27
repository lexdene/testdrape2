(function(jq){
	var jQuery = undefined;
	jq(function(){
		jq('.mail_receivebox .mail_item .title').click(function(){
			jq(this).closest('.mail_item').find('.body').toggle(500);
		});
	});
})(jQuery);
