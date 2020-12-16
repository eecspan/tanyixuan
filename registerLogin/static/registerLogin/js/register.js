function dealIdentity()
{
    var $identity = $('input:radio[name=identity]:checked').val();
    if ($identity == "consumer")
    {
        $('#name').hide();  // 隐藏真实姓名
        $('#name input').removeAttr("required");
        $('#id_number').hide();  
        $('#id_number input').removeAttr("required");
        $('#nickname').show();  // 展示昵称
        $('#nickname input').attr("required", "");
    }
    else 
    {
        $('#nickname').hide();  // 隐藏昵称
        $('#nickname input').removeAttr("required");
        $('#name').show();  // 展示真实姓名
        $('#name input').attr("required", "");
        $('#id_number').show();  
        $('#id_number input').attr("required", "");
    }
}


function dealRegisterResponse(response)
{
    if (response.success == "true")
    {
        alert("注册成功！请登录。");  // 提示，确认后跳转到登录页面
        window.location.assign("/login/");  // 注册成功跳转到登录页面
        return;
    }

    // 注册不成功
    if (response.user_name_exists == "true")
        $('#user_name input').after("<p class=\"remind\">用户名已存在！</p>");

    // 如果是管理者、摊主身份
    if (response.identity != "consumer")
    {
        if (response.id_number_exists == "true")
            $('#id_number input').after("<p class=\"remind\">身份证号已存在！</p>");
    }
    return;
}


// 用于注册时提交
function register()
{
    var $identity = $('input:radio[name=identity]:checked').val();  // 身份
    var $has_error = false;

    var $user_name = $('#user_name input').val().trim();
    var $phone_number = $('#phone_number input').val().trim();
    var $password = $('#password input').val().trim();
    var $password_confirm = $('#password-confirm input').val().trim();

    if ($user_name == "" || password == "")  // 直接結束
        return; 

    if ($identity == "consumer")  // 消费者身份
    {
        var $nickname = $('#nickname input').val().trim();
        if ($nickname == "")
            return;
    }
    else 
    {
        var $name = $('#name input').val().trim();
        var $id_number = $('#id_number input').val().trim();
        if ($name == "" || $id_number == "")
            return;
    }

    if ($password != $password_confirm)
    {
        $('#password-confirm input').after("<p class=\"remind\" >确认密码错误！</p>");
        $has_error = true;  // 有错误，不能提交
    }
    if ($phone_number != "" && (/^\d+$/.test($phone_number) == false))
    {
        $('#phone_number input').after("<p class=\"remind\">电话格式不正确！</p>");
        $has_error = true;  // 有错误，不能提交
    }
    
    if ($has_error == true)
        return;  // 直接结束函数

    // 没错误，就ajax提交
    $registerData = {
        'identity': $identity,
        'user_name': $user_name,
        'phone_number': $phone_number,
        'password': $password,
        'user_icon': "default_icon"
    };  // 要提交的数据
    
    if ($identity == "consumer")  // 消费者身份
        $registerData['nickname'] = $nickname;
    else 
    {
        $registerData['name'] = $name;
        $registerData['id_number'] = $id_number;
    }

    // ajax发送请求
    $.ajax({
        type: "POST",
        url: "/register/",
        data: $registerData,
        dataType: "json",
        success: function (response) {
            dealRegisterResponse(response);
        }
    });
}


// 当一切加载好，进行函数
$('document').ready(
    function()
    {
        // 这里是根据单选框动态更新注册内容
        dealIdentity();  // 先执行一次
        $('input:radio[name=identity]').click(
            dealIdentity
        );
        
        // 重新输入时，将提示信息删除
        $('#user_name input').click(
            function(){
                $('#phone_number p').remove();
            }
        );
        $('#id_number input').click(
            function(){
                $('#phone_number p').remove();
            }
        );
        $('#phone_number input').click(
            function(){
                $('#phone_number p').remove();
            }
        );
        $('#password-confirm input').click(
            function(){
                $('#password-confirm p').remove();
            }
        )
    }
)