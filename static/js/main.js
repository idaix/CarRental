// MANAGE BOOKING
const manageBookingForm = document.getElementById('manageBooking'),
      manageBookingBtn = document.getElementById('manageBookingBtn'),
      manageBookingHide = document.getElementById('manageBookingHide')

manageBookingBtn.addEventListener('click', ()=>{
    manageBookingForm.classList.add('show')
})
manageBookingHide.addEventListener('click', ()=>{
    manageBookingForm.classList.remove('show')
})