$(document).ready(()=> {
    let manager_id = $('#active_empl').data('manager-id')
    let department_id = $('#active_empl').data('department-id')
    $('.manager').each(function(){
        if ($(this).val() == manager_id){
            $(this).attr('selected', 'selected');
        }
    })
    $('.department').each(function(){
        if ($(this).val() == department_id){
            $(this).attr('selected', 'selected')
        }
    })
})