// 获取摆摊地点信息，sortItem为排序依据，searchItem为搜索依据，
// pageNo为展示第几页，pageSize为每页的数量


var $pageSize = 10;  // 一页展示的个数
var $pageNo = 1;  // 当前也数

function get_market(pageNo, pageSize, sortItem="", category="", searchItem="", )
{
    var $request_data = {
        "pageNo": pageNo,
        "pageSize": pageSize,
        "sortItem": sortItem,
        "category": category,
        "searchItem": searchItem,
    }
    $.ajax({
        type: "POST",
        url: "/seller/get-market/",
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
                                '<div class="star_score">4.71</div>' +
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
                            '<span class="tag-capacity tag-serious">'+(market.capacity - market.current_capacity)+'</span>' +
                            '<i class="percent">/</i>' +
                            '<span class="tag-capacity tag-serious">'+market.capacity+'</span>' +
                        '<div class="tag">经营类别' +
                            '<em class="sep">|</em>' +
                            '<span class="tag-category">美食、果蔬</span>' +
                        '</div>' +
                    '</div>' +
                '</li>';
            $(".market-list-scroll").append($marketHtml);
        });

        // 点击摆摊地点时，进入详情页面  要在这里添加函数
        $(".market-list-scroll li").click(function () {
            var $market_id = $(this).attr("id");
            alert("点击了" + $market_id);
            window.location.assign("/seller/market-detail/" + $market_id + '/');
        }
    );
    }
}


$(document).ready(
    function()
    {   
        $(".logout").click(function () { 
            window.location.assign("/logout/");  // 退出登录
        });

        get_market($pageNo, $pageSize, "dis", "", "");  // 第一次请求数据，默认排序

        // 弹出欢迎
        setTimeout(() => {
            alert($name + '，欢迎来到摊主主页');
        }, 500);
    }
);