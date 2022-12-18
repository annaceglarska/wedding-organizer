const deleteBtns = document.querySelectorAll('button[data-type="delete"]')
const modalTextContainer = document.querySelector('div.modal-body p')
const modalDeleteBtn = document.querySelector('button[data-type="delete-table"]')
const deleteBtnsAsArray = Array.from(deleteBtns);

const getMessageTemplate = (tableName) => `
Are you sure you want to delete ${tableName} ?
`

deleteBtnsAsArray.forEach(deleteBtn => {
    deleteBtn.addEventListener('click', (e) => {
        const btn = e.target;
        const name = btn.getAttribute('data-table-name')
        const tableId = btn.getAttribute('data-table-id')
        modalTextContainer.innerText = getMessageTemplate(name)
        modalDeleteBtn.setAttribute('data-table-id', tableId)
        $('#exampleModal').modal()
    })
})

modalDeleteBtn.addEventListener('click', async (e) => {
    const btn = e.target;
    const tableId = btn.getAttribute('data-table-id')

    try {
        await fetch(`/api/table/${tableId}`, {
            method: "DELETE"
        })

        $('#exampleModal').modal('hide')
        location.reload();
    } catch (error) {
        console.log(error)
    }
})

