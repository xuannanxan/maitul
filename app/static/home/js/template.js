/* Theme Name:iDea - Clean & Powerful Bootstrap Theme
 * Author:HtmlCoder
 * Author URI:http://www.htmlcoder.me
 * Author e-mail:htmlcoder.me@gmail.com
 * Version:1.0.0
 * Created:October 2014
 * License URI:http://wrapbootstrap.com
 * File Description: Initializations of plugins 
 */

(function($){
	$(document).ready(function(){
		// Magnific popup
		//-----------------------------------------------
		if (($(".popup-img").length > 0) || ($(".popup-iframe").length > 0) || ($(".popup-img-single").length > 0)) {
			$(".popup-img").magnificPopup({
				type:"image",
				gallery: {
					enabled: true,
				}
			});
			$(".popup-img-single").magnificPopup({
				type:"image",
				gallery: {
					enabled: false,
				}
			});
			$('.popup-iframe').magnificPopup({
				disableOn: 700,
				type: 'iframe',
				preloader: false,
				fixedContentPos: false
			});
		};
		//Show dropdown on hover only for desktop devices
		//-----------------------------------------------
		var delay=0, setTimeoutConst;

		//Owl carousel
		//-----------------------------------------------
		if ($('.owl-carousel').length>0) {
			$(".owl-carousel.carousel").owlCarousel({
				responsive:{
					0:{
						items:1
					},
					600:{
						items:2
					},
					1000:{
						items:4
					}
				},
				loop:true,
				margin:10,
				nav: true,
				navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
				dots: false,
				smartSpeed: 1000
			});
			$(".owl-carousel.carousel-autoplay").owlCarousel({
				items: 4,
				autoPlay: 5000,
				pagination: false,
				navigation: true,
				navigationText: false
			});
			$(".owl-carousel.clients").owlCarousel({
				responsive:{
					0:{
						items:3
					},
					600:{
						items:4
					},
					1000:{
						items:6
					}
				},
				loop: true,
				nav: false,
				dots: false,
				smartSpeed: 1000,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true
			});
			$(".owl-carousel.content-slider").owlCarousel({
				items:1,
				loop: true,
				nav: false,
				dots: false,
				smartSpeed: 1000,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true
			});
			$(".owl-carousel.content-slider-with-controls").owlCarousel({
				items:1,
				loop: true,
				nav: true,
				navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
				dots: true,
				smartSpeed: 1000,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true
			});
			$(".owl-carousel.content-slider-with-controls-autoplay").owlCarousel({
				singleItem: true,
				autoPlay: 5000,
				navigation: true,
				navigationText: false,
				pagination: true
			});
			$(".owl-carousel.content-slider-with-controls-bottom").owlCarousel({
				singleItem: true,
				autoPlay: false,
				navigation: true,
				navigationText: false,
				pagination: true
			});
			$(".owl-carousel.home-slider-carousel ").owlCarousel({
				items: 1,
				loop: true,
				nav: true,
				navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
				dots: true,
				smartSpeed: 1000,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true
			});
		};
		//Show dropdown on hover only for desktop devices
		//-----------------------------------------------
		var delay=0, setTimeoutConst;
		if (Modernizr.mq('only all and (min-width: 768px)') && !Modernizr.touch) {
			$('.main-navigation .navbar-nav>li.dropdown, .main-navigation li.dropdown>ul>li.dropdown').hover(
			function(){
				var $this = $(this);
				setTimeoutConst = setTimeout(function(){
					$this.addClass('open').slideDown();
					$this.find('.dropdown-toggle').addClass('disabled');
				}, delay);

			},	function(){
				clearTimeout(setTimeoutConst );
				$(this).removeClass('open');
				$(this).find('.dropdown-toggle').removeClass('disabled');
			});
		};

		//Show dropdown on click only for mobile devices
		//-----------------------------------------------
		if (Modernizr.mq('only all and (max-width: 767px)') || Modernizr.touch) {
			$('.main-navigation [data-toggle=dropdown], .header-top [data-toggle=dropdown]').on('click', function(event) {
			// Avoid following the href location when clicking
			event.preventDefault();
			// Avoid having the menu to close when clicking
			event.stopPropagation();
			// close all the siblings
			$(this).parent().siblings().removeClass('open');
			// close all the submenus of siblings
			$(this).parent().siblings().find('[data-toggle=dropdown]').parent().removeClass('open');
			// opening the one you clicked on
			$(this).parent().toggleClass('open');
			});
		};
		// Fixed header
		//-----------------------------------------------
		var	headerTopHeight = $(".header-top").outerHeight(),
		headerHeight = $("header.header.fixed").outerHeight();
		$(window).scroll(function() {
			if (($(".header.fixed").length > 0)) {
				if(($(this).scrollTop() > headerTopHeight+headerHeight) && ($(window).width() > 767)) {
					$("body").addClass("fixed-header-on");
					$(".header.fixed").addClass('animated object-visible fadeInDown');
					if ($(".banner:not(.header-top)").length>0) {
						$(".banner").css("marginTop", (headerHeight)+"px");
					} else if ($(".page-intro").length>0) {
						$(".page-intro").css("marginTop", (headerHeight)+"px");
					} else if ($(".page-top").length>0) {
						$(".page-top").css("marginTop", (headerHeight)+"px");
					} else {
						$("section.main-container").css("marginTop", (headerHeight/10)+"px");
					}
				} else {
					$("body").removeClass("fixed-header-on");
					$("section.main-container").css("marginTop", (0)+"px");
					$(".banner").css("marginTop", (0)+"px");
					$(".page-intro").css("marginTop", (0)+"px");
					$(".page-top").css("marginTop", (0)+"px");
					$(".header.fixed").removeClass('animated object-visible fadeInDown');
				}
			};
		});
				//Scroll Spy
		//-----------------------------------------------
		if($(".scrollspy").length>0) {
			$("body").addClass("scroll-spy");
			if($(".fixed.header").length>0) {
				$('body').scrollspy({
					target: '.scrollspy',
					offset: 85
				});
			} else {
				$('body').scrollspy({
					target: '.scrollspy',
					offset: 20
				});
			}
		}

		//Scroll totop
		//-----------------------------------------------
		$(window).scroll(function() {
			if($(this).scrollTop() != 0) {
				$(".scrollToTop").fadeIn();
			} else {
				$(".scrollToTop").fadeOut();
			}
		});

		$(".scrollToTop").click(function() {
			$("body,html").animate({scrollTop:0},800);
		});

	}); // End document ready

})(this.jQuery);

function sendMessage(obj,form) {
    //禁用提交按钮，避免重复提交
    obj.disabled = true;
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: '/message',//url
        data: $('#'+form).serialize(),
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
                setTimeout(function () {
                    window.location.reload();
                }, 3000);
            } else {
                toastr.error(result.msg);
                obj.disabled = false;
            }
            ;
        },
        error: function () {
            toastr.error("System error, message submitted failure, please call our phone.");
        }
    });

}
function initSelectBar(obj) {
	 var selectBar = $("#"+obj+" li a")
        //为filter下的所有a标签添加单击事件
       selectBar.click(function () {
		   if ($(this).hasClass( "selected")){
			   $(this).removeClass("selected");
		   }else {
			    $(this).parent().parent().children('li').each(function () {
					$('a',this).removeClass("selected");
				});
				$(this).attr("class", "selected");
		   }


		   var result = RetSelecteds(obj)
		   var url = window.location.pathname+"?"
		   for (var index in result){
				url = url+'&'+index+'='+result[index];
			};
			window.location.href = url
             //返回选中结果   弹出
        });

    };

    function RetSelecteds(obj) {
        var result = {};
        $("#"+obj+" a[class='selected']").each(function () {
			if($(this).attr('data-index')){
				 result[$(this).attr('data-index')]=$(this).attr('data-val');
			}
        });
		console.log(result)
        return result;
    }

	function enterSearch(obj,url=window.location.pathname){
		$(obj).keypress(function (e) {
						if (e.which == 13) {
							window.location.href = url+"?search="+$(this).val()
						}
		});
	}
	function btnSearch(obj,url=window.location.pathname){
		window.location.href = url+"?search="+$(obj).prev().val()
	}
　　function GetUrlRelativePath()
　　{
　　　　var url = document.location.toString();
　　　　var arrUrl = url.split("//");

　　　　var start = arrUrl[1].indexOf("/");
　　　　var relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符

　　　　if(relUrl.indexOf("?") != -1){
　　　　　　relUrl = relUrl.split("?")[0];
　　　　}
　　　　return relUrl;
　　}
	function click_count(){
		 $.get('/click_count?url='+GetUrlRelativePath());
	}
//用户登录
function user_login() {
    //禁用提交按钮，避免重复提交
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: '/user_login',//url
        data: $('#user_login').serialize(),
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
                setTimeout(function () {
                    window.location.reload();
                }, 3000);
            } else {
                toastr.error(result.msg);
            }
            ;
        },
        error: function () {
            toastr.error("System error!!");
        }
    });

}

function getColor(){
	colors = ['#660099','#096000','#0021CC','#ff9933','#cc0033','#7e0023','#999', '#00a5bb','#38c7f4','#003366', '#006699', '#4cabce', '#e5323e']
	var x = colors.length-1;
    var y = 0;
	var rand = parseInt(Math.random() * (x - y + 1) + y);
	return colors[rand]
}