
//Both header and data are 1dim arrays. TODO, data as json
function genFsimpleTable(header, data){
	$('#simpleTable').empty('.ul_remove');
	$('#simpleTable').append('<thead/>');
	var header = ['customer']	
	for (index in data){
		console.log(data[index]);
		$('<tr class="ul_remove"/>').appendTo('#simpleTable').append('<td>'+String(data[index])+'</td>');
	};
	for (index in header){
		$('#simpleTable thead').append('<td>'+String(header[index])+'</td>');
	};
};

