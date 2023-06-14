window.addEventListener('DOMContentLoaded', function(){
    setInterval(() => {
        fetch('http://192.168.11.140:8000/cgi-bin/movePhase.py')
        .then(response => {
        return response.json()
    })
    .then(data => {

        //console.log(data)
    })
    .catch(error => {
        console.log(error)
})
        
}, 1000);//msで指定　1000ms=1s
});