//shopping web

if (token = window.localStorage.getItem('dnblog_token')) {
        var username = window.localStorage.getItem('dnblog_user');
        var show = '';
            $.ajax({
                // 请求方式
                type:"get",
                // url
                url:"http://127.0.0.1:8000/v1/paycar"+'/'+ username,
                beforeSend: function(request) {
                    request.setRequestHeader("Authorization", token);
                },
                success:function (result) {
                    if (200 == result.code){
                $(document).ready(function() { 
                var products = result.data.car_pros;
                console.log(result);
                show+='<thead><tr>';
                show+='<th scope="col" class="col-2 col-md-2">圖片</th>';
                show+='<th scope="col" class="col-2 col-md-2">商品</th>';
                show+='<th scope="col" class="col-2 col-md-2">編碼</th>';
                show+='<th scope="col" class="col-2 col-md-2">單價</th>';
                show+='<th scope="col" class="col-1 col-md-1">數量</th>';
                show+='<th scope="col" class="col-1 col-md-1">總價</th>';
                show+='<th scope="col" class="col-2 col-md-2">移出</th>';
                show+='</tr></thead>';
                var all_price=0
                for(var c in products){
                console.log(c);
                var id = products[c].id;
                var avatar = products[c].avatar;
                var title = products[c].title;
                var sort = products[c].sort;
                var id_num = products[c].id_num;
                var price = products[c].price;
                var buy_amount = products[c].buy_amount;
                var total_price=buy_amount* price
                var avatar_url = 'http://127.0.0.1:8000/media/'+ avatar;
                show+='<tbody><tr>';
                show+='<th scope="row" class="col-2 col-md-2"><img src=' + avatar_url + ' alt=""></th>';
                show+='<td class="col-2 col-md-2">'+title +'</td>';
                show+='<td class="col-2 col-md-2">'+id_num+'</td>';
                show+='<td class="col-2 col-md-2">'+price+'</td>';
                show+='<td class="col-2 col-md-1" >'+buy_amount+'</td>';
                show+='<td class="col-2 col-md-1">'+total_price+'</td>';
                show+='<td class="col-2 col-md-2" style=" cursor: pointer;" data='+ id +'>';
                show+='<input  type="button" value="修改" onclick="change_amount(\''+ id +'\')"><input type="button" value="刪除" onclick="del(\''+ id +'\')">'
                show+='</td></tr>';
                all_price+=total_price
            }
                show+='<tbody><tr>';
                show+='<th scope="row" class="col-2 col-md-2" ><img src="" alt=""></th>';
                show+='<td class="col-2 col-md-2" ></td>';
                show+='<td class="col-2 col-md-2" ></td>';
                show+='<td class="col-2 col-md-2" ></td>';
                show+='<td class="col-2 col-md-2" ></td>';
                show+="<td class='col-2 col-md-2' >小計:";
                show+=all_price+"</td>";
                show+='<td class="" style=" cursor: pointer;" >';
                show+='<input type="button" value="結帳" onclick="payment()"></td></tr>'
                show+='</tbody></table>';
                $('#cart_pro').html(show);
                // 只是導入
                // loginOut();
                // change_amount();
                // del(id);
                // payment()

                }

                );
                }}
                })

    }else {
        alert("登入異常");
    }



//修改內容
function change_amount(id){
       
    alert('起動')
    var buy_amount=prompt('請輸入要修改數量',"")  
    console.log(typeof buy_amount)
    var change_data = {'id':id,'buy_amount':buy_amount}
    console.log(id,buy_amount)
    num=parseInt(buy_amount)
    if (buy_amount == 0){
      alert("不可為零");
    }else if(Number.isInteger(num)){
        $.ajax({
          type:"PUT",
          // contentType 
          contentType:"application/json",
          // dataType
          dataType:"json",
          // url
          url:"http://127.0.0.1:8000/v1/paycar"+'/'+ username,
          // 把JS的对象或数组序列化一个json 字符串
          data:JSON.stringify(change_data),
          beforeSend: function(request) {
        request.setRequestHeader("Authorization", token);
    },
          success:function (result) {
                          if (200 == result.code){
                             alert('親,改變購買數量囉');
                        
                            window.location.reload()                         
                          }else if (277 == result.code) {
                            alert('親,目前存貨數量是'+result.data.re_amount[0]);
                          } else {
                             alert('親,失败囉');
                          }
                      }

  })
    }else{
        alert("請輸入整數或者請聯絡官方客服")
      }
}

function loginOut(){

$('#login_out').on('click', function(){

    if(confirm("確定登出吗？")){
        window.localStorage.removeItem('dnblog_token');
        window.localStorage.removeItem('dnblog_user');
        window.location.href= '/new_index';
    }
}
)


        }


//移出購物商品
function del(id){

var delete_url = "http://127.0.0.1:8000/v1/paycar/"+ username + '/'+'del'+'/?did='+ id; 
if(confirm("確定移出吗？")){
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
    

} 

//購物車結帳
function payment(){

var delete_url = "http://127.0.0.1:8000/v1/paycar/"+ username + '/'+'del'+'/?did='+ 'buy'; 
if(confirm("確定結帳吗？結帳需要幾秒時間,請等待")){
$.ajax({
        // 请求方式
        type:"delete",
        url: delete_url,
        beforeSend: function(request) {
        request.setRequestHeader("Authorization", token);
        },
        success:function (result) {
            if (200 == result.code){

            alert('結帳成功');
            window.location.reload()
            

            }else if (400 == result.code) {

                alert('確認購買'+result.data.error_pro[0].title+
                '商品數量是否超出,目前存貨數量是'+result.data.error_pro[0].amount);
                
            }else if (600 == result.code) {

                alert('目前無商品可結帳');
                
            }else if (465 == result.code) {

                alert('目前郵件發送異常');
                
            } else {
                alert('結帳失敗,請聯絡官方');

                
            }
        }

    })

}
    

} 


//self_web_change
if (token = window.localStorage.getItem('dnblog_token')) {
    var username = window.localStorage.getItem('dnblog_user');
    var html_body = '';
    $.ajax({
       // 请求方式
       type:"get",
       beforeSend: function(request) {
           request.setRequestHeader("Authorization", token);
       },
       // url
       url:"http://127.0.0.1:8000/v1/users/"+ username,
       success:function (result) {
           if (200 == result.code){
               console.log(result);
                html_body+='<div  class="col-2 col-md-2" style="border:solid 1px #cee2df;">帳戶:</div>';
                html_body +='<div class="col-10 col-md-10" style="border:solid 1px #cee2df;">'+result.username+'</div>';
                html_body+='<div  class="col-2 col-md-2" style="border:solid 1px #cee2df;">email:</div>';
                html_body +='<div class="col-10 col-md-10" style="border:solid 1px #cee2df;">'+result.data.email+'</div>';
                html_body+='<div  class="col-2 col-md-2" style="border:solid 1px #cee2df;">電話:</div>';
                html_body +='<div class="col-10 col-md-10" style="border:solid 1px #cee2df;">'+result.data.phone+'</div>';
                html_body+='<div  class="col-2 col-md-2" style="border:solid 1px #cee2df;">地址:</div>';
                html_body +='<div class="col-10 col-md-10" style="border:solid 1px #cee2df;">'+result.data.address+'</div>';
                html_body+='<div  class="col-2 col-md-2" style="border:solid 1px #cee2df;">交易次數:</div>';
                html_body +='<div class="col-10 col-md-10" style="border:solid 1px #cee2df;">'+result.data.business_deal+'</div>';

                //

            //    html_body +='<div class="col-2 col-md-2" style="border:solid 1px #cee2df;">'+result.username+'</div>';
            //    html_body +='<div class="col-2 col-md-2" style="border:solid 1px #cee2df;">'+result.data.email+'</div>';
            //    html_body +='<div class="col-2 col-md-2" style="border:solid 1px #cee2df;">'+result.data.phone+'</div>';
            //    html_body +='<div class="col-3 col-md-3" style="border:solid 1px #cee2df;">'+result.data.address+'</div>';
            //    html_body +='<div class="col-2 col-md-2" style="border:solid 1px #cee2df;">'+result.data.business_deal+'</div>';
               html_body+='</div>';
               //



               html_body +='<div class="col-12 col-md-12" style="padding-left: 0px;"><div>'
               html_body +='<h3 style="margin-top: 20px; background-color:#000 ; color: #fff; text-align: center;">'
               html_body +='修改資訊</h3></div></div>';
               html_body +='<div class="body body col-12 col-md-10">';
               html_body +='<form action="http://127.0.0.1:5000/self" class="col-12 col-md-10">';
               html_body +='<div>修改郵箱<input type="email" class="form-control" name="email" id="email"   value="' + result.data.email + '"' + 'placeholder="輸入修改email"></div>';
               html_body +='<div>修改電話<input type="text" class="form-control" name="phone" id="phone"   value="' + result.data.phone + '"' + 'placeholder="輸入修改phone"></div>';
               html_body +='<div>修改地址<input type="text" class="form-control" name="address" id="address"  value="' + result.data.address + '"' + 'placeholder="輸入修改address"></div>';
               html_body +='<div align="center""><input type="button"  value="提交" onclick="changeInfo()"></div>';
               html_body +='</form></div>';
               $('#self_list').html(html_body);
               //初始化登出事件
               loginOut()
               }else{
                 alert(result.error)
                }
                }
                }
                );
            }
            


    function changeInfo(){
        var token = window.localStorage.getItem('dnblog_token');
        var username = window.localStorage.getItem('dnblog_user');
        // var email = document.getElementById("email");
        var email = $('#email').val()
        var phone = $('#phone').val()
        var address = $('#address').val()
        var post_data = {'email':email, 'phone':phone, 'address':address}

        $.ajax({
        // 请求方式
        type:"put",
        // contentType 
        contentType:"application/json",
        // dataType
        dataType:"json",
        // url
        url:"http://127.0.0.1:8000/v1/users/"+ username,
        // 把JS的对象或数组序列化一个json 字符串
        data:JSON.stringify(post_data),
        // result 为请求的返回结果对象
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success:function (result) {
            if (200 == result.code){
                alert("修改成功")
                refer_url = document.referrer
            //如果是项目内部的请求，回跳到上一步
            if (refer_url.search('127.0.0.1') != -1){

                window.location = refer_url;
            }


            }else{
                alert(result.error)
                window.location.href = '/new_index'
            }
           }
       });

    }
        