document.querySelectorAll("img").forEach((imgElm) =>{
    imgElm.addEventListener('click',function(){
        console.log(this.id);
        removeI = this.id.replace("i","");
        row = removeI.substr(0,1);
        column = removeI.substr(1,1);
        
        console.log(row);
        console.log(column);
        
        const form = new FormData();
        form.append('row', row);
        form.append('column', column);

        fetch("http://192.168.11.140:8000/cgi-bin/openCard.py", {
            method: 'POST',
            body: form
        }).then((response) => {
            if(!response.ok) {
                console.log('error!');
            } 
            //console.log('ok!');
            return response.json();
        }).then((data)  => {
            //console.log(data);
        }).catch((error) => {
            console.log(error);
        });

    });
})