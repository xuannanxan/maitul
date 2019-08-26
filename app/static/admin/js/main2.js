/**
 * Created by xuannan on 2019-03-23.
 */
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
        var index = arr.indexOf(file.name);
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