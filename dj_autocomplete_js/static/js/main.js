
new Autocomplete('#autocomplete', {
    search : input => {
        console.log(input)
        const url = "/search/?address="+input
        return new Promise(resolve => {
            fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                resolve(data.data)
            })
        })
    }
});