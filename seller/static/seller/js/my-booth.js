

$(document).ready(function () {

    // 退出登录按钮
    $("#logout").click(function () { 
        window.location.assign("/logout/");  // 退出登录
    });

    // 添加摊铺按钮
    $("#create-booth").click(function () {
        window.location.assign("/seller/create-booth/");
    });

    // 当点击停止营业按钮
    $(".btn-close").click(function (e) { 
        e.preventDefault();
        // 摊铺所在摆摊地点id
        var $market_id = $(this).attr("id");
        // 摊铺名称
        var $booth_name = $(this).parents(".card-body").find(".booth-name").html();
        // 发送请求
        $.ajax({
            type: "POST",
            url: "/seller/close-booth/",
            data: {
                "market_id": $market_id,
                "booth_name": $booth_name,
            },
            dataType: "json",
            success: function (response) {
                if (response.success == "true")
                {
                    // 重新加载
                    window.location.reload();
                }
                else alert("再试一次！");
            }
        });    
    });

    // 当点击开始营业按钮
    $(".btn-open").click(function (e) { 
        e.preventDefault();
    
        // 如果还没有选择要在哪摆摊，那么返回主页
        if ($market_id == 0 || $market_id == undefined)
        {
            alert("请先选择要摆摊的地点！");
            window.location.assign("/seller/index/");
        }
        else
        {
            // 摊铺名称
            var $booth_name = $(this).parents(".card-body").find(".booth-name").html(); 
            // 发送请求
            $.ajax({
                type: "POST",
                url: "/seller/open-booth/",
                data: {
                    "market_id": $market_id,
                    "booth_name": $booth_name,
                },
                dataType: "json",
                success: function (response) {
                    if (response.success == "true")
                    {
                        // 重新加载
                        window.location.reload();
                    }
                    else alert("开始营业未成功，再试一次！");
                }
            });    
        }
    });

    // 点击删除摊铺按钮
    $(".btn-delete").click(function() {
        var $booth_name = $(this).parents(".card-body").find(".booth-name").html(); 
        // 发送请求
        $.ajax({
            type: "POST",
            url: "/seller/delete-booth/",
            data: {
                "booth_name": $booth_name,
            },
            dataType: "json",
            success: function (response) {
                if (response.success == "true")
                {
                    // 重新加载
                    window.location.reload();
                }
                else alert("删除未成功，再试一次！");
            }
        });    
    });
});