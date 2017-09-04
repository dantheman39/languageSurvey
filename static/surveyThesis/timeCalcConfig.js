$(document).ready(function() {
	// calculate times
	var j;
	var sTable;
	var studyTables = $(".studyTable");
	var numSTables = studyTables.length;
	for (j = 0; j < numSTables; j++) {
		sTable = $(studyTables[j]);
		timeCalculator.calculate(sTable, ".studyTime", ".semestersTotal", "semesters", true);
	}
	var dayTables = $(".daysTable");
	var numTables = dayTables.length;
	var i;
	var table;
	for (i = 0; i < numTables; i++) {
		table = $(dayTables)[i];
		timeCalculator.calculate(table, ".timeInput", ".daysTotal", "days", true);
	}
});

$(document).on("change", ".studyTime", function() {
	var sender = $(this);
	// if no val, set to zero
	if (!(sender.val())) {
		sender.val(0);
	}
	var ind = dynamicDr.parseDjangoProp(sender.prop("id")).num;
	var container = sender.closest("table");
	timeCalculator.calculate(container, ".studyTime", ".semestersTotal", "semesters", true);
});

$(document).on("change", ".timeInput", function() {
	var sender = $(this);
	if (!(sender.val())) {
		sender.val(0);
	}
	var ind = dynamicDr.parseDjangoProp(sender.prop("id")).num;
	var container = sender.closest("table");
	timeCalculator.calculate(container, ".timeInput", ".daysTotal", "days", true);
});
