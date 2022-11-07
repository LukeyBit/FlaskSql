$(document).ready(()=> {
    $('.update-btn').click(function(){
        let id = $(this).data('id')
        $.ajax({
            method: "POST",
            data: {'id' : id},
            dataType: "text",
            success:(response) => {
                window.location.assign(response)
            }
        })
    })
})