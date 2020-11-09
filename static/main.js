// Function for adding Training Phrase

$(document).ready(function () {
    var id=1;
    var sam_id = 1;
    var phrase_values
    $("#btn").click(function(){
        var prev_id="t_name";
        var name = "add phrase" ;
        var main_id="#"+(prev_id+(id-1).toString());
        console.log($(main_id).val());
        $("#t_phrase").append('<label for= "'+prev_id+id+'">' + '</label>' +
            '<input type="text" class="form-control" placeholder="'+name+'" id="'+prev_id+id+'">')

        id++;
    });
    $("#btn_sample").click(function () {
        var place_holder = "add response";
        var prev_id="sam_response";
        var main_sam_id="#"+(prev_id+(sam_id-1).toString());
        console.log($(main_sam_id).val());
        $("#sample_response").append('<label for="'+prev_id+sam_id+'">' +'</label>' +
            '<input type="text" class="form-control" placeholder="'+place_holder+'" id="'+prev_id+sam_id+'"/>')
        sam_id++;
        // console.log(sam_id)
    });
    function getArray(divId, inputId){
        var divLength = $(divId).children().length/2;
        myArray=[];

        for (var i=0; i<divLength; i++){
            var main_id=(inputId+i.toString());
            myArray.push($(main_id).val());
        }
        return myArray;
    }
    $("#btn_submit").click(function () {
        console.log(getArray('#t_phrase', '#t_name' ));
        console.log(getArray('#sample_response', '#sam_response'));
        console.log($("#i_name").val());
        // $('.display').append(myArray);


    });
    $('#my-form').on('submit', function () {

        // alert(getArray());

    })


});
