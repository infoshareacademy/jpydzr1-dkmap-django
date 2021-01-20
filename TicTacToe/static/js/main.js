const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const links = document.querySelectorAll('.nav-links li');

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    links.forEach(link =>{
        link.classList.toggle('fade');
    });
}); 


function clicked() {
    return confirm('Message.');
}

var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function createBoard() {
    $.ajax({
        type: "POST",
        url: newBoard,
})}


function updateBoard(button_id) {
    $.ajax({
        type: "PUT",
        url: newUpdateBoard,
        data: {'button_id': button_id},
        dataType: 'json',

        success: function(data) {
            document.querySelector('#' + button_id).innerHTML = data[button_id]
          },
        error: function(data) {
        alert(`das`)
        }
})}


$('[id*="_field"]').click(function () {
    let button_id = this.id
    updateBoard(button_id)
});

