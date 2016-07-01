$(document).ready(function() {
	repopulateDifficulties();
});

$('input[name=visionProblems]').on('change', function() {
	hideShowDiv('#visionProblemsDetails', 'visionProblems');
});

$('input[name=readingProblems]').on('change', function() {
	hideShowDiv('#readingProblemsDetails', 'readingProblems');
});

function repopulateDifficulties() {
	hideShowDiv('#visionProblemsDetails', 'visionProblems');
	hideShowDiv('#readingProblemsDetails', 'readingProblems');
}
