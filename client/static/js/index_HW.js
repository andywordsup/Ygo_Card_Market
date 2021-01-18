//login check
function login_check(){
    console.log('into index.HW login_check()')
    token = window.localStorage.getItem('dnblog_token')
    username = window.localStorage.getItem('dnblog_user')
    if (token ==null) {
        var show = "";
        show+='<a class="nav-link" href="#amos-block" data-toggle="modal">Login <span class="sr-only">(current)</span></a>'
        $('#login_check').html(show);
        var reg="";
        reg+='<a class="nav-link" href="/register">register</a>'
        $('#reg').html(reg);
       
    }else if(username ==null) {
        var show = "";
        show+='<a class="nav-link" href="#amos-block" data-toggle="modal">Login <span class="sr-only">(current)</span></a>'
        $('#login_check').html(show);  
    }else{ 
        var show = "";
        show+='<a class="nav-link" id="login_out" data-toggle="modal">loginOut <span class="sr-only">(current)</span></a>'

        $('#login_check').html(show);
        //登出
        $('#login_out').on('click', function(){

            if(confirm("親,確定登出吗？")){
                window.localStorage.removeItem('dnblog_token');
                window.localStorage.removeItem('dnblog_user');
                window.location =  '/new_index';
  
                 }
              }
            )
        //打開上架視窗
    }
}



// 加載此商品類型原本加載的其餘所有商品
function add_other_goods(){
    $.ajax({
        // 请求方式
        type:"get",
        // url
        url:"http://127.0.0.1:8000/v1/products/root",
        // beforeSend: function(request) {
        //     request.setRequestHeader("Authorization", token);}, 
            success:function (result){//
            if (200 == result.code){
            $(document).ready(function() {

            var products = result.data.products
            console.log('into index.HW function add_other_goods()')
            var show = "";
            for(var p in products){
                var id= products[p].id;
                var avatar = products[p].avatar;
                var title = products[p].title;
                var sort = products[p].sort;
                var id_num = products[p].id_num;
                var price = products[p].price;
                var amount = products[p].amount;
                var avatar_url = 'http://127.0.0.1:8000/media/'+ avatar;
            show+="<div class='col-10 col-md-2'>"
            show+="<div style='background:#e7dfcc; padding: 8px; margin-bottom:15px;'>"
            show+='<img src="' + avatar_url + ' " alt="" " class="img-fluid">'
            // show+='<h1>title</h1>'
            show+='<div class="txt1"  style="font-size:smaller; color:#b1672f;" value="'+ products[p].title +'" id_pro="'+ products[p].id+'">'
            show+=''+ products[p].title +'</div>'
            show+='<div class="txt2" value="'+ products[p].id_num +'" id_pro="'+ products[p].id +'">編號:'
            show+=''+ products[p].id_num +'</div>'
            show+='<div class="txt3"  style="font-size: 12px;" value="'+ products[p].amount +'"  id_pro="'+ products[p].id +'">數量:'
            show+=''+ products[p].amount +'</div><div class="txt4"  style="font-size: 12px;" value="'+ products[p].price +'" id_pro="'+ products[p].id +'">價格:'
            show+=''+ products[p].price +'</div>'
            show+='<button style="text-align:center" value="'+ products[p].id_num +'" style="font-size:smaller;" class="buy" onclick="intocar(\''+ products[p].id +'\')">加入購物車</button>'
            show+='</div></div>'
            show+=''
            show+=''
            show+=''
            show+=''
            show+=''
            show+=''
            show+=''
            }
            show+=''
            show+=''
           // 將文本轉換為標籤加入元素節點
           $('#goods_list').html(show);

                })
            }
        }
        //success後內容
    })
    //.ajax

   	
}


//登入
function login(){
var username = $('.username').val()
var password = $('.password').val()
var post_data = {'username':username, 'password':password }

    $.ajax({
    // 方式
    type:"post",
    // contentType 
    contentType:"application/json",
    // dataType
    dataType:"json",
    // url
    url:"http://127.0.0.1:8000/v1/tokens",
    // url:"http://127.0.0.1:8000/test/",
    // 把JS的對像或數組序列化一個json 字符串
    //JSON.stringify函式將一個JavaScript物件轉換成文字化的JSON
    data:JSON.stringify(post_data),
    // result 為請求的返回結果對象
    success:function (result) {
        if (200 == result.code){
            window.localStorage.setItem('dnblog_token', result.data.token)
            window.localStorage.setItem('dnblog_user', result.username)
            alert('登入成功')
            refer_url = document.referrer
            //如果是项目内部的请求，回跳到上一步
            if (refer_url.search('127.0.0.1') != -1){

                window.location = refer_url;

            }else{
               product2_url='/' + username + '/' + 'new_del_pro'
               change_self_url='/' + username + '/' + 'self'
               paycar_url='/' + username + '/' + 'new_paycar'
              window.location ='/new_index';
            }

        }else{
            alert(result.error)
        }
    }
    });

    }
//登出
$('#login_out').on('click', function(){

            if(confirm("親,確定登出吗？")){
                window.localStorage.removeItem('dnblog_token');
                window.localStorage.removeItem('dnblog_user');
                window.location =  '/new_index';

            }
        }
)

//打開上架視窗
$('#up_pro').click(function(){
    $('.full-screen').toggle();
    $('.full-screen').css('display','flex');

})

//關閉上架商品畫面
$('.btn-close').click(function(){
    $('.full-screen').hide();
})


//加入商品項目至購物車
function intocar(id){
    token = window.localStorage.getItem('dnblog_token')
    console.log(token)
    username = window.localStorage.getItem('dnblog_user')
    if(token ==null){
        alert("請登入會員")
    }else{
        var array=[];
        var amount;
        var title;
        var id_num;
        var index;
        var id = id 
        $('.txt4').each(function(i){
          if($(this).attr('id_pro')==id){
            index=i;
            console.log(index)
          }
        })
        var price = $('.txt4').eq(index).text();
        //
        $('.txt3').each(function(i){
          if($(this).attr('id_pro')==id){
            index=i;
            console.log(index)
          }
        })
        var amount = $('.txt3').eq(index).text();
        //
        $('.txt2').each(function(i){
          if($(this).attr('id_pro')==id){
            index=i;
            console.log(index)
          }
        })
        var id_num = $('.txt2').eq(index).text();
        //
        $('.txt1').each(function(i){
          if($(this).attr('id_pro')==id){
            index=i;
            console.log(index)
          }
        })
        var title = $('.txt1').eq(index).text();
        //
        console.log(title,amount,price,id_num)
    
    
      //
        var amount=amount.split(':')[1].toString()
        // var title=title.split(':')[1].toString()
        var id_num=id_num.split(':')[1].toString()
        var price=price.split(':')[1].toString()
    
        console.log(title)
        console.log(id_num)
        console.log(amount)
        var paycar_data = {'id':id, 'id_num':id_num, 'title':title, 'amount':amount,'price':price}
        
        if (amount == '1000'){
          alert("傻逼,超出數量");
        }
        else if (amount!="0"){
    
            $.ajax({
              type:"post",
              // contentType 
              contentType:"application/json",
              // dataType
              dataType:"json",
              // url
              url:"http://127.0.0.1:8000/v1/paycar"+'/'+ username,
              // 把JS的对象或数组序列化一个json 字符串
              data:JSON.stringify(paycar_data),
              
              beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
              success:function (result) {
                              if (200 == result.code){
                                 alert('親,已加入購物車');
                              }else{
                                 alert('親,失败囉,選取數量超過');
                              }
                          }
    
      })
        }else{
            alert("傻逼,商品售完囉")
          }
    }
    
    }

//切換商品類別
function choice(sort){
    var sort_url = "http://127.0.0.1:8000/v1/choice/?get_sort="+ sort;
    $.ajax({
      type:"GET",
      url: sort_url,
    //   beforeSend: function(request) {
    //       request.setRequestHeader("Authorization", token);
    //   },
      success:function (result) {
                            if (200 == result.code){
                               console.log('切換成功');
                               $(document).ready(function() {
                                var products = result.data.products
                                console.log('into index.HW function add_other_goods()')
                                var show = "";
                                for(var p in products){
                                    var id= products[p].id;
                                    var avatar = products[p].avatar;
                                    var title = products[p].title;
                                    var sort = products[p].sort;
                                    var id_num = products[p].id_num;
                                    var price = products[p].price;
                                    var amount = products[p].amount;
                                    var avatar_url = 'http://127.0.0.1:8000/media/'+ avatar;
                                show+="<div class='col-10 col-md-2'>"
                                show+="<div class='good'style='background:#e7dfcc; padding: 8px; margin-bottom:15px;'>"
                                show+='<img src="' + avatar_url + ' " alt="" " class="img-fluid">'
                                // show+='<h1>title</h1>'
                                show+='<div class="txt1"  style="font-size:smaller; color:#b1672f;" value="'+ products[p].title +'" id_pro="'+ products[p].id+'">'
                                show+=''+ products[p].title +'</div>'
                                show+='<div class="txt2" value="'+ products[p].id_num +'" id_pro="'+ products[p].id +'">編號:'
                                show+=''+ products[p].id_num +'</div>'
                                show+='<div class="txt3"  style="font-size: 12px;" value="'+ products[p].amount +'"  id_pro="'+ products[p].id +'">數量:'
                                show+=''+ products[p].amount +'</div><div class="txt4"  style="font-size: 12px;" value="'+ products[p].price +'" id_pro="'+ products[p].id +'">價格:'
                                show+=''+ products[p].price +'</div>'
                                show+='<button style="text-align:center" value="'+ products[p].id_num +'" style="font-size:smaller;" class="buy" onclick="intocar(\''+ products[p].id +'\')">加入購物車</button>'
                                show+='</div></div>'
                                show+=''
                                show+=''
                                }
                                show+=''
                                show+=''
                               // 將文本轉換為標籤加入元素節點
                               $('#goods_list').html(show);
                            })
                            }else{
                               alert('切換失败');
                            }
                        }
    })
  }


//上架功能
  function product(){
    token = window.localStorage.getItem('dnblog_token');
    username = window.localStorage.getItem('dnblog_user');
    aurl=location.href+'/'+username
    if(token==null){
      alert("請登入會員")
    }else{
    formdata = new FormData();
    formdata.append("avatar",$("#avatar")[0].files[0]);
    var sort=$('#cars :selected').val()
    var title = $('.title').val()
    var id_num = $('.id_num').val()
    var price = $('.price').val()
    var amount = $('.amount').val()
    var pwd = $('.pwd').val() 
    var post_data = {'aurl':aurl,'title':title, 'id_num':id_num,'price':price,'amount':amount,'sort':sort,'pwd':pwd}
    // 把JS的对象或数组序列化一个json 字符串
    //JSON.stringify函式將一個JavaScript物件轉換成文字化的JSON
    var fdata=JSON.stringify(post_data);
    formdata.append('data',fdata);
    if(confirm("確定送出?在檢查一下吧?")){
      $.ajax({
                data:formdata,
                processData: false,
                contentType: false,
              type:"post",
              url:"http://127.0.0.1:8000/v1/products"+'/'+ username + '/avatar',
              beforeSend: function(request) {
                      request.setRequestHeader("Authorization", token);
                  },
              // result 为请求的返回结果对象
              success:function (result) {
                  if (200 == result.code){

                      alert('上傳成功')
                      refer_url = document.referrer
                      // 如果是项目内部的请求，回跳到上一步
                      if (refer_url.search('127.0.0.1') != -1){

                          window.location = "/new_index";

                      }

                  }else{
                      alert(result.error)
                  }
              }
              });
        }

} }







$(function(){
    console.log('into index.HW jq $funtion()')
    login_check();
	  add_other_goods();
   
});




   
    


