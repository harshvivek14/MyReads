// Accepts a string which is a book id
async function mark_read(id) {
    // Sending a patch request using axios and passing the book id
    res = await axios.patch("/read_unread", {
        book_id: id,
        oper: 'w'
    })
}

// Accepts a string which is a book id
async function mark_unread(id) {
    // Sending a patch request using axios and passing the book id and the U as the oper
    res = await axios.patch("/read_unread", {
        book_id: id,
        oper: 'u'
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
