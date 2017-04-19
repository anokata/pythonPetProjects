
$(document).ready(function(){
    main();
}); 

function main() {
    console.log( "ready!" ); 
    attach_events();
}

function attach_events() {
    $(".delete").on("click", delete_event);
}

function delete_event(e) {
    e.preventDefault(); 
    id = $(this).attr('id');
    node = $(e.target)[0].parentNode.parentNode;
    $.post("del_url", { "id":id }, function(data) {
        node.remove();
    });
}
