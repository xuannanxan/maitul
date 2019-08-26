/**
 * Created by xuannan on 2019-02-09.
 */
//[Master Javascript]

//Project:	MinimalLite Admin - Responsive Admin Template
//Primary use:	MinimalLite Admin - Responsive Admin Template

//should be included in all pages. It controls some layout

$(function () {
    $(".preloader").fadeOut();
}), jQuery(document).on("click", ".mega-dropdown", function (i) {
    i.stopPropagation();
})
//初始化select2
$('.select2').select2({
    language: "zh-CN",
    minimumInputLength: 0,
    placeholder: "请选择",//默认值
    allowClear: true,
})
$('.select2').change(function () {
    var arr = [];
    $(this).select2('data').forEach(function (v) {
        arr.push(v.id)
    });
    $(this).prev().val(arr.join(','))
})
//初始化tooltip
$('[data-toggle="tooltip"]').tooltip()


$('.treeview-menu').find('li').each(function () {
    if ($(this).hasClass('active')) {
        $(this).parent().parent().addClass('menu-open active')
    }
})
// Make sure jQuery has been loaded
if (typeof jQuery === 'undefined') {
    throw new Error('template requires jQuery')
}

// Layout()

//  Implements layout.
//  Fixes the layout height in case min-height fails.

//  @usage activated automatically upon window load.
//  Configure any options by passing data-option="value"
//  to the body tag.

accessid = ''
accesskey = ''
host = ''
policyBase64 = ''
signature = ''
callbackbody = ''
filename = ''
key = ''
expire = 0
g_object_name = ''
g_object_name_type = ''
now = timestamp = Date.parse(new Date()) / 1000;

function send_request() {
    var xmlhttp = null;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }
    else if (window.ActiveXObject) {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    if (xmlhttp != null) {
        // serverUrl是 用户获取 '签名和Policy' 等信息的应用服务器的URL，请将下面的IP和Port配置为您自己的真实信息。
        serverUrl = '/admin/oss_token'

        xmlhttp.open("GET", serverUrl, false);
        xmlhttp.send(null);
        return xmlhttp.responseText
    }
    else {
        alert("Your browser does not support XMLHTTP.");
    }
};

function check_object_radio() {
    var tt = document.getElementsByName('myradio');
    for (var i = 0; i < tt.length; i++) {
        if (tt[i].checked) {
            g_object_name_type = tt[i].value;
            break;
        }
    }
}

function get_signature() {
    // 可以判断当前expire是否超过了当前时间， 如果超过了当前时间， 就重新取一下，3s 作为缓冲。
    now = timestamp = Date.parse(new Date()) / 1000;
    if (expire < now + 3) {
        body = send_request()
        var obj = eval("(" + body + ")");
        host = obj['host']
        policyBase64 = obj['policy']
        accessid = obj['accessid']
        signature = obj['signature']
        expire = parseInt(obj['expire'])
        callbackbody = obj['callback']
        key = obj['dir']
        return true;
    }
    return false;
};

function random_string(len) {
    len = len || 32;
    var chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
    var maxPos = chars.length;
    var pwd = '';
    for (i = 0; i < len; i++) {
        pwd += chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
}

function get_suffix(filename) {
    pos = filename.lastIndexOf('.')
    suffix = ''
    if (pos != -1) {
        suffix = filename.substring(pos)
    }
    return suffix;
}

function calculate_object_name(filename) {
    if (g_object_name_type == 'local_name') {
        g_object_name += "${filename}"
    }
    else if (g_object_name_type == 'random_name') {
        suffix = get_suffix(filename)
        g_object_name = key + random_string(10) + suffix
    }
    return ''
}

function get_uploaded_object_name(filename) {
    if (g_object_name_type == 'local_name') {
        tmp_name = g_object_name
        tmp_name = tmp_name.replace("${filename}", filename);
        return tmp_name
    }
    else if (g_object_name_type == 'random_name') {
        return g_object_name
    }
}

function set_upload_param(up, filename, ret) {
    if (ret == false) {
        ret = get_signature()
    }
    g_object_name = key;
    if (filename != '') {
        suffix = get_suffix(filename)
        calculate_object_name(filename)
    }
    new_multipart_params = {
        'key': g_object_name,
        'policy': policyBase64,
        'OSSAccessKeyId': accessid,
        'success_action_status': '200', //让服务端返回200,不然，默认会返回204
        'callback': callbackbody,
        'signature': signature,
    };

    up.setOption({
        'url': host,
        'multipart_params': new_multipart_params
    });

    up.start();
}

//plupload
function initPlupload(element, maxFiles = 1, extData) {
    var uploader = new plupload.Uploader({
        runtimes: 'html5,flash,silverlight,html4',// 上传模式，依次退化
        browse_button: element,// 上传选择的点选按钮，必需
        //container: document.getElementById(element),
        //multi_selection: false,
        flash_swf_url: '../../components/plupload/js/Moxie.swf',
        silverlight_xap_url: '../../components/plupload/js/Moxie.xap',
        multipart_params: extData,
        url: '/admin/upload',
        auto_start: true, // 选择文件后自动上传，若关闭需要自己绑定事件触发上传
        filters: {
            mime_types: [ //只允许上传图片和zip文件
                {title: "Image files", extensions: "jpg,gif,png,bmp"},
                {title: "Zip files", extensions: "zip,rar"}
            ],
            max_file_size: '10mb', //最大只能上传10mb的文件
            prevent_duplicates: true //不允许选取重复文件
        },
        init: {
            'FilesAdded': function (up, files) {
                plupload.each(files, function (file) {
// 文件添加进队列后,处理相关的事情 

                });
            },
            'BeforeUpload': function (up, file) {
// 每个文件上传前,处理相关的事情 
            },
            'UploadProgress': function (up, file) {
// 每个文件上传时,处理相关的事情 
            },
            'UploadComplete': function () {
//队列文件处理完毕后,处理相关的事情 

            },
            'FileUploaded': function (up, file, info) {
                if (info.status == 200) {
                    var response = eval("(" + info.response + ")");
                    showAllFiles(element,response.file_name)
                }
                else {
                    toastr.error(info.response);
                }
            },
            Error: function (up, err) {
                if (err.code == -600) {
                    toastr.error("选择的文件太大了");
                }
                else if (err.code == -601) {
                    toastr.error("选择的文件后缀不对");
                }
                else if (err.code == -602) {
                    toastr.error("这个文件已经上传过一遍了");
                }
                else {
                    toastr.error(err.response);
                }
            }
        }
    });
    uploader.init();
}
//plupload清空展示的文件
function clearAllPreviousFiles(element) {
    var previous = document.getElementById(element).previousSibling;
    if (previous) {
        previous.parentNode.removeChild(previous)
        clearAllPreviousFiles(element)
    }else {
        return
    }
}
//plupload展示列表的文件
function showAllFiles(element,newFile) {
    var arr = []
    var formInput = document.getElementById(element).nextElementSibling;
    var oldFile = formInput.value
    if (oldFile) {
         arr = oldFile.split(',');//转数组
    }
    if (newFile){
        arr.push(newFile)//添加新上传的文件
    }
    formInput.value = arr.join(',');//转字符
    clearAllPreviousFiles(element) //清空所有已添加的数据
    arr.forEach(function (v) {
        var img = document.createElement('div');
        img.className = 'col-sm-2 pluploadshow';
        img.setAttribute('file_data', v);
        img.style.backgroundImage = "url(" +v + ")";
        var remove = document.createElement('div');
        remove.className = 'remove-btn';
        var icon = document.createElement('i');
        icon.className = 'fa fa-times'
        remove.appendChild(icon);
        img.appendChild(remove);
        document.getElementById(element).parentNode.insertBefore(img, document.getElementById(element));
                //plupload 移除文件
        $(remove).on('click',function(){
            var removefile = $(this).parent().attr('file_data')
            var index = arr.indexOf(removefile);
            if (index > -1) {
                arr.splice(index, 1);
            }
            formInput.value =arr.join(",");
            showAllFiles(element)
        })
    });
}

//上传到本地
function initImageUpload(element, maxFiles = 1, extData, formInput, info) {
    var myDropzone = new Dropzone(element, {
        url: "/admin/upload",//上传文件的地址，
        maxFiles: maxFiles,//最多上传几个图片
        params: extData,
        maxFilesize: 5,//图片的大小，单位是M
        addRemoveLinks: false,//是否有删除图片的功能
        acceptedFiles: "image/*",//支持的格式
        paramName: 'file',//上传的FILE名称，即服务端可以通过此来获取上传的图片，如$_FILES['dropimage']
        dictDefaultMessage: "将文件拖至此处或点击上传....",
        dictInvalidFileType: "格式错误,请上传图片...",
        dictResponseError: "服务器连接失败...",
        dictMaxFilesExceeded: "不能上传这么多...",
        dictRemoveFile: "移除文件",
        previewTemplate: "<div class=\"dz-preview dz-file-preview\">\n  " +
        "<div class=\"dz-image\">\n    " +
        "<img data-dz-thumbnail />\n " +
        "</div>\n  " +
        "<div class=\"dz-details\">\n    " +
        "<div class=\"dz-filename\"><span data-dz-name></span></div>\n " +
        "<a class=\"dz-delete\" onclick='removeFile(this)' data-dz-remove><i class='fa fa-close'></i>删除</a>\n " +
        "</div>\n  " +
        "<div class=\"dz-progress\"><span class=\"dz-upload\" data-dz-uploadprogress></span></div>\n " +
        " <div class=\"dz-success-mark\"><span></span></div>\n " +
        " <div class=\"dz-error-mark\"><span></span></div>\n " +
        " <div class=\"dz-error-message\"><span data-dz-errormessage></span></div>\n" +
        "</div>",
    });
    if (info) {
        initImageShow(myDropzone, info)
    }
    myDropzone.on("success", function (file, response) {
        myDropzone.removeFile(file);
        initImageShow(myDropzone, response.file_name)
        if (response.code == 1) {
            var arr = []
            if (formInput.val()) {
                var arr = formInput.val().split(',');//转数组
            }
            arr.push(response.file_name)//添加新上传的文件
            formInput.val(arr.join(','));//转字符
        } else {
            toastr.error(response.msg);
        }
    });
    myDropzone.on("removedfile", function (file) {
        var arr = formInput.val().split(',');
        var index = arr.indexOf(file_to_path(file.name));
        if (index > -1) {
            arr.splice(index, 1);
        }
        formInput.val(arr.join(","));
    });
    return myDropzone
}
// 编辑时显示已有数据
function initImageShow(dz, info) {
    if (info == '' || !info) return false;
    var info_array = info.split(",");
    for (var i in info_array) {
        var hidefileval_str = info_array[i];
        var hidefileval_arr = hidefileval_str.split("/");
        var mockfile_object = {name: hidefileval_arr[hidefileval_arr.length - 1], accepted: true}
        dz.emit('addedfile', mockfile_object);
        dz.emit('thumbnail', mockfile_object, hidefileval_str);
        dz.emit('processing', mockfile_object);
        dz.emit('complete', mockfile_object);
        dz.files.push(mockfile_object);
        mockfile_object = null;
    }
}
//彻底删除文件
function removeFile(obj) {
    var file_name = $(obj).prev()[0].innerText
    $.ajax({
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/admin/del_file",
        data: {
            csrf_token: extraData['csrf_token'],
            "file_name": file_name
        },
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
            } else {
                toastr.error(result.msg);
            }
            ;
        },
        error: function () {
            toastr.error("服务器异常，请稍后重试！");
        }
    });
}
//根据文件名称获取路径
function file_to_path(file_name) {
    return "/static/uploads/" + file_name.substring(0, 8) + "/" + file_name;
}
//删除方法
function deleteFun(obj) {
    //禁用提交按钮，避免重复提交
    obj.disabled = true;
    var url = $(obj).attr('url');
    var id = $(obj).attr('id');
    var csrftoken = $(obj).attr('csrftoken');
    swal({
        title: "确定删除?",
        text: "删除后将无法恢复!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        closeOnConfirm: false
    }, function () {
        $.ajax({
            type: "DELETE",//方法类型
            dataType: "json",//预期服务器返回的数据类型
            url: url,//url
            headers: {"X-CSRFToken": csrftoken},
            data: {"id": id},
            success: function (result) {
                if (result.code == 1) {
                    toastr.success(result.msg);
                    setTimeout(function () {
                        window.location.reload();
                    }, 1000);
                } else {
                    toastr.error(result.msg);
                    obj.disabled = false;
                }
                ;
            },
            error: function () {
                toastr.error("服务器异常，请稍后重试！");
            }
        });
    })
    obj.disabled = false;
}

function updateFun(obj) {
    //禁用提交按钮，避免重复提交
    obj.disabled = true;
    var url = $(obj).attr('url');
    var formId = $(obj).attr('formId');
    var form = $('#' + formId)
    $.ajax({
        type: "PUT",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: url,//url
        data: form.serialize(),
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
                setTimeout(function () {
                    window.location.reload();
                }, 1000);
            } else {
                toastr.error(result.msg);
                obj.disabled = false;
            }
            ;
        },
        error: function () {
            toastr.error("服务器异常，请稍后重试！");
        }
    });

}

function addFun(obj) {
    //禁用提交按钮，避免重复提交
    obj.disabled = true;
    var url = $(obj).attr('url');
    var formId = $(obj).attr('formId');
    var form = $('#' + formId)
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: url,//url
        data: form.serialize(),
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
                setTimeout(function () {
                    window.location.reload();
                }, 1000);
            } else {
                toastr.error(result.msg);
                obj.disabled = false;
            }
            ;
        },
        error: function () {
            toastr.error("服务器异常，请稍后重试！");
        }
    });

}

function initEditor(ctrlName, extraData, defaultValue) {
    var E = window.wangEditor
    var editor = new E(ctrlName)
    editor.customConfig.menus = [
	 		    'head',  // 标题
			    'bold' /** 粗体*/, 'fontSize' /** 字号 */, 'fontName' /** 字体 */,'italic' /** 斜体 */,
	 		    'underline',  // 下划线
			    'strikeThrough',  // 删除线
			    'foreColor',  // 文字颜色
			    'backColor',  // 背景颜色
			    'link',  // 插入链接
			    'list',  // 列表
			    'justify',  // 对齐方式
			    'quote',  // 引用
	 		   // 'emoticon',  // 表情   打开后支持表情功能
			    'image',  // 插入图片
			    'table',  // 表格
			    'video',  // 插入视频
//	 		    'code',  // 插入代码
			    'undo',  // 撤销
			    'redo'  // 重复
	                         ]
    editor.customConfig.onchange = function (html) {
        // 监控变化，同步更新到 textarea
        $(ctrlName).next().val(html)
    }
    // 自定义上传图片事件
    editor.customConfig.customUploadImg = function (files, insert) {
        files.forEach(function (file) {
            const data = new FormData();
            data.append('file', file);
            Object.keys(extraData).forEach(function (key) {
                data.append(key, extraData[key]);
            });
            $.ajax({
                url: '/admin/upload',
                type: 'POST',
                data: data,
                dataType: 'json',
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data.file_name) {
                        // 上传代码返回结果之后，将图片插入到编辑器中
                        insert(data.file_name);
                    } else {
                        toastr.error(data.msg);
                    }
                }
            });
        })
    }
    editor.create()
    editor.txt.html(defaultValue)
}
function strToArr(str) {
    if (str) {
        return str.split(",");
    }
}

//全选和反选

$("#select-all").change(
    function () {
        if ($(this).is(":checked")) {
            $("[name='selected']").prop("checked", true);
        } else {
            $("[name='selected']").prop("checked", false);
        }
    }
)

//获取所有选中checkbox的值
function checkedValue() {
    var arr = new Array();
    $("input:checkbox[name='selected']:checked").each(function (i) {
        arr.push($(this).attr('id'))
    });
    return arr.join(',');
}
function showicon(obj) {
        icon = $(obj).siblings().children()
        icon.removeClass()
        icon.addClass("fa")
        icon.addClass(obj.value)
    }
function searchFun(obj){
    var search_key = $(obj).prev().val();
    window.location.href= '?search='+search_key;
}
//回车搜索
$('.search-data-input').bind('keydown', function (event) {
    var event = window.event || arguments.callee.caller.arguments[0];
    if (event.keyCode == 13){
        search_key = $('.search-data-input').val();
        window.location.href= '?search='+search_key;
    }
});
//点击按钮搜索
$('.search-data-btn').click(function () {
    search_key = $('.search-data-input').val();
    window.location.href= '?search='+search_key;
});