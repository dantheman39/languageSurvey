$(document).ready( function() {
	hideShowDiv('#additionalHomeLangDetails', 'additionalHomeLang');
});

$('input[name=additionalHomeLang]').on('change', function() {
	hideShowDiv('#additionalHomeLangDetails', 'additionalHomeLang');
});
