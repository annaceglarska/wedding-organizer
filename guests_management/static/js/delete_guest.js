const deleteBtns = document.querySelectorAll('button[data-type="delete"]')
const modalTextContainer = document.querySelector('div.modal-body p')
const modalDeleteBtn = document.querySelector('button[data-type="delete"]') //cos nie moge tego zmienić
const deleteBtnsAsArray = Array.from(deleteBtns);

const getMessageTemplate = (guestName) => `
Are you sure you want to delete ${guestName} ?
`

deleteBtnsAsArray.forEach(deleteBtn => {
    deleteBtn.addEventListener('click', (e) => {
        const btn = e.target;
        const name = btn.getAttribute('data-guest-name')
        const guestId = btn.getAttribute('data-guest-id')
        modalTextContainer.innerText = getMessageTemplate(name)
        modalDeleteBtn.setAttribute('data-guest-id', guestId)
        $('#exampleModal').modal()
    })
})

modalDeleteBtn.addEventListener('click', async (e) => {
    const btn = e.target;
    const tableId = btn.getAttribute('data-guest-id')

    try {
        await fetch(`/api/guest-delete/${guestId}`, {
            method: "DELETE"
        })

        $('#exampleModal').modal('hide')
        location.reload();
    } catch (error) {
        console.log(error)
    }
})


