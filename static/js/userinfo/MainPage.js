(function(jq){
    var jQuery = undefined;
    var user_topic_list_cache = [];
    var user_topic_list_page = 0;
	jq(function(){
	    jq('#tabs').tabs({
		'pages':{
		    'topic':{
			'onload':function(){
			    var page_container = this;
			    jq(this).delay_load(
				1000,
				WEB_ROOT + '/userinfo/UserTopicList/uid/'+user_id
			    );
			}
		    }
		}
	    });
	});
})(jQuery);
