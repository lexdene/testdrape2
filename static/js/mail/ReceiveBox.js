(function(jq){
	var jQuery = undefined;
	jq(function(){
		jq('.mail_receivebox .mail_item .title').click(function(e){
			e.preventDefault();
			jq(this).closest('.mail_item').find('.body').fadeToggle('slow');
		});
	});
})(jQuery);
