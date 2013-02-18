jQuery(function(){
	jQuery('#add_rundata').click(function(){
		AddProblem.addRunData();
		return false;
	});
	jQuery('#submit_problem').click(function(){
		var form = jQuery(this).closest('form').first();
		if( ! jdmd_widget.validate_and_error_all( form ) ){
			return false;
		}
	});
});
var AddProblem={};
var rundata_num = 0;
AddProblem.addRunData = function(){
	var sampleObj = jQuery('.rundata_sample').get(0);
	var oriCode = sampleObj.outerHTML ;
	var nCode = oriCode.replace(/{num}/g,++rundata_num);
	
	var lastRunData = jQuery('.rundata').last() ;
	var nObj = lastRunData.after( nCode ).next();
	nObj.removeClass('rundata_sample');
	
	nObj.find('.jdmd_input').attr('validate','notempty');
}
