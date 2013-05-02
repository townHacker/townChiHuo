(function($) {
    $.fn.extend({
	figure_cut: function() {
	    var container = $(this);

	    var gen_slice = function() {
		var n_div = $('<div>');
		n_div.attr('style', 'width: 200px; height: 200px; position: absolute; top: 0px; left: 0px; z-index:9999;');
		n_div.addClass('ui-state-active');
		n_div.draggable({ containment: "parent" });
		n_div.resizable({ containment: "parent" });
		n_div.css({ opacity: .4 });
		container.css('position', 'relative');
		container.append(n_div);
	    }

	    var gen_original_img = function() {
		var img = $('<img id="figure_cut_original" style="max-width: none;">');

		var img_wrap = $('<div>');

		var callbackFunc = function() {
		    var img_w = parseFloat(img.css('width'));
		    var img_h = parseFloat(img.css('height'));
		    
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
		    img.draggable({ containment: "parent" });
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
	    }

	    _init();
	}
    });
})(jQuery);
