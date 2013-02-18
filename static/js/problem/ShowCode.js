var ShowCode={};
ShowCode.init = function(){
	var language = this.analyseLanguage();
	var preObj = jQuery('pre');
	preObj.addClass('sh_'+language);
	
	ShowCode.getUserTheme(function(theme){
		var select = document.getElementById('themeSelect');
		var i;
		for(i=0;i<select.options.length;++i){
			if( select.options[i].innerHTML == theme ){
				select.selectedIndex = i;
				break;
			}
		}
		try{
			loadStyle();
		}catch(e){
		}
		sh_highlightDocument('/static/shjs-0.6/lang/', '.js');
		
		jQuery('#themeSelect').change(function(){
			ShowCode.setUserTheme(jQuery(this).val());
		});
	});
}
ShowCode.analyseLanguage=function(){
	return 'cpp';
}
ShowCode.getUserTheme = function(cb){
	jQuery.post(
		'/user/UserSetting',
		{
			'key':'problem/ShowCode/theme',
		},
		function(data){
			cb(data['newvalue']);
		},
		'json'
	)
	.error(function(){
		cb('emacs');
	});
}
ShowCode.setUserTheme = function(theme){
	jQuery.post(
		'/user/UserSetting',
		{
			'key':'problem/ShowCode/theme',
			'value':theme
		},
		function(data){},
		'json'
	);
}

jQuery(function(){
	ShowCode.init();
});
