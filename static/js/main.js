// Function for adding Training Phrase



// ******** Author: Salman Rakin ********

//var address='http://' + document.domain + ':' + location.port+'admin_welcome'
//console.log(address);


$(document).ready(function () {
    var phraseId = 1;
    var samId=1;
    var intent_name;
    var training=[];
    var response=[];


     $("#loginn").click(function () {

         var username= $("#username").val();
         var password= $("#password").val();
         alert(username);
         alert(password);
         console.log("Username:- ", username);
         console.log("Password:- ", password);
         //console.log($("#i_name").val());

    });

    $('#btn').click(function () {
        var prevId="t_name";
        var placeholder = "Add Phrase" ;
        $("#t_phrase").append('<label for= "'+prevId+phraseId+'">' + '</label>' + '<input type="text" class="form-control" placeholder="'+placeholder+'" id="'+prevId+phraseId+'">');
        phraseId++;
    });
    $("#btn_sample").click(function () {

        var prevId = "sam_response";
        var placeholder = "Add Response ";
        $("#sample_response").append('<label for="'+prevId+samId+'">' +'</label><input type="text" class="form-control"  placeholder="'+placeholder+'" id="' +prevId+samId+'"/>');
        samId++;
    });
    function getArray(divId, inputId){
        var divLength = $(divId).children().length/2;
        var myArray=[];

        for (var i=0; i<divLength; i++){
            var main_id=(inputId+i.toString());
            myArray.push($(main_id).val());
        }
        return myArray;
    }
    $("#btn_submit").click(function () {


        training=getArray('#t_phrase', '#t_name')
        console.log(training);
        response=getArray('#sample_response', '#sam_response');
        console.log(response);
        intent_name=$("#i_name").val();
        console.log(intent_name);

    });



});
