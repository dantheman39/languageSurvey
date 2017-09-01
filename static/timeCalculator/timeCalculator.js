var timeCalculator = (function () {
	// originally written for days,
	// but can now be used for semesters

	var daysMap = {
		"Years": 365,
		"Months": 30,
		"Weeks": 7,
		"Days": 1
	};

	var semestersMap = {
		"Years": 2,
		"Semesters": 1
	};

	var parseListProp;
	var calculate;

	parseListProp = dynamicDr.parseDjangoProp;

	calculate = function(container, inputSelector, totalSelector, daysOrSemesters, totalIsSpan) {
		// daysOrSemesters will default to days if not given.
		container = $(container);
		var inputs = container.find(inputSelector);
		var numInputs = inputs.length;
		var i = 0;
		var input;
		var nameInfo;
		var totalDays = 0;
		var inputVal;
		var parseUnit;
		var map;

		if (totalIsSpan === undefined) {
			totalIsSpan = false;
		}
		if (typeof(totalIsSpan) !== "boolean") {
			throw "Argument totalIsSpan should be boolean";
		}

		parseUnit = function(str, map) {
			// for finding Years, Semesters, Days, etc. 
			var mapProps = Object.keys(map);
			var numProps = mapProps.length;
			var i;
			var mapProp;
			for (i = 0; i < numProps; i++) {
				mapProp = mapProps[i];
				if (str.includes(mapProp)) {
					return mapProp;
				}
			}

			// if we got this far, there was a mistake
			return null;
		};

		if (typeof daysOrSemesters === "undefined") {
			map = daysMap;
		} else {
			if (daysOrSemesters === "days") {
				map = daysMap;
			} else if (daysOrSemesters === "semesters") {
				map = semestersMap;
			} else {
				throw "Invalid argument for 'daysOrSemesters'";
			}
		}

		totalDisplay = container.find(totalSelector);
		
		for (i; i < numInputs; i++) {
			input = $(inputs[i]);
			inputVal = input.val();
			unit = parseUnit(input.prop("name"), map);
			if (unit === null) { 
				throw "The input for calculating days has an unexpected \"name\" structure"; 
			}

			totalDays += parseInt(inputVal, 10) * map[unit];
		}

		if (totalIsSpan) {
			totalDisplay.html(totalDays);
		} else {
			totalDisplay.val(totalDays);
		}

	};

	return {
		calculate: calculate,
	};

})();
