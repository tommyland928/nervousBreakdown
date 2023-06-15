const btn = document.querySelector('.readyBtn');
const url = '/cgi-bin/ready.py';

const postFetch = () => {
    fetch(url, {
        method: 'POST'
    }).then((response) => {
        if(!response.ok) {
            console.log('error!');
        } 
        //console.log('ok!');
        return response.json();
    }).then((data)  => {
        //console.log(data);
        document.getElementById("clicked").setAttribute("type","hidden")
        document.getElementById("score").innerHTML = "対戦待ち"
    }).catch((error) => {
        console.log(error);
    });
};

btn.addEventListener('click', postFetch, false);