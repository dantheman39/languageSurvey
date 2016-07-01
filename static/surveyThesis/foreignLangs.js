//this file must be loaded after radioButtonHideDiv
$(document).ready(function() {
	repopulateForeignLangs();
});

//catch page reload
$('body').bind('beforeunload', function() {
	console.log('unloading');
	collectForeignLangSelection();
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

	var source = $('#' + divBaseName + oldNum);
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
	return $clone;
}

function collectForeignLangSelection() {
	var flangDivs = $('div[id^=foreignLangDiv]');
	
	var langsList = [];
	for (var fd = 0; fd < flangDivs.length; fd++) {
		var flangDiv = $(flangDivs[fd]);
		langDict = {
			langName: flangDiv.find('select[id^=foreignLangSelect]').val(),
			proficiency: flangDiv.find('select[id^=foreignProfSelect]').val(),
			school: flangDiv.find('input[id^=schoolCheckbox]').is(':checked'),
			schoolSemesters: calculateSemesters(flangDiv.find('div[id^=schoolTimeDiv]')),
			livedAbroad: flangDiv.find('input[id^=livedCheckbox]').is(':checked'),
			livedAbroadDays: calculateDays(flangDiv.find('div[id^=livedTimeDiv]')),
			other: flangDiv.find('input[id^=otherStudyCheckbox]').is(':checked'),
			otherDescription: flangDiv.find('input[id^=otherStudyDetails]').val(),
			otherDays: calculateDays(flangDiv.find('div[id^=otherStudyTimeDiv]'))
		}
		langsList.push(langDict);
	}
	var langsListStr = JSON.stringify(langsList);
	$('#id_foreignLanguages').val(langsListStr);
	return langsListStr;
};

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
	var jsonString = $('#id_foreignLanguages').val();

	if (jsonString) {
		
		var langsArray = JSON.parse(jsonString);

		var numLangs = langsArray.length;

		//refill first div
	
		//create and fill divs
		if (numLangs > 1) {
			for (var nd = 1; nd < numLangs; nd++) {
				var newDiv = addForeignLanguage();
				var langObj = langsArray[nd];
				repopulateInputs(newDiv, langObj);
			}
		}
		
	}

	hideShowDiv('#foreignLanguageWrapper', 'foreignLangBool');

	console.log('since some of these are nested in dynamically generated objects, must update this');
}

function repopulateInputs(div, object) {
			flangDiv.find('select[id^=foreignLangSelect]').val(object.langName);
			flangDiv.find('select[id^=foreignProfSelect]').val(object.proficiency);
			//school: flangDiv.find('input[id^=schoolCheckbox]').is(':checked'),
			//schoolSemesters: calculateSemesters(flangDiv.find('div[id^=schoolTimeDiv]')),
			//livedAbroad: flangDiv.find('input[id^=livedCheckbox]').is(':checked'),
			//livedAbroadDays: calculateDays(flangDiv.find('div[id^=livedTimeDiv]')),
			//other: flangDiv.find('input[id^=otherStudyCheckbox]').is(':checked'),
			//otherDescription: flangDiv.find('input[id^=otherStudyDetails]').val(),
			//otherDays: calculateDays(flangDiv.find('div[id^=otherStudyTimeDiv]'))

}

function resetInputs(clone) {
	var els = clone.find('input');		

	for (var e = 0; e < els.length; e++) {
		var el = $(els[e]);
		var type = el.prop('type');
		if (type === "checkbox") { 
				el.prop('checked', false);
		} else if (type === "number") {
				el.val('0');
		} else if (type === "text") {
				el.val("");
		}
	}

	return clone;
}

function validateForeignLangs() {

	var flangString = collectForeignLangSelection();	
	console.log(flangString);
	
	return false;

};
