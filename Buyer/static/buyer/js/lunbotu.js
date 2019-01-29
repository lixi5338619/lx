window.onload = function () {
     /*相框元素*/
    var vis = document.getElementsByClassName('visible')[0];
    var yuans = document.querySelectorAll('.circles span');
    console.log(yuans);
    /*照片墙*/
    var pic_box = document.getElementsByClassName('pic_box')[0];
    var prev = document.getElementById('prev');
    var next = document.getElementById('next');
    /*指示小圆点的下标  */
    var index = 0 ;
    /*定义函数控制图片移动*/
    function ani(offset) {
         console.log(pic_box.style.left);//0
         var newLeft = parseInt(pic_box.style.left)+offset ;
         /*出去4张*/
         if(newLeft<-2360){
             newLeft = 0;
         }
         if(newLeft>0){
             newLeft = -2360;
         }
         pic_box.style.left = newLeft + 'px';


    }
   next.onclick = function () {
        /*右箭头  传入 -590*/
       ani(-590);
       index++; //1
       if(index===5){
           index = 0;

       }
       buttonShow();

   }
    prev.onclick = function () {
        index--;
        if(index===-1){
            index = 4;

        }
        /*右箭头  传入 -590*/
        ani(590);
        buttonShow();

    }
    /*自动轮播  加定时器*/
    var timer ; //全局变量
    function play() {
        timer = setInterval(function () {
            next.onclick();


            /*小圆点 */
        },1000);

    }
    play();


    /*鼠标移入图片切换  鼠标图片停止切换 ====》清除定时器*/
    vis.onmouseenter = function () {
        clearInterval(timer);
    };
    vis.onmouseleave = function () {
        play();
    };

    /*小圆点的切换函数*/

    function buttonShow() {
        for(var i =0;i<yuans.length ;i++){
            yuans[i].className = ' ';

        }
        yuans[index].className = 'on';

    }

    /*index = 2    recentIndex = 3  (2-3)*590 =-590 */

    for(var i =0;i<yuans.length ;i++){
        yuans[i].onmouseover = function () {
            var recentIndex = this.getAttribute('a');
            console.log(recentIndex);

            offset = (index-recentIndex)*590;


            ani(offset);
            index = recentIndex ; //新旧更替
            buttonShow();



        }

    }


}