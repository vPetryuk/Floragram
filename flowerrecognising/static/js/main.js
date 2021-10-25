
$(document).ready(function(){
    $('#modal-btn').click(function(){
        console.log('working')
        $('.ui.mymodal')
        .modal('show')
        ;
    })
    $('.ui.dropdown').dropdown()
})
