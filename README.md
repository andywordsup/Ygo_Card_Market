＃ 卡牌商城

####項目介紹
1.這是一個卡牌商品交易平台，也可以稱為卡牌商城；
2.授權的用戶可上傳自己商品【商品訊息和照片】；
3.用戶或遊客可以點選分類區的編號查看所要商品；
4.部分功能只有登錄後才能使用如自身商品的管理，商品的發布，編輯等；
5.購買後有發送email提醒功能

####技術路線

>項目是基於python的Django框架開發的，Django是一個開源的Web應用框架，由Python寫成，採用了MVC的框架模式； Django的主要目的是替代，快速的開發數據庫驅動的網站，擴展代碼嵌入，多個組件可以很方便的以“插件”形式服務於整個框架，Django自帶orm，模板渲染引擎及簡單的後台管理功能。
項目使用傳統的關係型數據庫mysql做數據的存儲，數據庫設計方面分為四張表，分別是用戶表，商品表，購物車，商品購買表以及表與表之間的關聯。

前端CSS,JS,HTML已Flask跟Django的管理做區分,達到模擬前後端分離樣式,在管理上做區分也比較清楚。界面展示使用bootstrap框架，整個系統的實現功能模塊主要有：用戶的註冊與登錄，商品的發布與管理，所有商品的瀏覽，不同商品對應的詳情信息展示，用戶的購買行為以及帳號交易次數的查詢等。