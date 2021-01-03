function name_repeat()
{
    var $result = false;
    $market_name = $("#market-name").val();
    $.ajax({
        async: false,    //设置为同步
        type: "POST",
        url: "/manager/check-market-repeat/",
        data: {
            "market-name": $market_name
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
        alert("市场名称重复，请更换名称！");

    return $result;
}


$(document).ready(function () {

    // 退出登录按钮
    $("#logout").click(function () {
        window.location.assign("/logout/");  // 退出登录
    });

     // 更改地址，为了实现动态改变值时也触发input事件
     function changeAddress () {
         var $invalid = $("#market-address").next();
         console.log($("#market-address").val());
         if ($("#market-address").val() != "") {
             $invalid.attr("class", "invalid-feedback");
             $invalid.css("display", "none");
         } else {
             $invalid.attr("class", "invalid-feedback");
             $invalid.css("display", "");
         }
     }

    // 地图相关
    var map = new BMap.Map("allmap");
    var point = new BMap.Point(120.694774, 36.367384);//当前坐标经纬可改
    map.centerAndZoom(point,17);//显示级数越大越细
    map.addOverlay(new BMap.Marker(point));//定点坐标红点覆盖
    map.enableScrollWheelZoom(true);
    map.enableScrollWheelZoom(true);  //启用滚轮放大缩小，默认禁用
    map.enableDragging();             //启用地图拖拽，默认启用
    map.enableDoubleClickZoom();      //启用双击放大，默认启用
    map.addControl(new BMap.NavigationControl()); //平移缩放控件
    map.addControl(new BMap.ScaleControl());      //比例尺控件

    var geoc = new BMap.Geocoder();

    map.addEventListener("click", function(e) {
        //通过点击百度地图，可以获取到对应的point, 由point的lng、lat属性就可以获取对应的经度纬度
        var pt = e.point;
        map.clearOverlays();
        // map.removeOverlay;
        map.addOverlay(new BMap.Marker(pt));//定点坐标红点覆盖
        geoc.getLocation(pt, function (rs) {
            //addressComponents对象可以获取到详细的地址信息
            var addComp = rs.addressComponents;
            var site = addComp.province + addComp.city  + addComp.district + addComp.street  + addComp.streetNumber;
            //将对应的HTML元素设置值
            $("#market-address").val(site);

            changeAddress();  // 改变输入框的值

            $("#longitude").val(pt.lng);
            $("#latitude").val(pt.lat);
        });
    });

    // 当输入了市场名称，将提示信息删去
    $("#market-name").bind("input propertychange", function () {
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

    // 当输入了市场简介，就将提示信息删去
    $("#market-introduction").bind("input propertychange", function () {
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

    $("#market-address").bind("input", changeAddress);

    $("#market-capacity").bind("input propertychange", function () {
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

    $("#market-phone-number").bind("input propertychange", function () {
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
    var $marketPic = $("#market-pics");
    var $marketPicLabel = $marketPic.next();
    $marketPic.bind("input propertychange", function (e) {
        $fileLength = $marketPic.prop("files").length;
        if ($fileLength == 0)
            $marketPicLabel.html("选择一张或多张图片上传（未上传将使用默认图片）");
        else
        {
            $filename = "";
            for (let i = 0; i < $fileLength; ++i)
                $filename += (' ' + $marketPic.prop("files")[i].name);
            $marketPicLabel.html($filename);
        }
    });
});
