if( jdmd_widget == undefined ){
	var jdmd_widget = {};
}
jdmd_widget.tabs = function(o){
	var jobj = jQuery(o);
	
	jobj.find('.tab_nav').find('a').click(function(){
		var page = jQuery(this).attr('tab_page');
		changePage( page );
		return false;
	});
	
	function changePage(pagename){
		jobj.find('.tab_page').hide();
		jobj.find('.tab_page[tab_page='+pagename+']').show();
		
		jobj.find('.tab_nav').find('.nav_btn').closest('.nav_btn_wrap').removeClass('nav_btn_active');
		jobj.find('.tab_nav').find('.nav_btn[tab_page='+pagename+']').closest('.nav_btn_wrap').addClass('nav_btn_active');
	}
	
	function showFirstPage(){
		changePage( jobj.find('.tab_page').first().attr('tab_page') );
	}
	
	showFirstPage();
}
