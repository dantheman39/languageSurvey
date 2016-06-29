//this file must be loaded after radioButtonHideDiv
$(document).ready(function() {
	repopulateForeignLangs();
});

$('#addForLangButt').click(function() {
	addForeignLanguage();
});

$('input[name=school]').on('change', function() {
	cbHideShowDiv('#schoolTimeDiv', 'school');
});

$('input[name=lived]').on('change', function() {
	cbHideShowDiv('#livedTimeDiv', 'lived');
});

function addForeignLanguage() {
	var divBaseName = 'foreignLangDiv';
	var selectBaseName = 'foreignLangSelect';
	var oldNum = getLastIdNum('div', divBaseName);
	var num = parseInt(oldNum) + 1;

	var source = $('#' + divBaseName + '1');
	var $clone = source.clone().prop('id', divBaseName + num);
	$clone.find('select>option:eq(0)').attr('selected', true);
	$clone.find('select').attr('id', selectBaseName + num);
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
	updateForeignLangSelection();
}

function repopulateForeignLangs() {
	cbHideShowDiv('#schoolTimeDiv', 'school');
	cbHideShowDiv('#livedTimeDiv', 'lived');
	hideShowDiv('#foreignLanguageWrapper', 'foreignLangBool');
}

function updateForeignLangSelection() {console.log("updateForeignLangSelection empty");};
