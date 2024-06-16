const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("collapsed");
});

const navLinkEls = document.querySelectorAll('.sidebar-link');
navLinkEls.forEach(navLinkEl => {
    navLinkEl.addEventListener('click', () => {
        document.querySelector('.activated')?.classList.remove('activated');
        navLinkEl.classList.add('activated');
    });
});


const asOfDate = document.querySelector('#AsOfDate');
asOfDate?.addEventListener("change", function () {
    document.querySelector('#AsOfDateInputForm').submit();
});

const selectedAccount = document.querySelector('#SelecetedAccount');
selectedAccount?.addEventListener("change", function () {
    document.querySelector('#AccountSelectForm').submit();
    //const selectedAccountOptions = 
    consolge.log(selectedAccount.value);
});

new Autocomplete('#autocomplete', {
    search : input => {
        const url = "/main/search/?client="+input;
        return new Promise(resolve =>{
            fetch(url)
            .then(response => response.json())
            .then(data => {
                resolve(data.data)
            })
        })
    },
    onSubmit : result => {
        document.querySelector("#ClientSelectForm").submit();
    }
});