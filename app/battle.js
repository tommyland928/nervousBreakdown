
var befTableCard = [[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]];
window.addEventListener('DOMContentLoaded', function(){
    setInterval(() => {
        fetch('/cgi-bin/battleInfo.py')
        .then(response => {
        return response.json()
        })
        .then(data => {
            //カードの画像を更新
            tableCard = data["tableCard"];
            if (befTableCard != tableCard.toString()){
                console.log("do");
                for (var i=0; i<4; i++){
                    for (var j=0; j<6; j++){
                        if (befTableCard[i][j] != tableCard[i][j].toString()){
                            var card = tableCard[i][j];
                            var suit = card[0];
                            var num = card[1];
                            
                            var id = "i"+i+j;
                            var img = "/reverseImg/";
                            if (suit == -1){//-1になったらカードを取られたってこと
                                img += "back.png";
                            }else if (suit == 0){
                                img += "reverse.png";
                            }else if (suit == 1){
                                img += "s/"+num+".png";
                            }else if (suit == 2){
                                img += "c/"+num+".png";
                            }else if (suit == 3){
                                img += "h/"+num+".png";
                            }else if (suit == 4){
                                img += "d/"+num+".png";
                            }
                            //this.document.getElementById(id).setAttribute('src',img);
                            var isBack = true;
                            let image = isBack ? img : '/reverseImg/back.png';
                            rotationAnimationLoop(document.getElementById(id), image, 0);
                            isBack = !isBack;
                        }
                    }
                }
            }
            befTableCard = tableCard;

            //scoreを表示
            get = data["get"]
            member = data["member"]
            for(var i=0;i<member.length;i++){
                member[i] = decodeURI(member[i])
            }
            if(get[0] != 0 || get[1] != 0){
                this.name[1]  
            }
            if(member != ""){
                this.document.getElementById("winner").innerHTML = ""
                this.document.getElementById("score").innerHTML = member[0] + ": " + get[0] + "枚 " + member[1] + ": " + get[1] + "枚"
            }
           

            //勝者情報があれば更新
            if(data["winner"] != ""){
                //真ん中に勝者を表示
                this.document.getElementById("winner").innerHTML = "勝者: " + data["winner"]
                
                this.document.getElementById("clicked").setAttribute("type","button")


            }




        })
        .catch(error => {
            console.log(error);
        })
    }, 300);//msで指定　1000ms=1s
});


const rotationAnimationLoop = (element, imagePath, deg) =>{
    if( deg <= 180 ){
        console.log("kpokpeorkagarg")
        rotationAnimation(element, imagePath, deg);
        setTimeout( 
            () => {
                rotationAnimationLoop(element, imagePath, deg+= 5 ) 
            }, 
        1 );
    }
}

const rotationAnimation = (element, imagePath, deg) =>{
    if ( 90 === deg ){
        element.src =  imagePath;
    }else {
        element.style.webkitTransform = 'rotateY(' + deg + 'deg)';
    }
}



