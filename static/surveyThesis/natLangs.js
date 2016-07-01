//for whatever reason, this option uses a delegate,
//and will work with dynamically created elements
$('#nativeLangWrapper').on('change', 'select', function() {
	updateLanguageSelection();
	//console.log( $(this).attr('id') );
}); 

$('#addNatLangButt').click(function () {
	addLanguage();
});

$(document).ready(function() {
	repopulateLangs();
});

function addLanguage() {

	var divBaseName = 'natLangDiv';
	var selectBaseName = 'natLangSelect';
	//console.log('addCountry() called');
	var oldNum = getLastIdNumLastElement('div', divBaseName);
	var num = parseInt(oldNum) + 1;

	var source = $('#' + divBaseName + '1');
	var $clone = source.clone().prop('id', divBaseName + num);
	$clone.find('select>option:eq(0)').attr('selected', true);
	$clone.find('select').attr('id', selectBaseName + num);
	$clone.find('button').remove();

	var removeButtonText = $('#removeButtonText').val();
	var removeButton = '<button type="button" id="removeLangButton' 
		+ num + '" onclick="removeLang(' + num + ')">' 
		+ removeButtonText + '</button>';
	$clone.append(removeButton);

	$clone.insertAfter('#' + divBaseName + oldNum);
}

function removeLang(number) {
	var divToRemove = $('#natLangDiv' + number);
	divToRemove.remove();
	updateLanguageSelection();
}

function repopulateLangs() {
	var langsSelected = $('#id_nativeLanguages').val().split(',');
	if (langsSelected.length > 1) {
		for (var e = 1; e < langsSelected.length; e++) {
			addCountry();
			var selectSelector = '#natLangSelect' + parseInt(e + 1);
			$('#natLangSelect' + parseInt(e + 1)).val(langsSelected[e]);
		}
	}

}

function updateLanguageSelection() {
	var langDivs = $('#nativeLangWrapper').find('div[id^=natLangDiv]');
	var selectedLangs = [];
	for (var dc = 0 ; dc < langDivs.length; dc++) {
		var langDiv = $(langDivs[dc]);
		var selectedVal = langDiv.find('select').val();
		if ( $.inArray(selectedVal, selectedLangs) === -1) {
			selectedLangs.push(selectedVal);
		}
	}

	var selectedLangsStr = selectedLangs.join(",");
	$('#id_nativeLanguages').val(selectedLangsStr);
	//console.log( $('#id_nativeLanguages').val() );
}
