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
asOfDate.addEventListener("change", function () {
    document.querySelector('#AsOfDateInputForm').submit();
});