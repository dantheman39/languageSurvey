//right now works for checkboxes and radio buttons
//If checked/true, will show a div
function hideShowDiv(hideDivId, inputName) {
	var div = $(hideDivId);
	var input = $('input[name=' + inputName + ']');
	var inputType = input.attr('type');

	var conditional = false;
	if (inputType === 'radio') {
		conditional = input.filter(':checked').val() === "True";
	} else if (inputType === 'checkbox') {
		conditional = input.is(':checked') === true;
	}

	if (conditional === true) {
		div.show();
	} else {
		div.hide();
	}
}
