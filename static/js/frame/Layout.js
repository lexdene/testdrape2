window.onload =  function(){
	var bv = frontpage.getBrowserVersion();
	var s = bv.split(':');
	switch(s[0]){
	case 'IE':
		frontpage.fuckIE();
		return ;
		break;
	}
}
var frontpage = {};
frontpage.getBrowserVersion = function(){
	var Sys = {};
	var ua = navigator.userAgent.toLowerCase();
	var s;
	(s = ua.match(/msie ([\d.]+)/)) ? Sys.ie = s[1] :
	(s = ua.match(/firefox\/([\d.]+)/)) ? Sys.firefox = s[1] :
	(s = ua.match(/chrome\/([\d.]+)/)) ? Sys.chrome = s[1] :
	(s = ua.match(/opera.([\d.]+)/)) ? Sys.opera = s[1] :
	(s = ua.match(/version\/([\d.]+).*safari/)) ? Sys.safari = s[1] : 0;
	
	//以下进行测试
	if (Sys.ie) return('IE:' + Sys.ie);
	if (Sys.firefox) return('Firefox:' + Sys.firefox);
	if (Sys.chrome) return('Chrome:' + Sys.chrome);
	if (Sys.opera) return('Opera:' + Sys.opera);
	if (Sys.safari) return('Safari:' + Sys.safari);
}


frontpage.fuckIE = function(){
	if( window.location.pathname != WEB_ROOT+'/fuckie' ){
		window.location = WEB_ROOT+'/fuckie';
	}
}
