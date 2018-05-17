$(document).ready(function() {

	window.onload = function() {
		$(".ui-dialog-titlebar button").text("X");
	};

	$("#deleteDialog").dialog({autoOpen: false, draggable: true});
	$("#deleteError").dialog({autoOpen: false, draggable: true});

	$(".deleteButton").on("click", function() {

		var dlg = document.getElementById("deleteDialog");
		// stash id of entry to delete in data-deleteid of deleteDialog,
		// to be used if deleteconfirmed
		dlg.dataset.deleteid = this.dataset.participantid;
		// Show dialog warning of what will happen
		$("#userName-dlg").html(this.dataset.username);
		//$("#deleteDialog").dialog("open");
		$(dlg).dialog("open");
	});

	$("#deleteConfirmed").on("click", function() {
		// Do ajax call to delete the entry and 
		// refresh the element
		var dlg = document.getElementById("deleteDialog");
		var toDelete = dlg.dataset.deleteid;
		dlg.dataset.deleteid = "";

		var csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

		//ajax call
		$.ajax({
			type: "POST",
			url: "delete/" + toDelete + "/",
			data: {"csrfmiddlewaretoken": csrf},
			success: function(data) {
				$("#entryListTable").html(data);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				$("#deleteError").dialog("open");
			}
		});

		$(dlg).dialog("close");

	});

	$("#deleteCanceled").on("click", function() {
		var dlg = document.getElementById("deleteDialog");
		dlg.dataset.deleteid = "";
		$(dlg).dialog("close");
	});

	
});
