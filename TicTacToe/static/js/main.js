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
        success: function(data) {
            clearBoard();
          },
        error: function(data) {
        alert(`Something went wrong.`)
        }
})}


function updateBoard(button_id) {
    $.ajax({
        type: "PUT",
        url: newUpdateBoard,
        data: {'button_id': button_id},
        dataType: 'json',
        success: function(data) {
            document.querySelector(`#${button_id}`).innerHTML = data[button_id]
          },
        error: function(data) {
        alert(`Something went wrong.`)
        }
})}

function joinBoard() {
    $.ajax({
        type: 'PUT',
        url: joinNewBoard,
        dataType: 'json',

        success: function (){
            alert('hej1')
        },
        error: function () {
            alert('hej2')
        },
    })}


$('[id*="_field"]').click(function () {
    let button_id = this.id
    updateBoard(button_id)
});


function clearBoard(){
    $("#first_field").html("");
    $("#second_field").html("");
    $("#third_field").html("");
    $("#fourth_field").html("");
    $("#fifth_field").html("");
    $("#sixth_field").html("");
    $("#seventh_field").html("");
    $("#eighth_field").html("");
    $("#ninth_field").html("");
}

