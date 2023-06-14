var befTableCard = [[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]];
window.addEventListener('DOMContentLoaded', function(){
    setInterval(() => {
        fetch('http://192.168.11.140:8000/cgi-bin/battleInfo.py')
        .then(response => {
        return response.json()
        })
        .then(data => {
            console.log(data);
            tableCard = data["tableCard"];
            console.log(befTableCard);
            console.log(tableCard);
            if (befTableCard != tableCard.toString()){
                console.log("do");
                for (var i=0; i<4; i++){
                    for (var j=0; j<6; j++){
                        if (befTableCard[i][j] != tableCard[i][j].toString()){
                            var card = tableCard[i][j];
                            var suit = card[0];
                            var num = card[1];
                            
                            var id = "i"+i+j;
                            var img = "/img/";
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
                            this.document.getElementById(id).setAttribute('src',img);
                        }
                    }
                }
            }
            befTableCard = tableCard;
        })
        .catch(error => {
            console.log(error);
        })
    }, 1000);//msで指定　1000ms=1s
});
