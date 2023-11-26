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
    
    book_detail_readlist_item = document.querySelectorAll("#book-detail-readlist-item")
    book_id = document.getElementById('book_id').innerText
    if (book_detail_readlist_item !== null && book_id !== null) {
        // since the querySelectAll returns a list, running the following for each item
        for (let i of book_detail_readlist_item) {
            if (i.children[1]) {
                i.style.setProperty('background-color', 'limegreen')
            // If the book is not in the readlist yet, do this
            } else {
                i.addEventListener('click', function (e) {
                    e.preventDefault()
                    readlist_id = i.parentElement.getAttribute('id')
                    add_to_readlist(book_id, readlist_id)
                    console.log(book_id, readlist_id)
                    i.innerHTML = '<h5 class="mb-0"><i class="bi bi-check2"></i> Added to readlist</h5>'
                    i.style.setProperty('background-color', 'limegreen')
                })
            }
        }
    }
}


if (window.location.href.indexOf("readlist/private") > -1) {
    readlist_private_remove_button = document.querySelectorAll('#readlist-private-remove-button')
    if (readlist_private_remove_button !== null) {
        for (let i of readlist_private_remove_button) {
            i.addEventListener('click', function (e) {
                e.preventDefault()
                // if the button says Remove, make sure we display Are you sure to confirm
                if (i.innerHTML === 'Remove') {
                    i.innerHTML = "Are you sure?"
                } else {
                    // getting the id attribute of the parent which is a readlist id
                    readlist_id = i.parentElement.getAttribute('id')
                    console.log(readlist_id)
                    // calling the custom method and passing the readlist id
                    delete_readlist(readlist_id)
                    // removing the div that we clicked on
                    i.parentElement.parentElement.parentElement.remove()
                }
            })
        }
    }

    readlist_private_share_button = document.querySelectorAll('#readlist-private-share-button')
    if (readlist_private_share_button !== null) { 
        for (let i of readlist_private_share_button) { 
            i.addEventListener('click', function (e) { 
                e.preventDefault()
                readlist_id = i.parentElement.getAttribute('id')

                if(i.getAttribute('url')) {
                    // if the readlist already has a shared url, don't send axios reqest, just redirect
                    let url = i.getAttribute('url')
                    location.href = `/readlist/shared/${url}`;
                } else {
                    // if the readlist does not have a url yet, send an axios PUT request
                    let u = share_readlist(readlist_id)
                    u.then(data => {location.href = `/readlist/shared/${data}`;})
                }
            })
        }
    }

    readlist_private_details_remove_button = document.querySelectorAll('#readlist-private-details-remove-button')
    if (readlist_private_details_remove_button !== null) {
        for (let i of readlist_private_details_remove_button) {
            i.addEventListener('click', function (e) {
                e.preventDefault()
                // if the button says Remove, make sure we display Are you sure to confirm
                if (i.innerHTML === 'Remove') {
                    i.innerHTML = "Are you sure?"
                // If the button does not say that, do the following. Example is second click after Are you sure?. 
                } else {
                    // getting the id attribute of the parent which is a book id
                    book_id = i.parentElement.getAttribute('book_id')
                    rlist_id = i.parentElement.getAttribute('rlist_id')
                    // calling the custom method and passing the book id and readlist id
                    remove_from_readlist(book_id, rlist_id)
                    // removing the div that we clicked on
                    i.parentElement.parentElement.parentElement.remove()
                }
            })
        }
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
                    mark_unread(book_id.substring(4))
                    i.parentElement.parentElement.parentElement.remove()
                }
            })
        }
    }
}

if (window.location.href.indexOf("readlist/shared") > -1) {
    // UN-SHARE BUTTON EVENT LISTENER
    readlist_shared_unshare_button = document.querySelectorAll('#readlist-shared-unshare-button')

    if (readlist_shared_unshare_button !== null) { 
        for (let i of readlist_shared_unshare_button) { 
            i.addEventListener('click', function (e) { 
                e.preventDefault()
                rlist_id = i.parentElement.getAttribute('id')
                // if the button says Remove, make sure we display Are you sure to confirm
                if (i.innerHTML === 'Un-share') {
                    i.innerHTML = "Are you sure?"
                } else {
                    unshare_readlist(rlist_id)
                    i.parentElement.parentElement.parentElement.remove()
                }
            })
    }

    // COPY URL BUTTON EVENT LISTENER
    readlist_shared_copy_url_button = document.querySelectorAll('#readlist-shared-copy-url-button')
    if (readlist_shared_copy_url_button !== null) { 
        for (let i of readlist_shared_copy_url_button) { 
            i.addEventListener('click', function (e) { 
                e.preventDefault()
                // getting the attribute url which is the readlist's url
                rlist_url = i.getAttribute('url')
                // getting the current url
                curr_url = window.location.href;
                // adding the current URL to / character and then the URL that was generated by us
                full_url = curr_url + '/' + rlist_url;
                // copying the newly created URL into clipboard
                navigator.clipboard.writeText(full_url);

                i.innerHTML = '<i class="bi bi-clipboard2-check"></i>  Copied'
                i.classList.remove('btn-info')
                i.classList.add('btn-success')
                
                // Timer for adding the original info and class back
                setTimeout(() => {
                    i.innerHTML = '<i class="bi bi-clipboard2"></i>  Copy URL'
                    i.classList.remove('btn-success')
                    i.classList.add('btn-info')
                }, 1500) // 1.5 second timeout.
            })
        }
    }
}
}