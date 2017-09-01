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

var rmNatLangClass = "rmNatLangButt";
var natLangForm = "natLang";
$(document).ready(function() {

	// hide all inputs for DELETE
	var deleteIns = $("input[id$=DELETE]");
	deleteIns.prop("hidden", true);
	// hide all divs that are marked as deleted (after bad POST, for example)
	deleteIns.filter(":checked").parent().prop("hidden", true);

	$(".addNatLangButt").click(function() {
		var newDiv = dynamicDr.cloneAndRenumber("natLangDiv", "#nativeLangWrapper", natLangForm, rmNatLangClass, natLangRenumSpec);
		var butt = newDiv.find("button");
		butt.html("-");
		butt.prop("class", rmNatLangClass);
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
