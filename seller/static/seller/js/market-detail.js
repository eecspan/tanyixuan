$(document).ready(function () {

    // 退出登录按钮
    $(".logout").click(function () { 
        window.location.assign("/logout/");  // 退出登录
    });

    $("#start-booth").click( ()=>{ 
        // 跳转到我的摊位页面
        window.location.assign("/seller/start-business/");
    });
});