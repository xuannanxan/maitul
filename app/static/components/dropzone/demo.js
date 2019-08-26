

function initImageUpload(element,maxFiles=1,extData,hadfile){
    
    var myDropzone = new Dropzone(element, {
        url: "/Public/set_dropzone_image",//上传文件的地址，
        maxFiles: maxFiles,//最多上传几个图片
        params:extData,
        maxFilesize: 5,//图片的大小，单位是M
        addRemoveLinks:true,//是否有删除图片的功能
        dictRemoveFile:"",//删除图片的文字
        acceptedFiles: "image/*",//支持的格式
        paramName:'dropimage',//上传的FILE名称，即服务端可以通过此来获取上传的图片，如$_FILES['dropimage']
        dictDefaultMessage:"拖拽文件到这里或者选择文件上传...",
        dictInvalidFileType:"格式错误,请上传图片...",
        dictResponseError:"服务器连接失败...",
        dictMaxFilesExceeded:"不能上传这么多...",
        dictRemoveFile:"删除文件",
    });
        if (hadfile){
            initImageShow(myDropzone,hadfile)
        }
        myDropzone.on("success", function(file) {
            console.log("File " + file.name + "uploaded");
        });
        myDropzone.on("removedfile", function(file) {
            console.log("File " + file.name + "removed");
        });
    
}
// 编辑时显示已有数据
function initImageShow(dz,info) {
    if( info=='' || !info ) return false;
    var info_array = info.split(",");
    for( var i in info_array )
    {
        var hidefileval_str = info_array[i];
        var hidefileval_arr = hidefileval_str.split("/");
        var mockfile_object = { name: hidefileval_arr[hidefileval_arr.length-1], accepted:true }
        dz.emit('addedfile', mockfile_object);
        dz.emit('thumbnail', mockfile_object, hidefileval_str);
        dz.emit('success', mockfile_object);
        dz.emit('processing', mockfile_object);
        dz.emit('complete', mockfile_object);
        dz.files.push( mockfile_object );
        mockfile_object = null;
    }
}