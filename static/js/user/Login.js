(function(j){
	function refresh_valcode_img(){
		j('.common_valcode_img').refresh();
	}
	j(function(){
		j('.valcode_btn').click(refresh_valcode_img);
		j('#submit_form').submit(function(){
			var form = j(this);
			form.ajaxSubmit({
				'success':function(){
					alert('登录成功');
					window.location = WEB_ROOT + form.attr('redirect');
				},
				'failed':function(msg){
					form.find('input[name=valcode]').val('');
					refresh_valcode_img();
					alert('登录失败:'+msg);
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
