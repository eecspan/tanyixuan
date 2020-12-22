// 获取摆摊地点信息，sortItem为排序依据，searchItem为搜索依据，
// pageNo为展示第几页，pageSize为每页的数量


var $pageSize = 10;  // 一页展示的个数
var $pageNo = 1;  // 当前页数
var $category_radio = 0;
var $category_item = "";
var $sort_btn = 0;
var $sort_item = "";
var $basis_btn = 0;
var $sort_basis = "asc";
var $search_item = "";

function get_market(pageNo, pageSize, sortItem="", category=$category_item, sortBasis="asc", searchItem="")
{
    var $request_data = {
        "pageNo": pageNo,
        "pageSize": pageSize,
        "sortItem": sortItem,
        "category": category,
        "sortBasis": sortBasis,
        "searchItem": searchItem,
    };
    $.ajax({
        type: "POST",
        url: "/seller/get-market/",
        traditional:true,
        data: $request_data,
        dataType: "json",
        success: function (response) {
            deal_market(response);
        }
    });
}


// 处理返回的摆摊地点信息，让其展示在页面中
function deal_market(response)
{
    if (response.success == "true")
    {
        // 删除原有的
        $(".market-list-scroll").empty();

        // 添加获取的
        $.each(response.marketList, function (indexInArray, market) { 
            var $marketHtml = 
                '<li id=\"' +market.id + '\">'+
                    '<div class="pic">' + 
                        '<a onclick="" target="_blank">' + 
                            '<img src=\"' + market.pic_url+ '\" alt=\"' + market.name + ' \">' + 
                        '</a>' +
                    '</div>' +
                    '<div class="txt">' +
                        '<div class="tit">' +
                            '<a onclick="" target="_blank">' +
                                '<h4>'+market.name+'</h4>' +
                            '</a>' +
                        '</div>' +
                        '<div class="comment">' +
                            '<div class="nebula_star">' +
                                '<div class="star_icon">' +
                                    '<span class="star star_full"></span>' +
                                    '<span class="star star_full"></span>' +
                                    '<span class="star star_full"></span>' +
                                    '<span class="star star_full"></span>' +
                                    '<span class="star star_half"></span>' +
                                '</div>' +
                                '<div class="star_score">'+market.mark+'</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="tag">简要介绍' +
                            '<em class="sep">|</em>' +
                            '<span class="tag-intro">'+market.introduction+'</span>' +
                        '</div>' +
                        '<div class="tag">具体地址' +
                            '<em class="sep">|</em>' +
                            '<span class="tag-addr">'+market.address+'</span>' +
                        '</div>' +
                        '<div class="tag">联系方式' +
                            '<em class="sep">|</em>' +
                            '<span class="tag-phone">'+market.phone_number+'</span>' +
                        '</div>' +
                    '</div>' +
                    '<div class="right-txt">' +
                        '<div class="tag">摊位容量' +
                            '<em class="sep">|</em>' +
                            '<span class="tag-capacity tag-serious">'+market.current_capacity+'</span>' +
                            '<i class="percent">/</i>' +
                            '<span class="tag-capacity tag-serious">'+market.capacity+'</span>' +
                        '<div class="tag">经营类别' +
                            '<em class="sep">|</em>' +
                            '<span class="tag-category">' +market.category+'</span>' +
                        '</div>' +
                    '</div>' +
                '</li>';
            $(".market-list-scroll").append($marketHtml);
        });

        // 点击摆摊地点时，进入详情页面  要在这里添加函数
        // 通过url传递market_id信息
        $(".market-list-scroll li").click(function () {
            var $market_id = $(this).attr("id");
            alert("点击了" + $market_id);
            window.location.assign("/seller/market-detail/" + $market_id + '/');
        });
    }

    // 如果已经没有数据
    else
    {
        // 如果是下一页，页数应减1
        if ($pageNo > 1)
            $pageNo -= 1;

        setTimeout(() => {
            alert("已加载全部数据！");
        }, 500);
    }

    // 显示页码
    $("#current-page").html($pageNo);
}


function sort_by_dis(position)
{
    var $latitude = position.coords.latitude;
    var $longtitude = position.coords.longitude;

    // 排序依据为经纬度
    $sort_item = [$latitude, $longtitude];
    get_market($pageNo, $pageSize, $sort_item, $category_item, $sort_basis);  // 地理排序
}

$(document).ready(
    function()
    {   
        $(".logout").click(function () { 
            window.location.assign("/logout/");  // 退出登录
        });

        get_market($pageNo, $pageSize);  // 第一次请求数据，默认排序

        // 弹出欢迎
        setTimeout(() => {
            alert($name + '，欢迎来到摊主主页');
        }, 500);


        // 根据分类栏得到特定类别的摆摊地点
        var $category_radios = $(".category-radio .btn");
        $.each($category_radios, function (index, radio) {
            $(radio).click(function (e) { 
                e.preventDefault();
                // 将选中的那个取消选中
                if (index != $category_radio)
                {
                    $category_radios.eq($category_radio).removeClass("active");
                    $category_radio = index;
                    $(radio).addClass("active");
                    
                    // 更改分类item
                    if (index == 0)
                        $category_item = "";
                    else $category_item = $(radio).html().trim();

                    // 重新设置pageNo！！！！！
                    $pageNo = 1;

                    // 重新加载摆摊地点
                    get_market($pageNo, $pageSize, $sort_item, $category_item, $sort_basis, $search_item);
                }
            });
        });

        // 根据排序依据得到摆摊地点
        var $sort_btns = $(".sort-btns button");
        $.each($sort_btns, function (index, btn) {
            $(btn).click(function (e) {
                e.preventDefault();
                // 将选中的那个取消选中
                if (index != $sort_btn)
                {
                    $sort_btns.eq($sort_btn).removeClass("bg-warning");
                    $sort_btn = index;
                    $(btn).addClass("bg-warning");

                    // 重新加载摆摊地点
                    if (index == 1)
                    {
                        if (navigator.geolocation)
                        {
                            navigator.geolocation.getCurrentPosition(sort_by_dis);
                        }
                        else // 浏览器不支持定位
                            alert("浏览器不支持定位！");
                    }
                    else{
                        if (index == 2)
                            $sort_item = "mark";
                        else
                            $sort_item = "";
                        get_market($pageNo, $pageSize, $sort_item, $category_item, $sort_basis, $search_item);  // 评分或者默认排序
                    }
                }
            });
        });


        // 选择升序或者降序
        var $basis_btns = $(".basis-btns button");
        $.each($basis_btns, function (index, btn) {
            $(btn).click(function (e) {
                e.preventDefault();

                // 如果选中的是新的
                if (index != $basis_btn)
                {
                    $basis_btns.eq($basis_btn).removeClass("bg-warning");
                    $basis_btn = index;
                    $(btn).addClass("bg-warning");

                    // 重新设置pageNo！！！！！！
                    $pageNo = 1;

                    //  重新申请
                    if (index == 0)
                        $sort_basis = "asc";
                    else $sort_basis = "desc";

                    get_market($pageNo, $pageSize, $sort_item, $category_item, $sort_basis, $search_item);
                }
            });
        });

        // 点击搜索，根据字符串搜索得到名称符合的摊铺
        $("#search-btn").click(() => {
            $search_item = $("#search-item").val().trim();

            // 重新设置pageNo！！！！！！
            $pageNo = 1;

            get_market($pageNo, $pageSize, $sort_item, $category_item, $sort_basis, $search_item,);
        });

        // 点击下一页和上一页，能够跳转，并且显示最新页码
        $("#next-page").click(() => {
           $pageNo += 1;  // 页数 += 1
            // 获取新数据并展示
            get_market($pageNo, $pageSize, $sort_item, $category_item, $sort_basis, $search_item);
        });

        $("#pre-page").click(() => {
            // 如果已经是第1页
            if ($pageNo == 1)
                alert("已经是第一页了！");
            else{
                $pageNo -= 1;  // 页数 -= 1
            // 获取新数据并展示
            get_market($pageNo, $pageSize, $sort_item, $category_item, $sort_basis, $search_item);
            }
        });
    }
);