//Some client-side validation
$('#submitButton').click(function() {

	var valResults = []

	var langsCheck = validateNativeLangs();
	valResults.push(langsCheck);

	var forLangsCheck = validateForeignLangs();
	valResults.push(forLangsCheck);
	
	if (valResults.indexOf(false) === -1) {
		$('#form').submit();
	}
});

function validateNativeLangs() {
	var childDivs = $('#nativeLangWrapper').children('div');
	var isClean = true;
	for (var count = 0; count < childDivs.length; count++) {
		var div = $(childDivs[count]);
		if (div.is(':visible')) {
			var select = div.find("select");
			if (!select.val()) {
				div.find("li[class=errorMessage]").show();
				isClean = false;
			}
		}
	}

	return isClean;
}
