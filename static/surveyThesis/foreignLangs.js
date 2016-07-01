//this file must be loaded after radioButtonHideDiv
$(document).ready(function() {
	repopulateForeignLangs();
});

$('input[name=foreignLangBool]').on('change', function() {
	hideShowDiv('#foreignLanguageWrapper', 'foreignLangBool');
});

$('#addForLangButt').click(function() {
	addForeignLanguage();
});

$('#foreignLanguageWrapper').on('change', 'input[name^=school]', function() {
	var senderId = '#' + $(this).attr('id');
	var num = getFinalNumInString(senderId);
	hideShowDiv('#schoolTimeDiv' + num, 'school' + num);
});

$('#foreignLanguageWrapper').on('change', 'input[name^=lived]', function() {
	var senderId = '#' + $(this).attr('id');
	var num = getFinalNumInString(senderId);
	hideShowDiv('#livedTimeDiv' + num, 'lived' + num);
});

$('#foreignLanguageWrapper').on('change', 'input[name^=otherStudy]', function() {
	var senderId = '#' + $(this).attr('id');
	var num = getFinalNumInString(senderId);
	hideShowDiv('#otherStudyTimeDiv' + num, 'otherStudy' + num);
});

function addForeignLanguage() {
	var divBaseName = 'foreignLangDiv';
	var selectBaseName = 'foreignLangSelect';
	var oldNum = getLastIdNumLastElement('div', divBaseName);
	var num = parseInt(oldNum) + 1;

	var source = $('#' + divBaseName + '1');
	var $clone = source.clone().prop('id', divBaseName + num);

	//renumber items with numbered names or ids
	$clone = renumberElements($clone);
	//reset all inputs
	$clone = resetInputs($clone);

	//reset time labels to 0
	var labsToReset = ['semestersTotal', 'daysTotal'];
	for (var l = 0; l < labsToReset.length; l++) {
		$clone.find('span[name=' + labsToReset[l] + ']').each(function(ind, spanEl) {
			console.log(spanEl);
			$(spanEl).html('0');
		});
	}

	var elsToHide = ['.errorMessage', 
			'div[id^=schoolTimeDiv]', 
			'div[id^=livedTimeDiv]',
			'div[id^=otherStudyTimeDiv]'];
	for (var ec = 0; ec < elsToHide.length; ec++) {
		$clone.find(elsToHide[ec]).hide();
	}

	$clone.find('button').remove();

	var removeButtonText = $('#removeButtonText').val();
	var removeButton = '<button type="button" id="removeLangButton' 
		+ num + '" onclick="removeForeignLang(' + num + ')">' 
		+ removeButtonText + '</button>';
	$clone.append(removeButton);

	$clone.insertAfter('#' + divBaseName + oldNum);
}

function removeForeignLang(number) {
	var divToRemove = $('#foreignLangDiv' + number);
	divToRemove.remove();
	collectForeignLangSelection();
}

function renumberElements(clone) {
	var descElements = clone.find('*');

	for (var n = 0; n < descElements.length; n++) {
		var el = $(descElements[n]);

		var props = ['id', 'name', 'for'];
		for (var p = 0; p < props.length; p++) {

			var prop = props[p];
			var oldProp = el.prop(prop);

			if (oldProp) {
				var oldPropNum = getFinalNumInString(oldProp);
				
				if (oldPropNum) {
					//console.log("oldIdNum: " + oldIdNum);
					var propBase = oldProp.slice(0, -oldPropNum.toString().length);
					//console.log(propBase + ": " + idBase);
					el.prop(prop, propBase + parseInt(oldPropNum + 1, 10));
				}
			}
		}
	}

	return clone;
}

function repopulateForeignLangs() {
	console.log('since some of these are nested in dynamically generated objects, must update this');
	hideShowDiv('#schoolTimeDiv', 'school');
	hideShowDiv('#livedTimeDiv', 'lived');
	hideShowDiv('#otherStudyTimeDiv', 'otherStudy');
	hideShowDiv('#foreignLanguageWrapper', 'foreignLangBool');
}

function resetInputs(clone) {
	var els = clone.find('input');		

	for (var e = 0; e < els.length; e++) {
		var el = $(els[e]);
		var type = el.prop('type');
		switch (type) {
			case "checkbox":
				el.prop('checked', false);
			case "number":
				el.val('0');
			case "text":
				el.val("");
		}
		
	}

	return clone;
}

function collectForeignLangSelection() {
	var flangDivs = $('div[id^=foreignLangDiv]');
	
	var langList = [];
	for (var fd = 0; fd < flangDivs.length; fd++) {
		var flangDiv = flangDivs[fd];
		var langName = flangDiv.find('select[id^=foreignLangSelect]').val();
		var proficiency = flangDiv.find('select[id^=foreignProfSelect]').val();
		var school = flangDiv.find('input[id^=schoolCheckbox]').is(':checked');
		var schoolSemesters = calculateSemesters(flangDiv.find('div[id^=schoolTimeDiv]'));
		var livedAbroad = flangDiv.find('input[id^=livedCheckbox]').is(':checked');
		var livedAbroadDays = calculateDays(flangDiv.find('div[id^=livedTimeDiv]'));
		var other = flangDiv.find('input[id^=otherStudyCheckbox]').is(':checked');
		var otherDescription = flangDiv.find('input[id^=otherStudyDetails]').val();
		var otherDays = calculateDays(flangDiv.find('div[id^=livedTimeDiv]'));
	}

	return "hey";

};

function validateForeignLangs() {

	var flangString = collectForeignLangSelection();	
	
	return false;

};
