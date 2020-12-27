function name_repeat()
{
    var $result = false;
    $booth_name = $("#booth-name").val();
    $.ajax({
        async: false,    //设置为同步
        type: "POST",
        url: "/seller/check-booth-reapeat/",
        data: {
            "booth-name": $booth_name
        },
        dataType: "json",
        success: function (response) {
            if (response.success == "true")
                $result = true;
            else 
                $result =  false;
        }
    });
    if ($result == false)
        alert("摊铺名称重复，请更换名称！");
    
    return $result; 
}


$(document).ready(function () {

    // 退出登录按钮
    $("#logout").click(function () { 
        window.location.assign("/logout/");  // 退出登录
    });

    // 当输入了摊铺名称，将提示信息删去
    $("#booth-name").bind("input propertychange", function () {
        var $invalid =  $(this).parents(".mb-3").children(".invalid-feedback");
        if ($(this).val() != "") {
            $invalid.css("display", "none");
        }
        else
        {
            $invalid.css("display", "");
        }
    });

    // 当选择了一个checkbox，就将提示信息删去
    var $checkBoxes = $(":checkbox");
    $.each($checkBoxes, function (indexInArray, checkBox) { 
        $(checkBox).change(function (e) { 
            e.preventDefault();

            // 如果被选中了  // 将每个checkbox取消required
            // 并且将最后的警示取消
            if ($(checkBox).prop("checked"))
            {
                // console.log("选中了！");
                // 移除required属性 
                $.each($checkBoxes, function (indexInArray, checkBox) { 
                    $(checkBox).removeAttr("required");
                });
            }
            // 如果取消了 那么看看是不是都取消了
            else
            {
                var $allInvalid = true;
                $.each($checkBoxes, function (indexInArray, checkBox) {
                    // 如果还有选中的，直接中止函数 
                    if ($(checkBox).prop("checked"))
                    {
                        $allInvalid = false;
                        return;
                    }
                });
                // 如果还有选中的
                if (!$allInvalid)
                    return;
                // 如果都取消了
                // console.log("都取消了");
                $.each($checkBoxes, function (indexInArray, checkBox) { 
                    $(checkBox).attr("required", true);
                });
            }
        });
    });

    // 当输入了摊铺简介，就将提示信息删去
    $("#booth-introduction").bind("input propertychange", function () {
        var $invalid = $(this).next();
        if ($(this).val() != "") {
            $invalid.attr("class", "invalid-feedback");
            $invalid.css("display", "none");
        }
        else
        {
            $invalid.attr("class", "invalid-feedback");
            $invalid.css("display", "");
        }
    });

    // 如果选择了图片，显示图片路径
    var $boothPic = $("#booth-pics");
    var $boothPicLabel = $boothPic.next();
    $boothPic.bind("input propertychange", function (e) {
        $fileLength = $boothPic.prop("files").length;
        if ($fileLength == 0)
            $boothPicLabel.html("选择一张或多张图片上传（未上传将使用默认图片）");
        else
        {
            $filename = "";
            for (let i = 0; i < $fileLength; ++i)
                $filename += (' ' + $boothPic.prop("files")[i].name);
            $boothPicLabel.html($filename);
        } 
    });
});
