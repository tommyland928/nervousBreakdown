const btn = document.querySelector('.readyBtn');
const url = 'http://192.168.11.140:8000/cgi-bin/ready.py';

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
    }).catch((error) => {
        console.log(error);
    });
};

btn.addEventListener('click', postFetch, false);