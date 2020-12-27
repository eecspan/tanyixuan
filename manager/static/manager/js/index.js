$(document).ready(
    function() {
        alert('欢迎来到管理者主页');

        $(".logout").click(function () {
            window.location.assign("/logout/");  // 退出登录
        });
    }
);