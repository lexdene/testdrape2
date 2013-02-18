jQuery(function(){
	jQuery('.admin_permission').find('.userlist').change(function(){
		var uid = jQuery(this).val();
		jQuery('.admin_permission').find('.form').find('input[name=uid]').val(uid);
	});
	
	jQuery('.admin_permission').find('.form').find('input[type=submit]').click(function(){
		var form = jQuery(this).closest('form').first();
		if( ! jdmd_widget.validate_and_error_all( form ) ){
			return false;
		}
	});
});
