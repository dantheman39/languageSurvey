$('input[name=visionProblems]').on('change', function() {
	hideShowTextArea('#visionProblemsDetails', 'visionProblems');
});

$('input[name=readingProblems]').on('change', function() {
	hideShowTextArea('#readingProblemsDetails', 'readingProblems');
});

function hideShowTextArea(hideDivId, radioButtonName) {
	var div = $(hideDivId);
	if ($('input[name=' + radioButtonName + ']:checked').val() === "True") {
		div.show();
	} else {
		div.hide();
	}
}
