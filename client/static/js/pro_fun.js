
// del_pros
    token = window.localStorage.getItem('dnblog_token')
    username = window.localStorage.getItem('dnblog_user')
    show=''
$.ajax({
        // 请求方式
        type:"get",
        // url
        url:"http://127.0.0.1:8000/v1/products"+'/'+ username+'/'+'del',
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success:function (result) {
            if (200 == result.code){
        $(document).ready(function() { 
        if (token = window.localStorage.getItem('dnblog_token')) {
        username = window.localStorage.getItem('dnblog_user');
        var products = result.data.products
        show+='<thead><tr>';
        show+='<th scope="col"class="col-2 col-md-2">圖片</th>';
        show+='<th scope="col" class="col-2 col-md-2">商品</th>';
        show+='<th scope="col" class="col-2 col-md-2">編碼</th>';
        show+='<th scope="col" class="col-2 col-md-2">單價</th>';
        show+='<th scope="col" class="col-2 col-md-2">屯貨</th>';
        // show+='<th scope="col">數量修改</th>';
        show+='<th scope="col" class="col-2 col-md-2">刪除</th>';
        show+='</tr></thead>';
        for(var p in products){
        var id = products[p].id;
        var avatar = products[p].avatar;
        var title = products[p].title;
        var sort = products[p].sort;
        var id_num = products[p].id_num;
        var price = products[p].price;
        var amount = products[p].amount;
        var avatar_url = 'http://127.0.0.1:8000/media/'+ avatar;
        show+='<tbody><tr;>';
        show+='<th scope="row" class="col-2 col-md-2"><img src=' + avatar_url + ' alt=""></th>';
        show+='<td class="col-2 col-md-2">'+title +'</td>';
        show+='<td class="col-2 col-md-2">'+id_num+'</td>';
        show+='<td class="col-2 col-md-2">'+price+'</td>';
        show+='<td class="col-2 col-md-2">'+amount+'</td>';
        // show+='<td class="delete" style=" cursor: pointer;" data='+ products[p].id +'>點擊編輯</td>';
        show+='<td id="delete" class="col-2 col-md-2" style=" cursor: pointer;" data='+ products[p].id +'>下架</td>';
        show+='</tr></tbody>';
        }
    }else {
    alert("登入異常")
    }
    $('#tab').html(show);
    // 只是導入
    loginOut();
    }

    );
    }}
})


function loginOut(){

$('#login_out').on('click', function(){

        if(confirm("確定登出吗？")){
            window.localStorage.removeItem('dnblog_token');
            window.localStorage.removeItem('dnblog_user');
            window.location.href= '/new_index';
        }
    }
)

$('#delete').on('click', function(){
    
                    var delete_id = $(this).attr('data');
                    var delete_url = "http://127.0.0.1:8000/v1/products/"+ username + '/'+'del'+'/?did='+ delete_id; 
                    if(confirm("親,確定下架商品吗？")){
                    $.ajax({
                            // 请求方式
                            type:"delete",
                            url: delete_url,
                            beforeSend: function(request) {
                                request.setRequestHeader("Authorization", token);
                            },
                            success:function (result) {
                                if (200 == result.code){

                                alert('删除成功');
                                window.location.reload()

                                }else{

                                alert('删除失败');

                                }
                            }

                        })
           
        }
                    

                });
            
            
            
            
            }
