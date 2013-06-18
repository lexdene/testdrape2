/*
 * drape jquery extend
 */
(function(jq) {
	var jQuery = undefined;
	function ajaxSubmit(form,options){
		var form = jq(form);
	    /**
	      type : validate / post / network
	      */
	    function on_error(type,message){
		clear_error();
		show_error(message);
		if( typeof options.error == 'function' ){
		    options.error(type,message)
		}
	    }
	    function show_error(message){
		form.append('<div class="jf_form_error">'+message+'</div>');
	    }
	    function clear_error(){
		form.find('.jf_form_error').remove();
	    }

	    form.find('input').focus(function(){
		clear_error();
	    });

		var senddata = {};
		var inputlist = form.find('input,textarea');
		inputlist.each(function(){
			var name = jq(this).attr('name');
			if( name == undefined ){
				return ;
			}
			var value = jq(this).val();
			var type = jq(this).attr('type');
			switch(type){
			case 'text':
			case 'password':
			default:
				senddata[name] = value;
				break;
			case 'radio':
				if( jq(this).attr('checked') == 'checked'){
					senddata[name] = value;
				}else{
					senddata[name] = '';
				}
				break;
			case 'checkbox':
			    if( jq(this).prop('checked') ){
				senddata[name] = 'on';
			    }else{
				senddata[name] = 'off';
			    }
			    break;
			}
		});
		// validate
		if( typeof options.validate == 'object' ){
			var i,j;
			var rtn = {
				result:true,
				msg:''
			};
			for(i in options.validate.form_area){
				var val_area = options.validate.form_area[i];
				var key = val_area.key;
				var val = senddata[key];
				var name = val_area.name;
				for(j in val_area.validates){
					var validate = val_area.validates[j];
					var method = validate[0];
					switch(method){
					case 'notempty':
						if( '' == val ){
							rtn.result = false;
							rtn.msg += name+'内容不能为空;';
						}
						break;
					case 'int':
						if( ! val.match(/^[0-9]+$/) ){
							rtn.result = false;
							rtn.msg += '内容必须为数字;';
						}
						break;
					case 'len':
						if( val.length < validate[1] || val.length > validate[2] ){
							rtn.result = false;
							rtn.msg += name+'的长度必须在['+validate[1]+','+validate[2]+']之间,您输入的长度为'+val.length;
						}
						break;
					case 'equal':
						if( val != senddata[ validate[1] ] ){
							rtn.result = false;
							rtn.msg += name+'的内容必须和'+validate[2]+'相同;';
						}
						break;
					case 'min-length':
						if( val.length < vil[1] ){
							rtn.result = false;
							rtn.msg += '内容的长度不得少于`'+vil[1]+'`;';
						}
						break;
					case 'max-length':
						if( val.length > vil[1] ){
							rtn.result = false;
							rtn.msg += '内容的长度不得超过`'+vil[1]+'`;';
						}
						break;
					case 'userdef':
						var fun = eval( vil[1] );
						var validate_rtn = fun( o,val ,vil);
						if( false == validate_rtn.result ){
							rtn.result = false;
							rtn.msg += validate_rtn.msg+';';
						}
						break;
					default:
						rtn.result = false;
						rtn.msg += '未知验证:`'+method+'`;';
					}
					if( ! rtn.result ){
						rtn.msg += '\n';
					}
				}
			}
			if( ! rtn.result ){
				on_error('validate',rtn.msg)
				return false;
			}
		}
		inputlist.attr('disabled',true);

		var url = form.attr('action');
		jq.post(
			url,
			senddata,
			function(){},
			'json'
		)
		.success(function(rspdata){
			switch(rspdata.result){
			case 'success':
				if( typeof options.success == 'function' ){
					options.success(rspdata);
				}
				break;
			case 'failed':
				if( rspdata.msg ){
				    on_error('post',rspdata.msg);
				}else{
				    on_error('post','no message');
				}
				break;
			default:
				break;
			}
			inputlist.attr('disabled',false);
		})
		.error(function(){
		    on_error('network','服务器错误，请联系网站管理员');
			inputlist.attr('disabled',false);
		})
	}
	jq.fn.extend({
		ajaxSubmit: function(options) {
			return this.each(function(){
				ajaxSubmit(this,options);
			});
		},
		img_refresh : function(){
			return this.each(function(){
				var src = jq(this).attr('src');
				var cleansrc = src.split('?')[0];
				var newsrc = cleansrc+'?t='+new Date().getTime();
				jq(this).attr('src',newsrc);
			});
		},
	    refresh_valcode : function(){
		var form = this;
		form.find('.jf_valcode_input').val('');
		form.find('.jf_valcode_img').img_refresh();
		return this;
	    },
	    valcode : function(){
		var form = this;
		form.find('.jf_valcode_btn').click(function(){
		    form.refresh_valcode();
		});
		return this;
	    },
		count_down: function(options) {
			return this.each(function(){
				var numObj = jq(this).find('.'+options['num_class']);
				var locationObj = jq(this).find('.'+options['location_class']);
				var location = locationObj.attr('href');
				var time = options['time'];
				numObj.html( time );
				var timer = setInterval(
					function(){
						--time;
						numObj.html( time );
						if( time <= 0 ){
							clearInterval( timer );
							window.location = location;
						}
					},
					1000
				);
			});
		}
		,centerInWindow : function(){
			return this.each(function(){
				var jwin = jq(window);
				var jdoc = jq(document);
				var obj = jq(this);
				var top = ( jwin.height() - obj.height() ) /2;
				var left = ( jwin.width() - obj.width() ) /2;
				var scrollTop = jdoc.scrollTop();
				var scrollLeft = jdoc.scrollLeft();
				obj.css({
					position : 'absolute',
					top : top + scrollTop,
					left : left + scrollLeft
				}).show();
			});
		}

		// 动画，将浏览器滚动至当前元素
		,jump: function(elapse){
			if( typeof elapse == 'undefined' ){
				elapse = 300;
			}
			if(this.length > 0 ){
				var _targetTop = this.offset().top;
				jq("html,body").animate({scrollTop:_targetTop},elapse);
			}
		}
		,tabs: function(options){
			onhashchange = function(event){
				changePageByHash();
			}
			var jobj = this;
			function changePage(pagename){
				jobj.find('.tab_page').hide();
			    var selected_page = jobj.find('.tab_page[tab_page='+pagename+']');
				selected_page.show();
				jobj.find('.tab_nav').find('.nav_btn').closest('.nav_btn_wrap').removeClass('nav_btn_active');
				jobj.find('.tab_nav').find('.nav_btn[tab_page='+pagename+']').closest('.nav_btn_wrap').addClass('nav_btn_active');
			    
			    // trigger on load function
			    try{
				options['pages'][pagename].onload.call( selected_page.get(0) )
			    }catch(e){
			    }
			}
			function showFirstPage(){
				changePage( jobj.find('.tab_page').first().attr('tab_page') );
			}
			function changePageByHash(){
				var tab_page = location.hash.substr(2);
				if( '' == tab_page ){
					showFirstPage();
				}else{
					// is start with #!
					if( location.hash.indexOf('#!') != 0){
						return;
					}

					changePage(tab_page);
				}
			}
			changePageByHash();
		}
		,delay_load: function(time, url, templator, loading_html, fail_html){
			var loading_html = loading_html || '<img src="'+WEB_ROOT+'/static/image/loading.gif" />载入中...';
			var fail_html = fail_html || '<img src="'+WEB_ROOT+'/static/image/error.png" />载入失败！';

			var load_data = undefined;
			var isTimerFinished = false;
			var jthis = this;
			function load(){
				if( load_data && isTimerFinished ){
					if('error' == load_data){
						jthis.html(fail_html);
					}else{
						jthis.html(load_data);
					}
				}
			}

			jthis.html( loading_html );

			jq.get(url,{},null,'html')
				.success(function(data){
					templator = templator || function(s){return s;};
					load_data = templator(data);
					load();
				})
				.error(function(){
					load_data = 'error';
					load();
				});

			var timer = setTimeout(
				function(){
					isTimerFinished = true;
					load()
				},
				time
			);
			return this;
	    }
	});
	jq.extend({
		htmlEscape: function(str) {
			return String(str)
				.replace(/&/g, '&amp;')
				.replace(/"/g, '&quot;')
				.replace(/'/g, '&#39;')
				.replace(/</g, '&lt;')
				.replace(/>/g, '&gt;');
		}
		,htmlUnescape: function(value){
			return String(value)
				.replace(/&quot;/g, '"')
				.replace(/&#39;/g, "'")
				.replace(/&lt;/g, '<')
				.replace(/&gt;/g, '>')
				.replace(/&amp;/g, '&');
		}
		,delay: function(time, action, finish){
			var result = undefined;
			var isTimerFinished = false;

			function load(){
				if(result && isTimerFinished){
					finish(result);
				}
			}

			function setResult(r){
				result = r;
				load();
			}

			action(setResult);

			var timer = setTimeout(
				function(){
					isTimerFinished = true;
					load();
				},
				time
			);
		}
	});
})(jQuery);
