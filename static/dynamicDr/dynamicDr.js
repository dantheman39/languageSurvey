var dynamicDr = (function() {
	"use strict";

	//right now can be asp or djangoFormset
	var engine = "asp";
	var setEngine;

	var hideShowDiv;

	// for getting information about an id or name
	var parseDjangoProp;
	var parseListProp;
	var getLettersAndNumber;

	var renumberHtml;

	// creates object providing spec argument to 
	// renumber functions
	var renumArgsBase;
	var renumber;
	var renumberMultiple;
	// helper function called by the previous two
	// functions, will be kept private
	var renumberElements;
	var cloneAndRenumber;
	var removeDivAndRenumber;
	var addRemoveButtons;
	var resetValues;
	var resetMultipleValues;

	setEngine = function(engineName) {
		var acceptedEngines = ["asp", "djangoFormset"];
		if (engineName === undefined) {
			this.engine = "asp";
		} else if (acceptedEngines.indexOf(engineName) < 0) {
			throw "The engine '" + engineName + "' is not listed as a known web framework.";
		} else {
			this.engine = engineName;
		}
	};

	//right now works for checkboxes and radio buttons
	//If checked/true, will show a div
	hideShowDiv = function(hideDivId, inputName) {
		var div = $(hideDivId);
		var input = $('input[name=' + inputName + ']');
		var inputType = input.attr('type');
		var checkedVal;

		var conditional = false;
		if (inputType === 'radio') {
			checkedVal = input.filter(':checked').val();
			conditional = checkedVal === "true" || checkedVal === "True";
		} else if (inputType === 'checkbox') {
			conditional = input.is(':checked') === true;
		}

		if (conditional === true) {
			div.show();
		} else {
			div.hide();
		}
	};

	parseDjangoProp = function(prop) {
		var reg, match, nameInfo;
		reg = /(.+?)(\d+)(.+)/g;
		match =  reg.exec(prop);
		if (!match) {
			return null;
		} else {
			nameInfo = {
				"preNum": match[1],
				"num": match[2],
				"postNum": match[3],
				"getNewName": function (newNum) {
					if (newNum === undefined) {
						throw "getNewName: argument 'newNum' is undefined";
					}
					return this.preNum + newNum + this.postNum;
				}
			};
			return nameInfo;
		}
	};

	parseListProp = function(prop, specialCharsType) {

		// default specialCharsType is [].
		var numPre, numPost, reg, match, nameInfo;

		if (typeof specialCharsType === "undefined" || specialCharsType === "brackets") {
			numPre = "[";
			numPost = "].";
			reg = /(.+?)\[(\d+)\]\.(.+)/g;
		} else if (specialCharsType === "underscore") {
			numPre = "_";
			numPost = "__";
			reg = /(.+?)_(\d)__(.+)/g;
		}

		match = reg.exec(prop);
		if (!match) {
			return null;
		}

		else {
			nameInfo = {
				"listName": match[1],
				"index": parseInt(match[2], 10),
				"propertyName": match[3],
				"numPre": numPre,
				"numPost": numPost,
				"getNewName": function (newNum) {
					if (typeof newNum === "undefined") { 
						throw "getNewName: argument 'newNum' is undefined";
					}
					return this.listName + this.numPre + newNum + this.numPost + this.propertyName;
				}
			};
			return nameInfo;
		}
	};

	getLettersAndNumber = function(s) {
		// For strings that have letters followed
		// by numbers, like "element22"
		var reg = /(.+?)(\d+)/g;
		var match = reg.exec(s);
		var nameInfo;
		if (!match) {
			return null;
		} else {
			nameInfo = {
				"name": match[1],
				"number": match[2]
			};
			return nameInfo;
		}
	};

	// Note: added this a bit ad hoc,
	// assumes a simple string with text 
	// and a single integer, like "Test 1" 
	renumberHtml = function(selector) {
		var elements = $(selector);
		var numElements = elements.length;
		var i = 0;
		var el;
		var origHtml;
		var matchObj;
		var newHtml;
		for (i; i < numElements; i++) {
			el = $(elements[i]);
			origHtml = el.html();
			matchObj = getLettersAndNumber(origHtml);
			if (matchObj !== null) {
				newHtml = matchObj.name + (parseInt(i) + 1);
				el.html(newHtml);
			}
		}
	};

	renumArgsBase = function (argsArray) {

		var setProp = function(prop) {
			return function(val) {
				this[prop] = val;
			};
		};

		var numArgs = argsArray.length;
		var i = 0;
		var argsObj;
		for (i; i < numArgs; i++) {
			argsObj = argsArray[i];
			// Give these objects a couple methods to 
			// set their private values
			argsObj.setContainer = setProp("container");
			argsObj.setNewNum = setProp("newNum");
		}

		//args arrays is an array of objects with properties
		// for the renumberElements function: 
		return {
			getArgs: function() { return argsArray; },
			length: function() { return argsArray.length; }
		};
	};

	renumber = function(container, newNum, renumSpecObj) {
		var argsObjects = renumSpecObj.getArgs();
		var numObjects = renumSpecObj.length();
		var i, obj;

		for (i = 0; i < numObjects; i++) {
			obj = argsObjects[i];
			obj.setContainer(container);
			obj.setNewNum(newNum);
			renumberElements.apply(this, [obj]);
		}
	};

	renumberMultiple = function(containers, renumSpecObj) {
		var argsObjects = renumSpecObj.getArgs();
		var numObjects = renumSpecObj.length();

		var containerCount = containers.length;
		var cc, container, i, obj;
		for (cc = 0; cc < containerCount; cc++) {
			container = $(containers[cc]);
			for (i = 0; i < numObjects; i++) {
				obj = argsObjects[i];
				obj.setContainer(container);
				obj.setNewNum(cc);
				renumberElements.apply(this, [obj]);
			}
		}
	};

	renumberElements = function(spec) {
		// container is a jQuery element (or selector)
		// selector is to find the target elements in the container
		// propToChange: value should be "id", "name", or "for".
		//		This is because for names [0]. is used, but ids _0__
		// propOrData: optional. For deciding if we want to call element.prop()
		//		or element.data(). If "data", then the value of propToChange
		//		is whatever data value that must be changed.
		// addBack: optional. If true the container is included in elements to
		// 		be changed

		// These are all properties of the "spec" object.
		var container = spec.container, 
			selector = spec.selector, 
			newNum = spec.newNum, 
			propToChange = spec.propToChange, 
			propOrData = spec.propOrData, 
			addBack = spec.addBack;

		var targetElements,	acceptedPropOrData, acceptedEngines,
			specialCharType, targetLen, i, el, propVal, nameInfo;

		//allows for jQuery object or selector
		container = $(container); 
		if (addBack) {
			targetElements = container.find(selector).addBack(selector);
		} else {
			targetElements = container.find(selector);
		}

		if (container.length === 0) { 
			throw "Object " + container + " not found or empty"; 
		}

		if (targetElements.length === 0) { 
			console.log("Objects for selector '" + selector + "' not found or empty"); 
			return container;
		}
		
		acceptedPropOrData = ["prop", "data"];
		if (!propOrData) {
			// default is "prop"
			propOrData = "prop";
		} else if (acceptedPropOrData.indexOf(propOrData) === -1) { 
			throw "Invalid value for 'propOrData";
		}
		
		specialCharType = "brackets";

		if (propOrData === "prop") {
			if (propToChange === "id" || propToChange === "for") {
				specialCharType = "underscore";
			}
		}


		targetLen = targetElements.length;
		for (i = 0; i < targetLen; i++) {
			el = $(targetElements[i]);
			propVal = el[propOrData](propToChange);

			if ((typeof propVal === "undefined") || (propVal === "")) {
				//console.log("Warning: the selected element does not have the property");
			} else {

				if (this.engine === "asp") {
					// First assume string is in MVC list format (List[0].Property)
					nameInfo = parseListProp(propVal, specialCharType);
					if (nameInfo) {
						el[propOrData](propToChange, nameInfo.getNewName(newNum));
					} else {
						// Then try for a numbered name (name0)
						nameInfo = getLettersAndNumber(propVal);
						if (nameInfo) {
							el[propOrData](propToChange, nameInfo.name + newNum);
						}
						// If still doesn't match, just leave it alone
					}
				} else if (this.engine === "djangoFormset") {
					nameInfo = parseDjangoProp(propVal);
					if (nameInfo) {
						el[propOrData](propToChange, nameInfo.getNewName(newNum));
					} else {
						nameInfo = getLettersAndNumber(propVal);
						if (nameInfo) {
							el[propOrData](propToChange, nameInfo.name + newNum);
						}
					}
				}
			}
		}

		return container;
	};

	cloneAndRenumber = function(divBaseName, appendToSelector, classOfDiv, classOfRemoveButton, renumSpecObj) {
		// note that for djangoFormset, classOfDiv should also be the name of the
		// formset prefex (as in "id_classOfDiv-0-DELETE")
		var sourceId = "#" + divBaseName + "0";
		var source = $(sourceId);
		var clone = source.clone();
		var newNum = $("." + classOfDiv).length;
		renumber.apply(this,[clone, newNum, renumSpecObj]);
		$(appendToSelector).append(clone);
		if (this.engine === "djangoFormset") {
			document.getElementById("id_" + classOfDiv + "-TOTAL_FORMS").value = parseInt(newNum) + 1;
		}

		return clone;
	}; 
	
	/*
	cloneAndRenumber = function(divBaseName, appendToSelector, classOfDiv, classOfRemoveButton, renumSpecObj) {
		var sourceId = "#" + divBaseName + "0";
		var source = $(sourceId);

		var clone = source.clone();
		
		var newNum = $("." + classOfDiv).length;

		renumber(clone, newNum, renumSpecObj);

		var numRmBttns = clone.find("." + classOfRemoveButton).length;
		if (numRmBttns === 0) {
			clone.append('<button class="' + classOfRemoveButton + '" type="button">Remove</button>');
		}
		$(appendToSelector).append(clone);

		return clone;
	};
	*/


	removeDivAndRenumber = function(button, divsSelector, renumSpecObj) {
		button = $(button);
		button.parent().remove();

		var targetDivs = $(divsSelector);
		var numDivs = targetDivs.length;
		if (numDivs === 0) {
			throw "No objects found for selector: " + divsSelector;
		}
		
		renumberMultiple(targetDivs, renumSpecObj);
	};


	addRemoveButtons = function(selector, klass, addToFirst) {
		// when reloading the page, add
		// delete buttons next to dynamically
		// added languages
		var startIndex;
		if (addToFirst === false || typeof(addToFirst) !== "boolean") {
			// default
			startIndex = 1; 
		} else {
			startIndex = 0;
		}

		var divs = $(selector);
		$.each(divs, function (ind, div) {
			var butts;
			// don't add to first language
			if (ind >= startIndex) {
				//make sure doesn't exist
				butts = $(div).find("." + klass);
				if (butts.length === 0) {
					$(div).append('<button class="' + klass + '" type="button">Remove</button>');
				}
			}
		});
	};

	resetValues = function(spec, container) {
		// assumes all object selected are of 
		// the same input type (i.e. checkbox)
		var selector = spec.selector;
		var newVal = spec.newVal;
		var optionSelector = spec.optionSelector;
		var newValDefined = newVal !== undefined;
		var inputs;
		var numIns;
		var i = 0;
		var input;
		var inType;
		var optionObj;

		if (container !== undefined) {
			container = $(container);
			if (container.length === 0) {
				console.log("Container selector \"" + containerSel + "\" returned no objects");
				return;
			}
			inputs = container.find(selector);
		} else {
			inputs = $(selector);

		}
		numIns = inputs.length;

		if (inputs.length > 0) {
			inType = $(inputs.first()).prop("type");
			if (inType === "checkbox") {
				if (!newValDefined) {
					newVal = false;
				}
				inputs.prop("checked", newVal);
			} else if (inType === "text" || inType === "textarea" || inType === "hidden" || inType === "number") {
				if (!newValDefined) {
					newVal = "";
				}
				inputs.val(newVal);
			} else if (inType === "radio") {
				if (!newValDefined) {
					newVal = false;
				}
				inputs.prop("checked", newVal);
			} else if (inType === "select-one") {
				if (optionSelector !== undefined) {
					optionObj = inputs.find(optionSelector);
					optionObj.prop("selected", true);
				} else {
					inputs.prop("selectedIndex", 0);
				}
			}
		} else {
			console.log("Selector \"" + "\" returned no objects");
		}
	};

	resetMultipleValues = function(specs, container) {
		var numSpecs = specs.length;
		var i = 0;
		var spec;
		for (i; i < numSpecs; i++) {
			spec = specs[i];
			resetValues(spec, container);
		}
	};

	return { hideShowDiv: hideShowDiv,
		setEngine: setEngine,
		parseDjangoProp: parseDjangoProp,
		parseListProp: parseListProp,
		getLettersAndNumber: getLettersAndNumber,
		renumberHtml: renumberHtml,
		renumArgsBase: renumArgsBase,
		renumber: renumber,
		renumberMultiple: renumberMultiple,
		cloneAndRenumber: cloneAndRenumber,
		removeDivAndRenumber: removeDivAndRenumber,
		addRemoveButtons: addRemoveButtons,
		resetValues: resetValues,
		resetMultipleValues: resetMultipleValues,
	};

})();
