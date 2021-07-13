let data={
    schools:[]
};

let vm = new Vue({
    el:'#school-app',
    data,
    mounted(){
        fetch('http://localhost:5000/bank')
            .then(resp=>resp.json())
            .then(data=>{
                for(i in data.data) {
                    this.schools.push(data.data[i])
                }
            })
    },
});