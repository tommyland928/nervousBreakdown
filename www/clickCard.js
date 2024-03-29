document.querySelectorAll("img").forEach((imgElm) =>{
    imgElm.addEventListener('click',function(){
        removeI = this.id.replace("i","");
        row = removeI.substr(0,1);
        column = removeI.substr(1,1);
        
        const form = new FormData();
        form.append('row', row);
        form.append('column', column);

        fetch("/cgi-bin/openCard.py", {
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
