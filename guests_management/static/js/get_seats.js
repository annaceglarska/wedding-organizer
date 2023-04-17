const tableSelect = document.querySelector('#table')
const seatSelect = document.querySelector('#seat')

const getOptionTemplate = (seatId, seatNumber) => `
<option value="${seatId}">${seatNumber}</option>
`
const defaultOption = `<option value="" disabled selected>Select seat</option>`

tableSelect.addEventListener('change', async (e) => {
    const tableId = e.target.value
    try {
        const response = await fetch(`/api/seat/${tableId}`, {
            method: "DELETE"
        })
        const seats = await response.json()
        const seatOptions = seats.map((seat) => {
            return getOptionTemplate(seat.seatId, seat.seatNumber)
        })
        seatOptions.unshift(defaultOption)
        seatSelect.innerHTML = seatOptions
    } catch (error) {
        console.log(error)
    }
})