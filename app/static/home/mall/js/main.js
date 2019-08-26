function sendMessage(obj) {
    //禁用提交按钮，避免重复提交
    obj.disabled = true;
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: '/message',//url
        data: $('#contact-form').serialize(),
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
                setTimeout(function () {
                    window.location.reload();
                }, 5000);
            } else {
                toastr.error(result.msg);
                obj.disabled = false;
            }
            ;
        },
        error: function () {
            toastr.error("System error, message submitted failure, please call our phone.");
        }
    });

}