// Isto se complicou rápido. Ao refrescar e ao mandar,
// se chama collectForeignLangSelection(), que coleta os
// valores das entradas e salva num arranjo, que contém
// arranjos associativos. Ao disparar o evento 'pronto', se chama
// repopulateForeignLangs, que lê deste arranjo para 
// criar e preencher as entradas que se tinham criado
// dinamicamente antes de refrescar.


//this file must be loaded after radioButtonHideDiv
$(document).ready(function() {
	repopulateForeignLangs();
});

//catch page reload
$(window).unload(function() {
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
		var studyDiv = flangDiv.find('div[id^=schoolTimeDiv]');
		var livedDiv = flangDiv.find('div[id^=livedTimeDiv]');
		var otherStudyDiv = flangDiv.find('div[id^=otherStudyTimeDiv]');
		langDict = {
			langName: flangDiv.find('select[id^=foreignLangSelect]').val(),
			proficiency: flangDiv.find('select[id^=foreignProfSelect]').val(),
			school: flangDiv.find('input[id^=schoolCheckbox]').is(':checked'),
			schoolSemestersInput: studyDiv.find('input[name=semesters]').val(),
			schoolYearsInput: studyDiv.find('input[name=years]').val(),
			//total semesters
			schoolSemesters: calculateSemesters(flangDiv.find('div[id^=schoolTimeDiv]')),

			livedAbroad: flangDiv.find('input[id^=livedCheckbox]').is(':checked'),
			livedAbroadYearsInput: livedDiv.find('input[name=years]').val(),
			livedAbroadMonthsInput: livedDiv.find('input[name=months]').val(),
			livedAbroadWeeksInput: livedDiv.find('input[name=weeks]').val(),
			livedAbroadDaysInput: livedDiv.find('input[name=days]').val(),

			livedAbroadDays: calculateDays(flangDiv.find('div[id^=livedTimeDiv]')),

			other: flangDiv.find('input[id^=otherStudyCheckbox]').is(':checked'),
			otherDescription: flangDiv.find('input[id^=otherStudyDetails]').val(),
			otherDays: calculateDays(flangDiv.find('div[id^=otherStudyTimeDiv]')),

			otherYearsInput: otherStudyDiv.find('input[name=years]').val(),
			otherMonthsInput: otherStudyDiv.find('input[name=months]').val(),
			otherWeeksInput: otherStudyDiv.find('input[name=weeks]').val(),
			otherDaysInput: otherStudyDiv.find('input[name=days]').val(),
		}
		langsList.push(langDict);
		console.log(langsList);
	}
	var langsListStr = JSON.stringify(langsList);
	$('#id_foreignLanguages').val(langsListStr);
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
	console.log('in repopulate');
	var jsonString = $('#id_foreignLanguages').val();

	if (jsonString) {
		
		var langsArray = JSON.parse(jsonString);

		var numLangs = langsArray.length;

		//refill first div
	
		//create and fill divs
		if (numLangs > 1) {
			for (var nd = 0; nd < numLangs; nd++) {
				if (nd > 0) {
					var theDiv = addForeignLanguage();
				} else {
					var theDiv = $('#foreignLangDiv1');
				}
				var langObj = langsArray[nd];
				repopulateInputs(theDiv, langObj);
			}
		}
		
	}
	//unhide elements
	hideShowDiv('#foreignLanguageWrapper', 'foreignLangBool');

	var forDivs = $('div[id^=foreignLangDiv');	

	for (var dc = 0; dc < forDivs.length; dc++) {
		var forDiv = $(forDivs[dc]);

		var idsNames = [
			['schoolTimeDiv', 'school'],
			['livedTimeDiv', 'lived'],
			['otherStudyTimeDiv', 'otherStudy'],
		];

		for (var idN = 0; idN < idsNames.length; idN++) {
			var theId = forDiv.find('div[id^=' + idsNames[idN][0] + ']').prop('id');
			var theName = forDiv.find('input[name^=' + idsNames[idN][1] + ']').prop('name');
			hideShowDiv('#' + theId, theName);
		}
	}

}

function repopulateInputs(div, object) {
	div.find('select[id^=foreignLangSelect]').val(object.langName);
	div.find('select[id^=foreignProfSelect]').val(object.proficiency);
	div.find('input[id^=schoolCheckbox]').prop('checked', object.school);
	var studyDiv = div.find('div[id^=schoolTimeDiv]');
	var livedDiv = div.find('div[id^=livedTimeDiv]');
	var otherStudyDiv = div.find('div[id^=otherStudyTimeDiv]');

	studyDiv.find('input[name="years"]').val(object.schoolYearsInput);
	studyDiv.find('input[name="semesters"]').val(object.schoolSemestersInput);
	studyDiv.find('span[name=semestersTotal]').html(object.schoolSemesters);

	div.find('input[id^=livedCheckbox]').prop('checked', object.livedAbroad);
	livedDiv.find('input[name="years"]').val(object.livedAbroadYearsInput);
	livedDiv.find('input[name="months"]').val(object.livedAbroadMonthsInput);
	livedDiv.find('input[name="weeks"]').val(object.livedAbroadWeeksInput);
	livedDiv.find('input[name="days"]').val(object.livedAbroadDaysInput);
	livedDiv.find('span[name=daysTotal]').html(object.livedAbroadDays);

	div.find('input[id^=otherStudyCheckbox]').prop('checked', object.other);
	div.find('input[id^=otherStudyDetails]').val(object.otherStudyDetails);
	otherStudyDiv.find('input[name="years"]').val(object.otherYearsInput);
	otherStudyDiv.find('input[name="months"]').val(object.otherMonthsInput);
	otherStudyDiv.find('input[name="weeks"]').val(object.otherWeeksInput);
	otherStudyDiv.find('input[name="days"]').val(object.otherDaysInput);
	otherStudyDiv.find('span[name=daysTotal]').html(object.otherDays);
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
