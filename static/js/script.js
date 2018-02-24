$(document).on('click', '.btn-add', function (event) {
    event.preventDefault();

    var field = $(this).closest('.form-group');
    var field_new = field.clone();

    $(this)
        .toggleClass('btn-default')
        .toggleClass('btn-add')
        .toggleClass('btn-danger')
        .toggleClass('btn-remove')
        .html('–');

    field_new.find('input').val('');
    field_new.insertAfter(field);
});

$(document).on('click', '.btn-remove', function (event) {
    event.preventDefault();
    $(this).closest('.form-group').remove();
});


$(function () {
    $("#submit").click(function () {
            var $reviewers = new Array();
            var $id = parseInt($("#submit").val())

            $("#reviewers").find(".form-control").each(function () {
                $reviewers.push($(this).val())
            })
            $.ajaxSetup({
                headers: {"X-CSRFToken": getCookie("csrftoken")}
            });

            $.ajax({
                type: 'POST',
                url: '/editor/' + $id,
                data: {
                    "reviewers[]": $reviewers,
                    "status": $("#status").val()
                },
                dataType: 'json'
            })
        }
    )
    function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

})