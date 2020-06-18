function edit_tableEffort(){
    var table = $("#tableEffort").DataTable({
        destroy: true,
        "columnDefs": [ 
            {
                //No.TC
                "targets": 4,
                "render": function ( data, type, row, meta ) {
                    //console.log(data)
                return '<td><input value="'+data+'"></td';
                }
            },
            {
                //No.TC
                "targets": 4,
                "render": function ( data, type, row, meta ) {
                    //console.log(data)
                return '<td><input value="'+data+'"></td';
                }
            },
            {
                // Effort
                "targets": 5,
                "render": function ( data, type, row, meta ) { 
                    //console.log(row)
                return '<td><input value="'+data+'"></td';
                }
            },
            {
                // Comments
                "targets": 6,
                "render": function ( data, type, row, meta ) { 
                    //console.log(row)
                return '<td><div><textarea rows="1" cols="50">'+data+'</textarea></div></td>';
                }
            },
            {
                "targets": 0,
                "visible": false,
            },
        ]
    });
    $('#edit_tableEffort').hide();
    $('#save_tableEffort').show();
    $('#cancel_tableEffort').show();
}

function save_tableEffort(){
    $('#edit_tableEffort').show();
    $('#save_tableEffort').hide();
    $('#cancel_tableEffort').hide();
}

function cancel_tableEffort(){
    $('#edit_tableEffort').show();
    $('#save_tableEffort').hide();
    $('#cancel_tableEffort').hide();
}

function delete_row(taskID, token){
    var form = $("#delete_task_"+taskID).closest("form")
    $.ajax({
        url : "",
        data : form.serialize(),
        dataType : 'json',
        type : 'POST',
        success : function(data) {
            if (data.success){
                $('#Delete_'+taskID).modal('hide');
                document.location.reload(true);
            }
            else {
               
            }
        }
    });
}
