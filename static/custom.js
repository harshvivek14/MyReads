// Accepts a string which is a book id
async function mark_read(id) {
    // Sending a patch request using axios and passing the book id
    res = await axios.patch("/read_unread", {
        book_id: id,
        oper: "r"
    })
}

// Accepts a string which is a book id
async function mark_unread(id) {
    // Sending a patch request using axios and passing the book id and the U as the oper
    res = await axios.patch("/read_unread", {
        book_id: id,
        oper: "u"
    })
}

// Accepts a string which is a book id and rlist_id
// Methods for "adding item to readlist". Will be reused by multiple event listeners.
async function add_to_readlist(book_id, rlist_id) {
    // Sending a patch request using axios and passing the data sent to this method
    res = await axios.patch("/readlist/add_remove", {
        book_id: book_id,
        rlist_id: rlist_id
    })
}

// Accepts a string which is a book id and rlist_id
async function remove_from_readlist(book_id, rlist_id) {
    // Sending a delete request using axios and passing the data sent to this method
    res = await axios.delete("/readlist/add_remove", {
        data: {
            book_id: book_id,
            rlist_id: rlist_id
        }
    })

}

// Accepts a string which is a readlist id
// Methods for removing and sharing private readlists. Will be reused by multiple event listeners. DRY.
async function delete_readlist(rlist_id) {
    // Sending a delete request using axios and passing the data sent to this method
    res = await axios.delete("/readlist/delete", {
        data: {
            rlist_id: rlist_id
        }
    })
}

// Accepts a string which is a readlist id
async function share_readlist(rlist_id) {
    // Sending a put request using axios and passing the data sent to this method
    res = await axios.put("/readlist/share", {
        rlist_id: rlist_id
    })
    // Return the result of the PUT request which is the URL generated on the back-end in a string format
    return res.data;
}

// Accepts a string which is a readlist id
async function unshare_readlist(rlist_id) {
    // Sending a delete request using axios and passing the data sent to this method
    res = await axios.delete("/readlist/shared", {
        data: {
            rlist_id: rlist_id
        }
    })
}

// SEARCH LOGIC
// mapping the DOM element to a variable
search_form = document.getElementById('search-form')
// Adding on event listener for submitting a form. The button type is also submit which triggering the form submission. Thus we don't need an even listener for the search button. Enter or Pressing the button will trigger the search
search_form.addEventListener('submit', function(e){
    // preventing the default behavior of the DOM element
    e.preventDefault()
    // Finding the search textbox
    // mapping the DOM element to a variable
    search_form_input = document.getElementById('search-form-input')
    // Redirecting the user to the search page
    location.href = `/search/${search_form_input.value}`;
})

// Book Read/Unread
if (window.location.href.indexOf("book/") > -1) {
    // mapping the DOM element to a variable
    btn_read_unread = document.getElementById('btn_read_unread')
    // only running this logic if we are on the correct page (if we get a result from our getelementbyid)
    if (btn_read_unread !== null) {
        // adding on event listener for click
        btn_read_unread.addEventListener('click', function (e) {
            e.preventDefault()
            if (btn_read_unread.innerText === " Mark as read") {
                book_id = document.getElementById('book_id').innerText
                console.log(book_id)
                mark_read(book_id)
                btn_read_unread.innerHTML = '<i class="bi bi-bookmark-dash-fill"></i> Mark not read'
            } else if (btn_read_unread.innerText === " Mark not read") {
                book_id = document.getElementById('book_id').innerText
                mark_unread(book_id)
                btn_read_unread.innerHTML = '<i class="bi bi-bookmark-plus"></i></i> Mark as read</button>'
            } else {
                console.log('Error. Could not mark the book as read/unread.')
            }
        })
    }
}


if (window.location.href.indexOf("readlist/read") > -1) {
    btn_readlist_read_remove = document.querySelectorAll('#readlist-read-remove-button')
    if (btn_readlist_read_remove !== null) {
        for (let i of btn_readlist_read_remove) {
            i.addEventListener('click', function (e) {
                e.preventDefault()
                if (i.innerHTML === 'Remove') {
                    i.innerHTML = "Are you sure?"
                } else {
                    book_id = document.getElementById('book-id').innerText
                    console.log(book_id)
                    console.log(book_id.substring(4))
                    mark_unread(book_id.substring(4))
                    i.parentElement.parentElement.parentElement.remove()
                }
            })
        }
    }
}