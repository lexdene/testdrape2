(function(j){
	j(function(){
	    var form = j('#submit_form');
	    form.valcode();
		form.submit(function(){
			form.ajaxSubmit({
				'success':function(){
					alert('登录成功');
					window.location = WEB_ROOT + form.attr('redirect');
				},
				'error':function(msg){
				    form.refresh_valcode();
				},
				'validate':{
					'form_area':[
						{
							'key':'loginname',
							'name':'登录名',
							'validates' : [
								[ 'notempty' ],
								[ 'len',4,20 ]
							]
						},
						{
							'key' : 'password',
							'name' : '密码',
							'validates' : [
								[ 'notempty' ],
								[ 'len',4,20 ]
							]
						},
						{
							'key' : 'valcode',
							'name' : '验证码',
							'validates' : [
								[ 'notempty' ],
								[ 'len',4,4 ]
							]
						},
					],
				}
			});
			return false;
		});
	});
})(jQuery);
