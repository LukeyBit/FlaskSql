$(document).ready(() => {
    $('.delete').on('click', function () {
        let id = $(this).data('id')
        $.confirm({
            title: 'Delete?',
            content: 'Are you sure that you want to delete this data?',
            type: 'green',
            buttons: {
                ok: {
                    text: 'OK',
                    btnClass: 'btn-danger',
                    action: () => {
                        $.ajax({
                            type: "DELETE",
                            url: '/delete-empl',
                            data: {'id' : id},
                            dataType: "text",
                            success: (response)=> {
                                console.log(response)
                                location.reload(true)
                            }
                        })
                    }
                },
                cancel: {
                    text: 'Cancel',
                    keys: ['enter', 'space'],
                    btnClass: 'btn-primary',
                }
            }
        })
    })
})