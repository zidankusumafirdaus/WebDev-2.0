document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.otp-input');
    const form = document.getElementById('otp-form');
    const fullOtpInput = document.getElementById('full-otp');

    inputs.forEach((input, index) => {
        input.addEventListener('input', function (e) {
            const value = e.target.value.replace(/[^0-9]/g, ''); 
            e.target.value = value.charAt(0); 
            if (value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', function (e) {
            if (e.key === 'Backspace') {
                if (!this.value && index > 0) {
                    inputs[index - 1].focus();
                }
            }
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const otp = Array.from(inputs).map(input => input.value).join('');
        fullOtpInput.value = otp;

        if (otp.length === inputs.length) {
            this.submit();
        } else {
            alert('Kode OTP belum lengkap!');
        }
    });
});
