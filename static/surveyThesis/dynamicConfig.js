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
		{ selector: "select" },
		{ selector: "input" },
		{ selector: ".daysTotal,.semestersTotal", newVal: "0" },
	]
);
var herLangRenumSpec = dynamicDr.renumArgsBase(
	[
		{ selector: ".heritageLangDiv", propToChange: "id", addBack: true },
		{ selector: "label", propToChange: "for"},
		{ selector: "select", propToChange: "id"},
		{ selector: "select", propToChange: "name"},
		{ selector: "input", propToChange: "id" },
		{ selector: "input", propToChange: "name" },
		{ selector: "textarea", propToChange: "id"},
		{ selector: "textarea", propToChange: "name"},
	]
);
var herLangResetSpec = dynamicDr.renumArgsBase(
	[
		{ selector: "select" },
		{ selector: "input" },
		{ selector: "textarea" },
	]
);

var rmNatLangClass = "rmNatLangButt";
var rmForLangClass = "rmForLangButt";
var rmHerLangClass = "rmHerLangButt";
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

var hideShowUnderGrad = function () {
	var select = $('#id_education');
	var selected = select.val();
	var hiddenDiv = $('#undergradLevelDiv');
	if (selected === "undergrad") {
		hiddenDiv.show();
	} else {
		hiddenDiv.hide();
	}
};

$(document).ready(function() {

	$("form").attr("autocomplete", "off");

	dynamicDr.hideShowDiv("#foreignLanguageWrapper", "input[name=foreignLangBool]");
	dynamicDr.hideShowDiv("#heritageLanguageWrapper", "input[name=heritageLangBool]");
	dynamicDr.hideShowDiv("#visionProblemsDetails", "input[name=visionProblems]");
	dynamicDr.hideShowDiv("#hearingProblemsDetails", "input[name=hearingProblems]");

	$("input[name=foreignLangBool]").on("change", function() {
		dynamicDr.hideShowDiv("#foreignLanguageWrapper", "input[name=foreignLangBool]");
	});
	$("input[name=heritageLangBool]").on("change", function() {
		dynamicDr.hideShowDiv("#heritageLanguageWrapper", "input[name=heritageLangBool]");
	});
	$("input[name=visionProblems]").on("change", function() {
		dynamicDr.hideShowDiv("#visionProblemsDetails", "input[name=visionProblems]");
	});
	$("input[name=hearingProblems]").on("change", function() {
		dynamicDr.hideShowDiv("#hearingProblemsDetails", "input[name=hearingProblems]");
	});
	$("#id_education").on("change", function() {
		hideShowUnderGrad();
	});

	hideShowTimeDivs();
	hideShowUnderGrad();

	$(document).on("change", ".hideShowCb", function() {
		dynamicDr.hideShowDiv($(this).next("div"), $(this));
	});

	// hide all inputs for DELETE
	var deleteIns = $("input[id$=DELETE]");
	deleteIns.prop("hidden", true);
	// hide all divs that are marked as deleted (after bad POST, for example)
	// assumes the parent is the div you want to hide
	deleteIns.filter(":checked").parent().prop("hidden", true);

	$(".addNatLangButt").click(function() {
		var newDiv = dynamicDr.cloneAndRenumber("natLangDiv", "#nativeLangWrapper", natLangForm, rmNatLangClass, natLangRenumSpec, natLangForm);
		newDiv.find(".errorlist").remove();
		var butt = newDiv.find("button");
		dynamicDr.resetValues({ selector: "select" }, newDiv);
		butt.html("Remove");
		butt.prop("class", rmNatLangClass);
		// remove errors
	});

	$(".addForLangButt").click(function() {
		var newDiv = dynamicDr.cloneAndRenumber("foreignLangDiv", "#foreignLanguageWrapper", "foreignLangDiv", "dontMattah", forLangRenumSpec, "forLang");
		newDiv.find(".errorlist").remove();
		dynamicDr.resetMultipleValues(forLangResetSpec, newDiv);
		hideShowTimeDivs(newDiv);

		var butt = newDiv.find("button");
		butt.html("Remove");
		butt.prop("class", rmForLangClass);
	});

	$(".addHerLangButt").click(function() {
		var newDiv = dynamicDr.cloneAndRenumber("heritageLangDiv", "#heritageLanguageWrapper", "heritageLangDiv", "dontMattah", herLangRenumSpec, "herLang");
		newDiv.find(".errorlist").remove();
		dynamicDr.resetMultipleValues(herLangResetSpec, newDiv);
		hideShowTimeDivs(newDiv);

		var butt = newDiv.find("button");
		butt.html("Remove");
		butt.prop("class", rmHerLangClass);
	});

});

// This is a helper function used by the following three 
// event handlers. They set a form as marked for deletion
//
// papa is the parent of a given "delete" button
var setDivForDelete = function(papa, deleteInputIdPrefix) {
	var parentId = papa.prop("id");
	var divNum = dynamicDr.getLettersAndNumber(parentId).number;
	papa.prop("hidden", true);
	var deleteInputId = deleteInputIdPrefix + divNum + "-DELETE";
	document.getElementById(deleteInputId).checked = true;
};

$(document).on('click', "." + rmNatLangClass, function () {
	var deleteInputIdPre = "id_" + natLangForm + "-";
	var papa = $(this).parent();
	setDivForDelete(papa, deleteInputIdPre);
});

$(document).on('click', "." + rmForLangClass, function() {
	var deleteInputIdPre = "id_forLang-";
	var papa = $(this).parent();
	setDivForDelete(papa, deleteInputIdPre);
});

$(document).on('click', "." + rmHerLangClass, function() {
	var deleteInputId = "id_herLang-";
	var papa = $(this).parent();
	setDivForDelete(papa, deleteInputIdPre);
});
