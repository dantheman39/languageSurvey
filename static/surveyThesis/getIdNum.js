function getLastIdNumLastElement(element, idNoNum) {
	var $lastElement = $(element + '[id^=' + idNoNum + ']:last');
	var num = getFinalNumInString( $lastElement.prop('id') );
	return num;
}

function getFinalNumInString(s) {
	//The forward slashes start and end the javascript regexp
	//\d means digit, + means match preceding expression 1 or more times
	//g is a flag that means global search
	var num = parseInt( s.match(/\d+/g), 10 );
	return num;
}
