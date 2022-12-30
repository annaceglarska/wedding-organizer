const deleteBtns = document.querySelectorAll('button[data-type="delete"]')
const modalTextContainer = document.querySelector('div.modal-body p')
const modalDeleteBtn = document.querySelector('button[data-type="delete-element"]') //cos nie moge tego zmienić
const deleteBtnsAsArray = Array.from(deleteBtns);

const getMessageTemplate = (guestName, guestSurname) => `
Are you sure you want to delete ${guestName} ${guestSurname} ?
`

deleteBtnsAsArray.forEach(deleteBtn => {
    deleteBtn.addEventListener('click', (e) => {
        const btn = e.target;
        const name = btn.getAttribute('data-guest-name')
        const surname = btn.getAttribute('data-guest-surname')
        const guestId = btn.getAttribute('data-guest-id')
        modalTextContainer.innerText = getMessageTemplate(name, surname)
        modalDeleteBtn.setAttribute('data-guest-id', guestId)
        $('#exampleModal').modal()
    })
})

modalDeleteBtn.addEventListener('click', async (e) => {
    const btn = e.target;
    const guestId = btn.getAttribute('data-guest-id')

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


