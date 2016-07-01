$('#foreignLanguageWrapper').on('change', '.studyTime', function() {
	var parentDiv = $(this).closest('div');
	calculateSemesters(parentDiv);
}); 

$('#foreignLanguageWrapper').on('change', '.timeInput', function() {
	var parentDiv = $(this).closest('div');
	calculateDays(parentDiv);
});

function calculateSemesters(parentDiv) {
	var years = parentDiv.find('input[name=years]').val();
	var semesters = parentDiv.find('input[name=semesters]').val();

	var totalSemesters = parseInt(years * 2, 10) + parseInt(semesters, 10);

	parentDiv.find('span[name=semestersTotal]').html(totalSemesters);
	return totalSemesters;
}

function calculateDays(parentDiv) {
	var years = parentDiv.find('input[name=years]').val();
	var months = parentDiv.find('input[name=months]').val();
	var weeks = parentDiv.find('input[name=weeks]').val();
	var days = parentDiv.find('input[name=days]').val();

	var vals = [years, months, weeks, days];
	for (var v = 0; v < vals.length; v++) {
		if (!vals[v]) {vals[v] = 0;};
	}
	var totalDays = parseInt(years * 365) + parseInt(months * 30) + parseInt(weeks * 7) + parseInt(days);
	parentDiv.find('span[name=daysTotal]').html(totalDays);
	return totalDays;
}

$(document).ready(function() {
	//calculateDays( $('#) );
	//make sure the counters are up to date with the inputs
});
