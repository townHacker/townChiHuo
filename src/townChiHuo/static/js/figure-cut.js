(function($) {
    $.fn.extend({
	figure_cut: function(option) {
	    option = $.extend({
		zoom_slider: '#figure_cut_slider',
		zoom_val: '#zoom_val', 
	    }, option);
	    var container = $(this);
	    var img_o_width, img_o_height;
	    var img_n_width, img_n_height;

	    var _offset = function() {
		var img_offset = $('#figure_cut_original').offset();
		var slice_offset = $('#figure_cut_slice').offset();
		offset_top = slice_offset.top - img_offset.top;
		offset_left = slice_offset.left - img_offset.left;
		container.attr('figure-top', offset_top);
		container.attr('figure-left', offset_left);
	    };

	    var zoom_img = function(zoom) {
		var img = $('#figure_cut_original');
		img_n_width = img_o_width * zoom;
		img_n_height = img_o_height * zoom;
		img.animate({
		    width: img_n_width,
		    height: img_n_height,
		}, 500, function() {

		    container.attr('figure-zoom', zoom);

		    var ctn_w = container.width();
		    var ctn_h = container.height();
		    var wrp_left = img_n_width <= ctn_w ?
			0 : img_n_width - ctn_w;
		    var wrp_top = img_n_height <= ctn_h ?
			0 : img_n_height - ctn_h;
		    
		    $('#figure_img_wrapper').css({
			'width': wrp_left * 2 + ctn_w,
			'height': wrp_top * 2 + ctn_h,
			'left': -wrp_left,
			'top': -wrp_top, 
		    });
		    $('#figure_cut_original').animate({
			'left': wrp_left,
			'top': wrp_top, 
		    }, 500, function() {
			_offset();
		    });

		});
	    };

	    var animate_timeout;
	    var zoom_animate = function(val) {
		clearTimeout(animate_timeout);
		animate_timeout = setTimeout(function() {
		    $(option.slider_val_show).html(val);
		    zoom_img(val);
		}, 150);
	    };

	    var gen_slider = function() {
			
		$(option.slider).slider({
		    min: 0,
		    max: 2000,
		    value: 1000,
		    slide: function(event, ui) {
			zoom_animate(ui.value / 1000.0);
		    }
		});

		$(option.slider_val_show).html(1);
	    };

	    var gen_slice = function() {
		var n_div = $('<div id="figure_cut_slice">');
		n_div.attr('style', 'width: 200px; height: 200px; position: absolute; top: 0px; left: 0px; z-index:9999;');
		n_div.addClass('ui-state-active');
		n_div.draggable({
		    containment: "parent",
		    stop: function() {
			_offset();
		    }, 
		});

		n_div.resizable({ containment: "parent" });
		n_div.resize(function() {
		    container.attr('cut_width', $(this).width());
		    container.attr('cut_height', $(this).height());
		});

		
		n_div.css({ opacity: .4 });
		container.css('position', 'relative');
		container.append(n_div);
	    }

	    var gen_original_img = function() {
		var img = $('<img id="figure_cut_original" style="max-width: none;">');

		var img_wrap = $('<div id="figure_img_wrapper">');

		var callbackFunc = function() {
		    var img_w = parseFloat(img.css('width'));
		    var img_h = parseFloat(img.css('height'));
		    img_o_width = img_w;
		    img_o_height = img_h;
		    
		    var ctn_w = parseFloat(container.css('width'));
		    var ctn_h = parseFloat(container.css('height'));
		    
		    var wrp_left = img_w <= ctn_w ? 0 : img_w - ctn_w;
		    var wrp_top = img_h <= ctn_h ? 0 : img_h - ctn_h;
		    
		    var wrp_w = wrp_left * 2 + ctn_w;
		    var wrp_h = wrp_top * 2 + ctn_h;

		    if (!img_w || !img_h)
			return;
		    
		    img_wrap.css({
			'width': wrp_w,
			'height': wrp_h,
			'position': 'absolute',
			'left': -wrp_left,
			'top': -wrp_top, 
		    });
		    
		    img.css({
			'position': 'absolute',
			'left': wrp_left,
			'top': wrp_top, 
		    });
		    img.draggable({
			containment: "parent",
			stop: function() {
			    _offset();
			}, 
		    });
		};

		img.one('load', function() {
		    callbackFunc();
		}).each(function() {
		    if (this.complete) {
			callbackFunc();
		    }
		});
		
		img_wrap.append(img);
		container.append(img_wrap);
		img.attr('src', container.attr('img-src'));
	    }

	    var _init = function() {
		container.empty();
		container.css({
		    width: 400,
		    height: 400,
		    border: '1px solid #CCC',
		    backgroundColor: '#EEEEEE', 
		    overflow: 'hidden',
		});

		gen_original_img();
		gen_slice();
		gen_slider();
	    }

	    _init();
	}
    });
})(jQuery);
