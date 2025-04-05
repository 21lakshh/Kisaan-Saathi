// Donation page functionality

// Set donation amount when button is clicked
function setDonationAmount(amount) {
    document.getElementById('donationAmount').value = amount;
    
    // Update UI to show selected amount
    const amountButtons = document.querySelectorAll('.amount-btn');
    amountButtons.forEach(button => {
        button.classList.remove('bg-[#4caf50]');
        button.classList.add('bg-[#1a2e1d]');
    });
    
    // Highlight the selected button (if the event came from a button)
    if (event && event.target) {
        const clickedButton = event.target.closest('button');
        if (clickedButton) {
            clickedButton.classList.remove('bg-[#1a2e1d]');
            clickedButton.classList.add('bg-[#4caf50]');
        }
    }
}

// Set donation frequency type
function setDonationType(type) {
    const oneTimeBtn = document.getElementById('one-time-btn');
    const monthlyBtn = document.getElementById('monthly-btn');
    
    if (type === 'one-time') {
        oneTimeBtn.classList.add('bg-[#4caf50]');
        oneTimeBtn.classList.remove('bg-[#1a2e1d]');
        monthlyBtn.classList.add('bg-[#1a2e1d]');
        monthlyBtn.classList.remove('bg-[#4caf50]');
    } else {
        monthlyBtn.classList.add('bg-[#4caf50]');
        monthlyBtn.classList.remove('bg-[#1a2e1d]');
        oneTimeBtn.classList.add('bg-[#1a2e1d]');
        oneTimeBtn.classList.remove('bg-[#4caf50]');
    }
}

// Show UPI QR code payment modal
function showUPIPayment() {
    const amount = document.getElementById('donationAmount').value || 1000;
    document.getElementById('paymentAmount').textContent = amount;
    
    // Generate QR code (in real implementation, this would call an API)
    generateQRCode(amount);
    
    // Show the modal
    try {
        const qrModal = new bootstrap.Modal(document.getElementById('qrModal'));
        qrModal.show();
    } catch (e) {
        console.error('Bootstrap modal error:', e);
        // Fallback to jQuery
        try {
            $('#qrModal').modal('show');
        } catch (e) {
            console.error('jQuery modal error:', e);
            alert('Could not show payment modal. Please try again.');
        }
    }
}

// Placeholder for QR code generation
function generateQRCode(amount) {
    // In a real implementation, this would call a backend API to generate a QR code
    // For now, we'll just use a placeholder image
    console.log(`Generating QR code for ₹${amount}`);
    
    // Simulate a dynamic QR code by adding the amount to the URL
    // In production, this would be a real QR code URL
    const qrCodeElement = document.getElementById('dynamicQRCode');
    if (qrCodeElement) {
        // In a real implementation, you'd generate or fetch a real QR code
        // This is just a placeholder for demonstration
        qrCodeElement.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=kisaansaathi@axis&pn=KisaanSaathi&am=${amount}&cu=INR`;
    }
}

// Show card payment form
function showCardPayment() {
    // In a real implementation, this would show a card payment form
    alert('Card payment gateway will be integrated here');
}

// Show Paytm payment option
function showPaytmPayment() {
    // In a real implementation, this would redirect to Paytm or show a Paytm payment modal
    alert('Paytm gateway will be integrated here');
}

// Initialize when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add click event listeners to amount buttons
    const amountButtons = document.querySelectorAll('.amount-btn');
    amountButtons.forEach(button => {
        button.addEventListener('click', () => {
            const amount = button.getAttribute('data-amount');
            if (amount) {
                setDonationAmount(parseInt(amount));
            }
        });
    });
    
    // Add class to buttons for easier selection
    const donationButtons = document.querySelectorAll('[onclick^="setDonationAmount"]');
    donationButtons.forEach(button => {
        button.classList.add('amount-btn');
        
        // Extract amount from onclick attribute
        const onclickAttr = button.getAttribute('onclick');
        if (onclickAttr) {
            const match = onclickAttr.match(/setDonationAmount\((\d+)\)/);
            if (match && match[1]) {
                button.setAttribute('data-amount', match[1]);
            }
        }
    });
});

// Make functions available globally for direct onclick handlers
window.setDonationAmount = setDonationAmount;
window.setDonationType = setDonationType;
window.showUPIPayment = showUPIPayment;
window.showCardPayment = showCardPayment;
window.showPaytmPayment = showPaytmPayment;

// Export functions for use in HTML when imported as a module
export {
    setDonationAmount,
    setDonationType,
    showUPIPayment,
    showCardPayment,
    showPaytmPayment
}; 