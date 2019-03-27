$(document).ready(function () {

    const messages = $('#messages');

    const users_wrapper = $('#users');

    let old_messages = $('.message');

    const typing_user = $('#typing');

    let now_typing = new Set();

    let users = new Set();

    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            let date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    function getCookie(name) {
        let nameEQ = name + "=";
        let ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    window.username = getCookie('username');

    if (!window.username) {
        UIkit.modal.prompt('Ваше имя:', '').then(function (name) {
            setCookie('username', name);
            window.username = name;
            setSocket();
        });
    } else {
        setSocket();
    }

    function setSocket() {
        window.webSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

        window.webSocket.onopen = () => {
            webSocket.send(JSON.stringify({'type': 'join', 'username': window.username}));
            console.log('WebSocket Connection opened!');
        };

        window.webSocket.onclose = () => {
            console.log('WebSocket Connection closed!');
        };

        window.webSocket.onmessage = (message) => {
            let data = JSON.parse(message.data);
            switch (data.msg_type) {
                case 'message':
                    let msg_wrapper = $("<li><div class='message'>" +
                        "<div class='name'>" + data.username + "</div>" +
                        "<div class='text'>" + data.message + "</div>" +
                        "</div></li>");
                    if (data.username === window.username) {
                        msg_wrapper.find('.name').remove();
                        msg_wrapper.closest('li').addClass('uk-clearfix uk-text-right');
                        msg_wrapper.find('.message').addClass('uk-align-right uk-margin-remove-bottom');
                    }
                    messages.append(msg_wrapper);
                    let last_message = messages.find('li:last-child')[0];
                    last_message.scrollIntoView();
                    break;
                case 'join':
                    console.log('Someone join', data);
                    users.add(data.username);
                    show_users();
                    break;
                case 'typing':
                    console.log('Someone typing');
                    if (!now_typing.has(data.username)) {
                        now_typing.add(data.username);
                        show_typing()
                    }
                    break;
                case 'stats':
                    let stats = data.stats;
                    let _users = users_wrapper.find('li');
                    for (let i = 0; i < _users.length; i++) {
                        if (stats.afk.includes($(_users[i]).text())) {
                            console.log($(_users[i]).text(), 'has gone away');
                            $(_users[i]).addClass('afk');
                        } else {
                            $(_users[i]).removeClass('afk');
                        }
                    }
                    break;
                default:
                    console.log('Other action', data);
                    break;
            }
        };
    }

    for (let i = 0; i < old_messages.length; i++) {
        let sender = $.trim($(old_messages[i]).find('.name').text());
        if (sender === window.username) {
            $(old_messages[i]).find('.name').remove();
            $(old_messages[i]).closest('li').addClass('uk-clearfix uk-text-right');
            $(old_messages[i]).addClass('uk-align-right uk-margin-remove-bottom');
        }
    }


    for (let i = 0; i < users_wrapper.length; i++) {
        let old_user = users_wrapper.children('li').eq(i).text();
        if (old_user !== '') {
            users.add(old_user);
        }
    }

    function show_users() {
        users_wrapper.html('');
        if (users.size >= 1) {
            for (let user_item of users) {
                let user = $('<li>' + user_item + '</li>');
                users_wrapper.append(user);
            }
        }
    }

    show_users();

    function show_typing() {
        typing_user.html('');
        for (let item of now_typing) {
            let typing_mes = $('<span>' + item + ' is typing...</span>');
            typing_user.append(typing_mes);
            setTimeout(function () {
                now_typing.delete(item);
                show_typing();
            }, 3e3);
        }
    }

    const message_input = $('#messageBox');

    message_input.on('focus', function () {
        webSocket.send(JSON.stringify({
            'type': 'typing',
            'username': window.username
        }));
    });


    $('#messageSend').click(function () {
        if (message_input.val() !== '') {
            webSocket.send(JSON.stringify({
                'message': message_input.val(),
                'type': 'send_message',
                'username': window.username
            }));
            message_input.val('');
        }
    });
})