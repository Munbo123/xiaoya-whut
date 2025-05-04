document.body.onload=a; 

function a(){
	document.cookie = "cas_hash=" + encodeURIComponent(window.location.hash) ;
	if(window.localStorage){
		//重新登录的时候清除掉localStorage
		window.localStorage.clear();
	}
	if(window.sessionStorage){
		//重新登录的时候清除掉sessionStorage
		window.sessionStorage.clear();
	}

	var setting = {
		imageWidth : 1680,
		imageHeight : 1050

	};
	var windowHeight = $(window).height();
	var windowWidth = $(window).width();

	var init = function(){
		$(".login_conatiner").height(windowHeight).width(windowWidth);
		$("#container_bg").height(windowHeight).width(windowWidth);
		$("#login_right_box").height(windowHeight);
		var imgW = setting.imageWidth;
		var imgH = setting.imageHeight;
		var ratio = imgH / imgW; //图片的高宽比
	
		imgW = windowWidth; //图片的宽度等于窗口宽度
		imgH = Math.round(windowWidth * ratio); //图片高度等于图片宽度 乘以 高宽比
	
		if(imgH < windowHeight){ //但如果图片高度小于窗口高度的话
			imgH = windowHeight; //让图片高度等于窗口高度
			imgW = Math.round(imgH / ratio); //图片宽度等于图片高度 除以 高宽比
		}
		$(".login_img_01").width(imgW).height(imgH);  //设置图片高度和宽度
	};
	init();
	$(window).resize(function(){
		init();
	});
	
	//密码找回的中英文切换
	if($("#change_language").attr("value") == "中文"){
		$("#pwd_url").attr("href",$("#pwd_url").attr("href")+"?locale=en");
	}else{
		$("#pwd_url").attr("href",$("#pwd_url").attr("href")+"?locale=zh_CN");
	}
	$("#change_language").unbind("click").click(function(){
		var re=eval('/(locale=)([^&]*)/gi');  
	    var url = window.location.href;
		if($("#change_language").attr("value") == "中文"){
			if(url.indexOf("locale") >= 0 ) { 
				url=url.replace(re,'locale=zh_CN');
				location.href=url;
			}else{
				if(url.indexOf("?") >= 0){
					location.href=url+"&locale=zh_CN";					
				}else{
					location.href=url+"?locale=zh_CN";
				}
			}
		}else if($("#change_language").attr("value") == "English") {
			if(url.indexOf("locale") >= 0 ) { 
				url=url.replace(re,'locale=en');
				location.href=url;
			}else{
				if(url.indexOf("?") >= 0){
					location.href=url+"&locale=en";					
				}else{
					location.href=url+"?locale=en";
				}
			}
		}
	});
	//初始化点击事件
	initPassWordEvent();
} 

function login(){
	var $u = $("#un") , $p=$("#pd");
	var u = $u.val().trim();
	if(u==""){
		$u.focus();
		$u.parent().addClass("login_error_border");
		return ;
	}
	
	var p = $p.val().trim();
	if(p==""){
		$p.focus();
		$p.parent().addClass("login_error_border");
		return ;
	}
	
	$u.attr("disabled","disabled");
	$p.attr("disabled","disabled");
	
	//防止记录错误密码，每次要刷新记住的密码
	if($("#rememberName").is(":checked")){
		//不等于空，写cookie
		setCookie('neusoft_cas_un' , u , 7);
		setCookie('neusoft_cas_pd' , strEnc(p,'neusoft','cas','pd') , 7);
	}
	
	var lt = $("#lt").val();
	
	//获取key
	$.ajax({
		 url : "rsa?skipWechat=true",
		 dataType : "json",
		 type : "POST",
		 success:function(data){
			var encrypt = new JSEncrypt();
			encrypt.setPublicKey(data.publicKey);
			$("#ul").val(encrypt.encrypt(u));
			$("#pl").val(encrypt.encrypt(p));
			$("#loginForm")[0].submit();
		 }
	});
	
}

//初始化登录页事件
function initPassWordEvent(){
	var passwordhtml = document.getElementById("password_template").innerHTML;
	var qrcodehtml = document.getElementById("qrcode_template").innerHTML;
	var loginByMobile_template = document.getElementById("mobile_template").innerHTML;
	$("#index_login_btn").click(function(){
		login();
	}); 
	//点击记住账号密码
	$("#rememberName").change(function(){
		if($(this).is(":checked")){
			var $u = $("#un").val() ;
			var $p = $("#pd").val() ;
			if($.trim($u)==''||$.trim($p)==''){
				$("#errormsg").text("账号和密码不能为空").show();
				$(this).prop("checked", false);
			}else{
				//不等于空，写cookie
				setCookie('neusoft_cas_un' , $u , 7);
				setCookie('neusoft_cas_pd' , strEnc($p,'neusoft','cas','pd') , 7);
			}
		}else{
			//反选之后清空cookie
			clearCookie('neusoft_cas_un');
			clearCookie('neusoft_cas_pd');
		}
	});
	//获取cookie值
	var cookie_u = getCookie('neusoft_cas_un');
	var cookie_p = getCookie('neusoft_cas_pd');
	if(cookie_u&&cookie_p){
		$("#un").val(cookie_u);
		$("#pd").val(strDec(cookie_p,'neusoft','cas','pd'));
		$("#rememberName").attr("checked","checked");
	}
	
	//用户名文本域keyup事件
	$("#un").keyup(function(e){
		if(e.which == 13) {
			
			login();
	    }
	}).keydown(function(e){
		$("#errormsg").hide();
	}).focus();
	
	//密码文本域keyup事件
	$("#pd").keyup(function(e){
		if(e.which == 13) {
			login();
	    }
	}).keydown(function(e){
		$("#errormsg").hide();
	});
	
	//如果有错误信息，则显示
	if($("#errormsghide").text()){
		$("#errormsg").text($("#errormsghide").text()).show();
		$("#errormsg").css("width", "100%");
	}
	//重新获取验证码
	$("#codeImage").click(function(){
    	$("#codeImage").attr("src", "code?"+Math.random()) ;
    });
	//触发如何使用360极速模式图片
	$("#open_360").mouseover(function(){
		$("#open_360_img").show();
	}).mouseout(function(){
		$("#open_360_img").hide();
	});
	// 点击账号登录
	$("#password_login").unbind().click(function(){
		$("#password_login").addClass("active");
		$("#qrcode_login").removeClass("active");
		$("#loginByMobile").removeClass("active");
		$("#login_content").html(passwordhtml);
		initPassWordEvent();
		$("#errormsg").hide();
		$(this).unbind();
	});
	// 点击扫码登录
	$("#qrcode_login").unbind().click(function(){
		$("#password_login").removeClass("active");
		$("#qrcode_login").addClass("active");
		$("#loginByMobile").removeClass("active");
		$("#login_content").html(qrcodehtml);
		//微信企业号扫码登录
		var lqrcode = new loginQRCode("qrcode",153,153);
		lqrcode.generateLoginQRCode(function(result){
			window.location.href = result.redirect_url;
		});
		//触发如何使用360极速模式图片
		$("#open_360").mouseover(function(){
			$("#open_360_img").show();
		}).mouseout(function(){
			$("#open_360_img").hide();
		});
		initPassWordEvent();
		$("#errormsg").hide();
		$(this).unbind();
	});
	// 手机验证码登录
	$("#loginByMobile").unbind().click(function(){
		$("#errormsg").hide();
		$("#password_login").removeClass("active");
		$("#qrcode_login").removeClass("active");
		$("#loginByMobile").addClass("active");
		$("#login_content").html(loginByMobile_template);
		initPassWordEvent();
		$("#errormsg").hide();
		loginByMobile();

		$(this).unbind();
	});
}


function loginByMobile(){
	document.cookie = "loginType" + "=" + "loginByMobile" + "; " ;

	//手机号文本域keyup事件
	$("#loginMobile").keyup(function(e){
	}).keydown(function(e){
		$("#errormsg").hide();
	}).focus();

	//图形验证码文本域keyup事件
	$("#sendConfirm").keyup(function(e){
	}).keydown(function(e){
		$("#errormsg").hide();
	});

	//短信验证码文本域keyup事件
	$("#phoneCode").keyup(function(e){
	}).keydown(function(e){
		$("#errormsg").hide();
	});

	//重新获取验证码
	$("#codeImage").attr("src", "code?"+Math.random()) ;
	$("#codeImage").unbind("click").bind("click",function(){
		$("#codeImage").attr("src", "code?"+Math.random()) ;
	});

	//手机正则表达[1开头11位]
	let mreg = /^0?1\d{10}$/;

	//验证码相关的校验
	$("#getMobileVerifyCode").unbind("click").bind("click", function () {
		if($(this).html().indexOf($("#getPhoneCodeText").text())===-1){
			return;
		}
		//需要填写手机号码才能发送验证码
		let mobile = $("#loginMobile").val();
		let sendConfirm = $("#sendConfirm").val();
		if($.trim(mobile) == ""||!mreg.test(mobile)){
			$("#errormsg").text("手机号格式错误");
			toAlertInfo();
			return false;
		}
		else if($.trim(sendConfirm) == ""){
			$('#errormsg').text("验证码不能为空");
			toAlertInfo();
			return false;
		}
		else{
			$.post("loginByMorE", {
				"method": "sendMobileCode",
				"sendConfirm": sendConfirm,
				"mobile": mobile,
				"random": Math.random()
			}, function (data) {
				if (data.result == "false") {
					$("#codeImage").trigger("click");
					$("#errormsg").text(data.error).css("width", "100%");
					toAlertInfo();
				} else {
					//先禁用按钮以避免连续重复提交
					$("#getMobileVerifyCode").attr("disabled", "disabled");
					$("#errormsg").text("发送成功，验证码有效期5分钟，请注意查收");
					$("#errormsg").css("width", "100%");
					toAlertInfo();
					const intDiff = parseInt(60);//倒计时总秒数量
					dglogintimer(intDiff);
				}
			});
		}
	});
	$("#finishloginbymobile").click(function(){
		//验证手机号码
		let mobile = $("#loginMobile").val();
		if($.trim(mobile) == ""||!mreg.test(mobile)){
			$('#errormsg').text("手机号格式错误");
			toAlertInfo();
			return false;
		}
		//验证手机动态验证码
		let mobilecode = $("#phoneCode").val();
		if($.trim(mobilecode) == ""||mobilecode.length!=6){
			$('#errormsg').text("动态验证码错误");
			toAlertInfo();
			return false;
		}
		$.post("loginByMorE", {
			"method": "login",
			"mobile": mobile,
			"mobileCode": mobilecode,
			"random": Math.random(),
			"service": $.getUrlParam("service")
		}, function (data) {
			//选择登录账号
			if (Boolean(data.result)) {
				accountlist = data.numberlist;
				let accountHtml = document.getElementById("chooseloginid").innerHTML;
				$("#accountForm").html(accountHtml);
				let icon = "01";
				for (let i = 0; i < accountlist.length; i++) {
					let id_number = accountlist[i].ID_NUMBER;
					let codename = accountlist[i].CODENAME;
					let unitname = accountlist[i].UNIT_NAME;
					switch (accountlist[i].CODENAME) {
						case "本科生":
							icon = "01";
							break;
						case "教工":
							icon = "02";
							break;
						case "公众用户":
							icon = "03";
							break;
						case "家长":
							icon = "04";
							if (Boolean(accountlist[i].CHILD_USER_NAME)) {
								codename = accountlist[i].CHILD_USER_NAME + " " + accountlist[i].CODENAME
							}
							break;
						case "其他人员":
							icon = "05";
							break;
						case "企业用户":
							icon = "06";
							break;
						default:
							icon = "05";
					}
					$("#numberlist").append('<div class="popup-list cl-after list-' + icon + '" name="numbercard" data-value="' + i + '">' +
						'<div class="list-icon pull-left">' +
						'<img src="comm/image/bg/popup-list-' + icon + '.png" alt="">' +
						'</div>' +
						'<div class="list-text pull-left">' +
						'<p class="job">' + codename + ' ' + id_number + '</p>' +
						'<p class="add">' + unitname + '</p>' +
						'</div>' +
						'</div>'
					);
					$("#numberlist").find("div[name='numbercard']").each(function () {
						$(this).unbind().click(function () {
							let index = $(this).attr("data-value");
							let idnumber = accountlist[index].ID_NUMBER;
							layer.confirm('确认登录账号[' + idnumber + ']？', {
								title: "登录确认",
								time: 0 //不自动关闭
								, btn: ['确认', '取消']
								, yes: function (index) {
									layer.close(index);
									loginBymobileOnChooseNumber(mobile, mobilecode, idnumber);
								}
							});
							return;
						})
					});
				}
				$(".scroll-list").mCustomScrollbar({
					axis: "y", // horizontal scrollbar
					alwaysShowScrollbar: 0,
					theme: "minimal-dark"
				});
				$("#closecardlist").click(function () {
					$("#accountForm").html("");
				});
				return false;
			}
			if (data.result == "false") {
				$('#errormsg').text(data.error);
				toAlertInfo();
			} else if (!Boolean(data.redirectUrl)) {
				window.location.href = "login";
			} else {
				//正常登录
				window.location.href = data.redirectUrl;
			}
		});
	});
}

function loginBymobileOnChooseNumber(mobile, mobilecode, account) {
	$.post("loginByMorE", {
		"method": "login",
		"mobile": mobile,
		"mobileCode": mobilecode,
		"random": Math.random(),
		"service": $.getUrlParam("service"),
		"account": account
	}, function (data) {
		if (data.result == "false") {
			$('#errormsg').text(data.error);
			toAlertInfo();
		} else if (!Boolean(data.redirectUrl)) {
			window.location.href = "login";
		} else {
			//正常登录
			window.location.href = data.redirectUrl;
		}
	});
}

function getParameter(hash,name,nvl) {
	if(!nvl){
		nvl = "";
	}
	var svalue = hash.match(new RegExp("[\?\&]?" + name + "=([^\&\#]*)(\&?)", "i"));
	if(svalue == null){
		return nvl;
	}else{
		svalue = svalue ? svalue[1] : svalue;
		svalue = svalue.replace(/<script>/gi,"").replace(/<\/script>/gi,"").replace(/<html>/gi,"").replace(/<\/html>/gi,"").replace(/alert/gi,"").replace(/<span>/gi,"").replace(/<\/span>/gi,"").replace(/<div>/gi,"").replace(/<\/div>/gi,"");
		return svalue;
	}
}


//设置cookie
function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}

//获取cookie
function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1);
      if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
  }
  return "";
}

//清除cookie  
function clearCookie(name) {  
  setCookie(name, "", -1);  
}

// 弹出提示信息
function toAlertInfo() {
	$("#errormsg").show();
}

function dglogintimer(intDiff){
	let showname = $('#getMobileVerifyCode').html();
	$("#getMobileVerifyCode").unbind("click");
	let second = intDiff;
	if(intDiff < 10){
		second = "0" + intDiff;
	}
	$('#getMobileVerifyCode').html("(" + second + ")");//60秒后重新获取
	intDiff--;
	logtimer=window.setInterval(function(){
		var second=0;//时间默认值
		if(intDiff > 0){
			second = Math.floor(intDiff);
		}
		if (second <= 9){
			second = '0' + second;
		}

		$('#getMobileVerifyCode').html("(" + second + ")");//'秒后重新获取'
		if(second == 0){
			window.clearInterval(logtimer);
			$('#getMobileVerifyCode').html(showname);
			//获取手机验证码
			$("#getMobileVerifyCode").unbind("click").bind("click", function () {
				if($(this).html().indexOf($("#getPhoneCodeText").text())===-1){
					return;
				}
				let mreg = /^0?1\d{10}$/;
				//需要填写手机号码才能发送验证码
				let mobile = $("#loginMobile").val();
				let sendConfirm = $("#sendConfirm").val();
				if($.trim(mobile) == ""||!mreg.test(mobile)){
					$("#errormsg").text("手机号格式错误");
					toAlertInfo();
					return false;
				}
				else if($.trim(sendConfirm) == ""){
					$('#errormsg').text("验证码不能为空");
					toAlertInfo();
					return false;
				}
				else{
					$.post("loginByMorE", {
						"method": "sendMobileCode",
						"sendConfirm": sendConfirm,
						"mobile": mobile,
						"random": Math.random()
					}, function (data) {
						if (data.result == "false") {
							$("#codeImage").trigger("click");
							$("#errormsg").text(data.error);
							$("#errormsg").css("width", "100%");
							toAlertInfo();
						} else {
							//先禁用按钮以避免连续重复提交
							$("#getMobileVerifyCode").attr("disabled", "disabled");
							const intDiff = parseInt(60);//倒计时总秒数量
							dglogintimer(intDiff);
						}
					});
				}
			});
			$("#getMobileVerifyCode").removeAttr("disabled");
		}
		intDiff--;
	}, 1000);
}

(function ($) {
	$.getUrlParam = function (name) {
		var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
		var r = window.location.search.substr(1).match(reg);
		if (r != null) return unescape(r[2]);
		return null;
	}
})(jQuery);