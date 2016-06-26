$('#addNatLangButt').click(function () {
	addCountry();
});

function addCountry() {

	var divBaseName = 'natLangDiv';
	//console.log('addCountry() called');
	var oldNum = getLastIdNum('div', divBaseName);
	var num = parseInt(oldNum) + 1;

	var source = $('#' + divBaseName + '1');
	var $clone = source.clone().prop('id', divBaseName + num);
	$clone.find('select>option:eq(0)').prop('selected', true);
	$clone.find('button').remove();

	var removeButtonText = $('#removeButtonText').val();
	var removeButton = '<button type="button" id="removeLangButton' + num + '" onclick="removeLang">' + removeButtonText + '</button>';
	$clone.append(removeButton);

	$clone.insertAfter('#' + divBaseName + oldNum);


}

function getLastIdNum(element, idNoNum) {

	//console.log(element);
	//console.log(idNoNum);

	//The forward slashes start and end the javascript regexp
	//\d means digit, + means match preceding expression 1 or more times
	//g is a flag that means global search
	var $lastElement = $(element + '[id^=' + idNoNum + ']:last');
	var num = parseInt( $lastElement.prop('id').match(/\d+/g), 10  );
	return num

}
