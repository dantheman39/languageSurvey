$('input[name=visionProblems]').on('change', function() {
	hideShowDiv('#visionProblemsDetails', 'visionProblems');
});

$('input[name=readingProblems]').on('change', function() {
	hideShowDiv('#readingProblemsDetails', 'readingProblems');
});

$('input[name=foreignLangBool]').on('change', function() {
	hideShowDiv('#foreignLanguageWrapper', 'foreignLangBool');
});

function hideShowDiv(hideDivId, radioButtonName) {
	var div = $(hideDivId);
	if ($('input[name=' + radioButtonName + ']:checked').val() === "True") {
		div.show();
	} else {
		div.hide();
	}
}

function cbHideShowDiv(hideDivId, checkboxName) {
	var div = $(hideDivId);
	if ($('input[name=' + checkboxName + ']').is(':checked') === true) {
		div.show();
	} else {
		div.hide();
	}
}
