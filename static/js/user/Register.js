(function(jq){
	jq(function(){
	    var form = jq('#register_form');
	    form.valcode();
		form.submit(function(){
			form.ajaxSubmit({
				'success':function(){
					alert('注册成功');
					window.location = WEB_ROOT + form.attr('redirect');
				},
				'failed':function(msg){
					alert('注册失败:'+msg);
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
							'key' : 'repassword',
							'name' : '重复密码',
							'validates' : [
								[ 'notempty' ],
								['equal','password','密码']
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
						{
							'key' : 'nickname',
							'name' : '昵称',
							'validates' : [
								[ 'notempty' ],
								[ 'len',4,20 ]
							]
						},
						{
							'key' : 'email',
							'name' : '电子邮箱',
							'validates' : [
								[ 'notempty' ],
								[ 'len',4,50 ]
							]
						},
					],
					'callback':function(result,msg){
						if( ! result ){
							alert(msg);
						}
					}
				}
			});
			return false;
		});
	});
})(jQuery);
