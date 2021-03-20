const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const links = document.querySelectorAll('.nav-links li');

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    links.forEach(link => {
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
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function createBoard() {
    $.ajax({
        type: "POST",
        url: newBoard,
        success: function (data) {
            clearBoard();
        },
        error: function (data) {
            alert(`Error occurred when creating a new game.`)
        }
    })
}


let interval = window.setInterval(function () {
    refreshBoard()
}, 2000);

function refreshBoard() {
    let board_id = window.location.href

    $.ajax({
        type: "GET",
        url: refreshNewBoard,
        data: {'board_id': board_id},
        dataType: "json",
        success: function (response) {
            document.querySelector("#first_field").innerHTML = response["first_field"]
            document.querySelector("#second_field").innerHTML = response["second_field"]
            document.querySelector("#third_field").innerHTML = response["third_field"]
            document.querySelector("#fourth_field").innerHTML = response["fourth_field"]
            document.querySelector("#fifth_field").innerHTML = response["fifth_field"]
            document.querySelector("#sixth_field").innerHTML = response["sixth_field"]
            document.querySelector("#seventh_field").innerHTML = response["seventh_field"]
            document.querySelector("#eighth_field").innerHTML = response["eighth_field"]
            document.querySelector("#ninth_field").innerHTML = response["ninth_field"]
            document.querySelector("#last_move").innerHTML = response["last_move"]
        }
    })
}

function updateBoard(button_id) {
    let board_id = window.location.href

    $.ajax({
        type: "PUT",
        url: newUpdateBoard,
        data: {'button_id': button_id, 'board_id': board_id},
        dataType: 'json',
        async: false,
        success: function (data) {
            document.querySelector(`#${button_id}`).innerHTML = data[button_id]
        },
        error: function (data) {
            alert(`Error occurred when updating board. Please contact with administrator.`)
        }
    })
}

function joinBoard(board_number) {
    $.ajax({
        type: 'PUT',
        url: joinNewBoard,
        data: {'joined_board': board_number},
        dataType: 'json',
        success: function (data) {

        },
        error: function (data) {
            alert(`Error occurred when updating board. Please contact with administrator.`)
        },
    })
}


$('[id*="_field"]').click(function () {
    let button_id = this.id
    updateBoard(button_id)
});


function clearBoard() {
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

