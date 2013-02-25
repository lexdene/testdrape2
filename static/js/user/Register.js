(function(jq){
	function refresh_valcode_img(){
		jq('.common_valcode_img').refresh();
	}
	jq(function(){
		jq('.common_valcode_btn').click(refresh_valcode_img);
		jq('#register_form').submit(function(){
			var form = jq(this);
			form.ajaxSubmit({
				'success':function(){
					alert('注册成功');
					window.location = WEB_ROOT + form.attr('redirect');
				},
				'failed':function(msg){
					form.find('input[name=valcode]').val('');
					refresh_valcode_img();
					alert('注册失败:'+msg);
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
