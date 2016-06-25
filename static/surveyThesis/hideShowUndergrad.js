function hideShowUndergrad() {
	var select = $('#id_education');
	var selected = select.val();
	var hiddenDiv = $('#undergradLevelDiv');
	if (selected === "undergrad") {
		hiddenDiv.show();
	} else {
		hiddenDiv.hide();
	}
}

function showLang() {
	var childDivs = $('#nativeLangWrapper').children('div'); 
	for (var count = 0; count < childDivs.length; count++) {
		var div = $(childDivs[count]);
		if (!div.is(':visible')) {
			div.show();
			break;
		}
	}
}

function hideLang(selector) {
	var div = $(selector).hide();	
}

$('#id_education').change(function() {
	hideShowUndergrad()	
}); 

$(document).ready(function() {
	hideShowUndergrad()
});

$('#natLangButt1').click(function() {
	showLang();
});

$('#natLangButt2').click(function() {
	hideLang('#natLangDiv2');
});


$('#natLangButt3').click(function() {
	hideLang('#natLangDiv3');
});

$('#natLangButt4').click(function() {
	hideLang('#natLangDiv4');
});
