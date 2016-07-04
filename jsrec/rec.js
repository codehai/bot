the_log=[];
(function(){
	var types = [ 
		"mousedown", "mouseup", "click", "dblclick", "mousemove", "mouseover", "mouseout", "mousewheel",
		"keydown", "keyup", "keypress", "textInput",
		"touchstart", "touchmove", "touchend", "touchcancel",
		"resize", "scroll", "zoom", "focus", "blur", "select", "change", "submit", "reset",
		"load", "unload", "abort", "error", "search", "devicemotion", "deviceorientation",
		"DOMFocusIn", "DOMFocusOut", "DOMActivate",
		"DOMSubtreeModified",
		"DOMNodeInserted",
		"DOMNodeRemoved",
		"DOMNodeRemovedFromDocument",
		"DOMNodeInsertedIntoDocument",
		"DOMAttrModified",
		"DOMCharacterDataModified"
		];
	var f = function(e){
		the_log.push(e);
		//console.log(e);
	};
	var object = document;
	for (var i = 0; i < types.length; ++i) {
		//object.removeEventListener(types[i], f, false);
		object.addEventListener(types[i], f, false);
	}

	/*var add = function(element,eventName,callback){ };
	var before = null;
	var after = null;
	var aEL = HTMLElement.prototype.addEventListener;

	HTMLElement.prototype.addEventListener = function(eventName, callback) {
		add.apply(this, arguments);

		aEL.apply(this, [eventName, function() {
			if (before) {
				before.apply(this, arguments);
			}

			callback.apply(this, arguments);

			if (after) {
				after.apply(this, arguments);
			}
		}]);
	}*/

})();
