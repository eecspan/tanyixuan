
// 处理登录后返回的json数据
function dealLoginResponse(response)
{
    if (response.success == "true")
    {
        window.location.assign('/' + response.identity + "/index/")
    }
    else
    {
        // // 先把之前的提示删除
        // $("p.remind").remove();
        if (response.user_name_exists == "true")  // 如果用户账号存在，说明密码错了
            $("#password").after("<p class=\"remind\">密码错误！</p>");  
        else $("#user_name").after("<p class=\"remind\">账号不存在！</p>");
    }
}


function login()
{
    // 先把之前的提示删除
    $("p.remind").remove();

    var $user_name = $("#user_name").val().trim();  // 用户账号 去除首尾空格
    var $password = $('#password').val();  // 登录密码

    if ($user_name == "" || $password == "")
    {
        if ($user_name == "")
            $("#user_name").after("<p class=\"remind\">账号不能为空！</p>");
        if ($password == "")
            $("#password").after("<p class=\"remind\">密码不能为空！</p>");  
        return;
    }
    else
    {
        var $identity = $('input:radio[name=identity]:checked').val();  // 身份
        // 如果账号和密码都存在
        $.ajax({
            type: "POST",
            url: "/login/",
            data: {
                'identity': $identity,
                'user_name': $user_name,
                'password': $password,
            },
            dataType: "json",
            success: function (response) {
                dealLoginResponse(response);
            }
        });
    }
}


