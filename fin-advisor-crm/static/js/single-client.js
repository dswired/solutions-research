const clientAsOfDate = document.querySelector('#ClientAsOfDate');
clientAsOfDate?.addEventListener("change", function () {
    document.querySelector('#AccountSelectForm').submit();
});

const selectedAccount = document.querySelector('#SelectedAccount');
selectedAccount?.addEventListener("change", function () {
    document.querySelector('#AccountSelectForm').submit();
});