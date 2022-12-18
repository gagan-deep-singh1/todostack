$(document).ready(function () {
    $("#tag_line").fadeIn("slow");
    var upd_task_prev;

    function refreshData() {
        $("#maintable").load(window.location.href + " #maintable");
        $("#completed-table").load(window.locationation.href + " #completed-table");
    }

    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 5000);


    $(document).on("click", ".update_btns", function () {
        upd_task_prev = $(this).parent().parent().find('h4').text().trim();
        var edit_field = '<input type="text" name="task" style="float: left;" class="form-control" id= "add_task" maxlength="60" value="' + upd_task_prev.replace(/"/g, '&quot;') + '" autofocus>';
        $(this).parent().parent().find('td:eq(1)').html(edit_field);
        $(this).hide();
        $(this).siblings('.update_task_btn').show();
    });

    $(document).on("click", ".update_task_btn", function () {
        $(this).hide()
        $(this).siblings('.update_btns').show();
        var upd_task_current = $(this).parent().parent().find('td:eq(1)').find('input').val().trim();
        var upd_id = $(this).parent().parent().find('td:eq(0)').find('input').attr('id');

        if (upd_task_current == upd_task_prev && upd_task_current.length > 0) {
            var upd_field = '<h4 class="text-left" id="title' + upd_id + '">' + upd_task_current + '</h4>';
            $('.task_' + upd_id).find('td:eq(1)').html(upd_field);
        }

        else {
            if (upd_task_current.length == 0) {
                alert('Task Name cannot be Empty!');
                var upd_field = '<h4 class="text-left" id="title' + upd_id + '">' + upd_task_prev + '</h4>';
                $('.task_' + upd_id).find('td:eq(1)').html(upd_field);
            }
            else {
                $.ajax({
                    type: 'POST',
                    url: '/update_task/',
                    cache: false,
                    data: {
                        task_id: upd_id,
                        task_name: upd_task_current,
                    },
                    success: function () {
                        var upd_field = '<h4 class="text-left" id="title' + upd_id + '">' + upd_task_current + '</h4>';
                        $('.task_' + upd_id).find('td:eq(1)').html(upd_field);

                    }
                });
            }
        }
    });


    $(document).on("click", ".delete_existing_row, .delete_new_row", function () {
        if ($(this).hasClass('delete_new_row')) {
            $(this).parent().parent().remove();
        }
        else {
            var val = $(this).parent().parent().find('input').attr("id");
            var c = confirm('Are you sure you want to delete this task ?');
            if (c == true) {
                $.ajax(
                    {
                        type: "POST",
                        url: "/delete_task/",
                        cache: false,
                        data: {
                            task_id: val,
                        },
                        success: function () {
                            refreshData();
                        }
                    });
            }
        }

    });


    $("#completed-table").on('click', '#clear_all_completed_tasks', function () {
        if ($('#completed-table tr').length <= 2) {
            alert('No Completed Tasks to Clear!');
        }
        else {
            var cd = confirm('Are you sure you want to delete all completed tasks ?');
            if (cd == true) {
                $.ajax(
                    {
                        type: "POST",
                        url: "/delete_all_completed_tasks/",
                        data: {},
                        success: function () {
                            refreshData();
                        }
                    });
            }
        }
    });


    $("table").on('click', "#add_task_btn", function () {
        var task_name;
        task_name = $.trim($('#add_task').val());

        if (task_name != "") {
            $.ajax(
                {
                    type: "POST",
                    url: "/add_new_task/",
                    data: {
                        title: task_name,
                    },
                    success: function ()
                    {
                        refreshData();
                    }
                })
        }
        else {
            alert('Enter a Valid Task Name!');
        }
    });


    $("table").on('click', ".mark_as_done, .mark_as_undone", function () {
        if ($(this).hasClass('mark_as_done')) {
            var check_id;
            check_id = $(this).attr("id");
            class_name = $(this).attr("class");
            task_name = $("#title" + check_id).html();
            $.ajax(
                {
                    type: "POST",
                    url: "/move_tasks/",
                    data: {
                        task_id: check_id,
                        task_class: class_name
                    },
                    success: function () {
                        refreshData()


                    }
                })

        }
        else {
            var un_check_id;
            un_check_id = $(this).attr("id");
            task_name = $("#title" + un_check_id).html();
            class_name = $(this).attr("class");
            $.ajax(
                {
                    type: "POST",
                    url: "/move_tasks/",
                    data: {
                        task_id: un_check_id,
                        task_class: class_name
                    },
                    success: function () {
                        refreshData();
                    }
                })

        }

    });

});
