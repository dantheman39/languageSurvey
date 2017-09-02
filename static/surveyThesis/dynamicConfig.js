dynamicDr.setEngine("djangoFormset");
var natLangRenumSpec = dynamicDr.renumArgsBase(
	[
		{ selector: "div", propToChange: "id", addBack: true },
		{ selector: "label", propToChange: "for" },
		{ selector: "select", propToChange: "id" },
		{ selector: "select", propToChange: "name" },
		{ selector: "input", propToChange: "id" },
		{ selector: "input", propToChange: "name" },
	]
);

var forLangRenumSpec = dynamicDr.renumArgsBase(
	[
		{ selector: ".foreignLangDiv", propToChange: "id", addBack: true },
		{ selector: "label", propToChange: "for"},
		{ selector: "select", propToChange: "id" },
		{ selector: "select", propToChange: "name" },
		{ selector: "input", propToChange: "id" },
		{ selector: "input", propToChange: "name" },
	]
);
var forLangResetSpec = dynamicDr.renumArgsBase(
	[
		{ selector: "input" },
		{ selector: ".daysTotal,.semestersTotal", newVal: "0" },
	]
);
var rmNatLangClass = "rmNatLangButt";
var rmForLangClass = "rmForLangButt";
var natLangForm = "natLang";

var hideShowTimeDivs = function(container) {
	// if container is undefined hideShow all timeDivs.
	// Assumes all divs will each have checkbox input, 
	// and all checkbox inputs have the same class, 
	// so there are the same number of divs and checkboxes
	var calDivs;
	var calDivsSel = ".studyCalculator,.daysCalculator";
	var inputSelector = ".hideShowCb";
	var cbs;
	if (container === undefined) {
		calDivs = $(calDivsSel);
		cbs = $(inputSelector);
	} else {
		calDivs = $(container).find(calDivsSel);
		cbs = $(container).find(inputSelector);
	}

	var numCalDivs = calDivs.length;
	var i;
	var calDiv;
	var cb;
	for (i = 0; i < numCalDivs; i++) {
		calDiv = $(calDivs[i]);
		cb = $(cbs[i]);
		dynamicDr.hideShowDiv(calDiv, cb);
	}
};

$(document).ready(function() {

	dynamicDr.hideShowDiv("#foreignLanguageWrapper", "input[name=foreignLangBool]");
	dynamicDr.hideShowDiv("#visionProblemsDetails", "input[name=visionProblems]");
	dynamicDr.hideShowDiv("#readingProblemsDetails", "input[name=readingProblems]");

	$("input[name=foreignLangBool]").on("change", function() {
		dynamicDr.hideShowDiv("#foreignLanguageWrapper", "input[name=foreignLangBool]");
	});
	$("input[name=visionProblems]").on("change", function() {
		dynamicDr.hideShowDiv("#visionProblemsDetails", "input[name=visionProblems]");
	});
	$("input[name=readingProblems]").on("change", function() {
		dynamicDr.hideShowDiv("#readingProblemsDetails", "input[name=readingProblems]");
	});

	hideShowTimeDivs();

	$(document).on("change", ".hideShowCb", function() {
		dynamicDr.hideShowDiv($(this).next("div"), $(this));
	});

	// hide all inputs for DELETE
	var deleteIns = $("input[id$=DELETE]");
	deleteIns.prop("hidden", true);
	// hide all divs that are marked as deleted (after bad POST, for example)
	deleteIns.filter(":checked").parent().prop("hidden", true);

	$(".addNatLangButt").click(function() {
		var newDiv = dynamicDr.cloneAndRenumber("natLangDiv", "#nativeLangWrapper", natLangForm, rmNatLangClass, natLangRenumSpec, natLangForm);
		var butt = newDiv.find("button");
		butt.html("-");
		butt.prop("class", rmNatLangClass);
	});

	$(".addForLangButt").click(function() {
		var newDiv = dynamicDr.cloneAndRenumber("foreignLangDiv", "#foreignLanguageWrapper", "foreignLangDiv", "dontMattah", forLangRenumSpec, "forLang");
		dynamicDr.resetMultipleValues(forLangResetSpec, newDiv);
		hideShowTimeDivs(newDiv);

		var butt = newDiv.find("button");
		butt.html("Remove");
		butt.prop("class", rmForLangClass);
	});

});

$(document).on('click', "." + rmNatLangClass, function () {
	var papa = $(this).parent();
	var parentId = papa.prop("id");
	var divNum = dynamicDr.getLettersAndNumber(parentId).number;
	papa.prop("hidden", true);
	var deleteInputId = "id_" + natLangForm + "-" + divNum + "-DELETE";
	document.getElementById(deleteInputId).checked = true;
});

$(document).on('click', "." + rmForLangClass, function() {
	var papa = $(this).parent();
	var parentId = papa.prop("id");
	var divNum = dynamicDr.getLettersAndNumber(parentId).number;
	papa.prop("hidden", true);
	var deleteInputId = "id_forLang-" + divNum + "-DELETE";
	document.getElementById(deleteInputId).checked = true;
});
