
  function phoneSlide(){
  	$('.phone').on('click', function(){
  		$('.phones').slideToggle(500);
  	});
  }

  function asideToggle(){
  	$('.aside-toggle button').on('click', function(evt){
  	    evt.preventDefault();
  		$('aside').slideToggle(300);
  		$(this).toggleClass('shutdown');
  	});
  }

  function filterToggle(){
  	$('.filter-toggle button').on('click', function(evt){
  	    evt.preventDefault();
  		$('.filters').slideToggle(300);
  		$(this).toggleClass('shutdown');
  	});
  }


  function imageChangeAttr(){
  	$('#thumbs').on('click', 'img', function(){
          $('#largeImage').attr('src',$(this).attr('src'));
          $('[data-fancybox]').attr('href',$(this).attr('src'));
      }); 
  }

  function fancyBoxInit(){
      $('[data-fancybox]').fancybox({
        fullScreen: false,
        frameWidth: 800,
        frameHeight: 600,
        closeBtn: true,
        image: {
            protect: true
        }
      });
  }

  // Carousel
  function carouselInit() {
        $(document).on('click', ".carousel-button-right",function(){
            var carusel = $(this).parents('.carousel');
            right_carusel(carusel);
            return false;
        });
        $(document).on('click',".carousel-button-left",function(){
            var carusel = $(this).parents('.carousel');
            left_carusel(carusel);
            return false;
        });
    function left_carusel(carusel){
       var block_width = $(carusel).find('.carousel-block').outerWidth();
           $(carusel).find(".carousel-items .carousel-block").eq(-1).clone().prependTo($(carusel).find(".carousel-items"));
           $(carusel).find(".carousel-items").css({"left":"-"+block_width+"px"});
           $(carusel).find(".carousel-items .carousel-block").eq(-1).remove();
           $(carusel).find(".carousel-items").animate({left: "0px"}, 200);
        }
    function right_carusel(carusel){
       var block_width = $(carusel).find('.carousel-block').outerWidth();
           $(carusel).find(".carousel-items").animate({left: "-"+ block_width +"px"}, 200, function(){
           $(carusel).find(".carousel-items .carousel-block").eq(0).clone().appendTo($(carusel).find(".carousel-items"));
           $(carusel).find(".carousel-items .carousel-block").eq(0).remove();
           $(carusel).find(".carousel-items").css({"left":"0px"});
         });
      }

    $(function() {
        auto_right('.carousel:first');
    });

    function auto_right(carusel){
        setInterval(function(){
            if (!$(carusel).is('.hover'))
                right_carusel(carusel);
        }, 3000)}
    // Навели курсор на карусель (прокрутка зупиняється)
        $(document).on('mouseenter', '.carousel', function(){$(this).addClass('hover')});
    //Забрали курсор з каруселі
        $(document).on('mouseleave', '.carousel', function(){$(this).removeClass('hover')});
    }



$(document).ready(function(){
    phoneSlide();
    asideToggle();
    filterToggle();
    imageChangeAttr();
    fancyBoxInit();
    carouselInit();

});