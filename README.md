##基本說明

<img src="https://github.com/henry8082/-Baha/blob/master/%E5%B7%B4%E5%93%88/1589874552743.jpg" width = "30%" />

-這是一個利用django設定line機器人並部署到heroku上，讓使用者在輸入@動漫通或@巴哈勇者福利社時候到各自的網站去爬蟲，並回傳結果。

-使用 heroku / django / line bot / requests / re(利用正則找網頁的內容)  / Flex Messages

<img src="https://github.com/henry8082/-Baha/blob/master/%E5%B7%B4%E5%93%88/S__63660095.jpg" width = "30%" /> <img src="https://github.com/henry8082/-Baha/blob/master/%E5%B7%B4%E5%93%88/S__63660096.jpg" width = "30%" />   
---------------------------------------

重要設定：
---------------------------------------

當linebot接收到字串後會至[invoiceapi](https://github.com/henry8082/-Baha/tree/master/invoiceapi)/**views.py** 中依使用者所輸入的字串來判斷會使用[
module](https://github.com/henry8082/-Baha/tree/master/module)/func.py中的哪一個funtion，之後便會執行不同的事件。

---------------------------------------

