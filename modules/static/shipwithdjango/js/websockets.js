/**
 * @fileoverview This file has functions related to websockets.
 */

var WS_PAGE_ID = generatePageId(); // The page id of the current page.

// Sockets
var userSocket = undefined;

window.addEventListener('load', function() {

    // Initialize the websocket for the users route.
    userSocket = initWebsocket('users', userSocketOnOpen, userSocketActions);

});

/**
 * Generates a random page id. This is used to identify the page when sending messages to the websocket.
 * @returns {string} The page id.
 * @example
 * const page_id = generatePageId();
 * console.log(page_id);
 * // Output: 3j4k5l6m7
 */
function generatePageId() {
    return Math.random().toString(36).substr(2, 9);
}

/** 
 * Returns the correct websocket protocol: wss or ws depending on the current protocol.
 * @returns {string} The websocket protocol.
 * @example
 * const connection_string = `${returnWSProtocol()}//${window.location.host}/ws/${route}/`;
 */
function returnWSProtocol() {
    if(window.location.protocol == 'https:') {
        return 'wss:'
    } else {
        return 'ws:'
    }
}

/**
 * Initializes a websocket.
 * @param {string} route - The route to connect to.
 * @param {Function} onopen_func - The function to call when the websocket is opened. The socket is passed as an argument.
 * @param {Function} action_func - The function to call when the websocket receives a message. The socket, action, and payload data are passed as arguments.
 * @returns {Object} The websocket object.
 * @example
 *  // Connects to the route /ws/users/ and calls the function user_socket_onopen when the websocket is opened.
 * const socket = initWebsocket('users', onopen_func=user_socket_onopen);
 * function user_socket_onopen(socket) {
 *    alert('The websocket is opened!');
 * }
 */
function initWebsocket(route, onOpenFunc=undefined, actionFunc=undefined) {
    const protocol = returnWSProtocol();
    const connection_string = `${protocol}//${window.location.host}/ws/${route}/`;
    let socket = new WebSocket(connection_string);

    socket.onopen = function open() {
        console.log(`WebSocket (${route}) is connected.`)
        if(onOpenFunc) { onOpenFunc(socket); }
    }

    socket.onclose = function(e) {
        console.log(`WebSocket (${route}) is closed. Reconnect will be attempted in 10 seconds. Reason: ${e.reason}`);
        setTimeout(function() {
            socket = new WebSocket(connection_string);
            initWebsocket(route, onOpenFunc, actionFunc);
        }, 10000);
    }

    socket.onmessage = function(e) {

        let message_data = JSON.parse(e.data);
        let action = message_data['action'];
        let page_id = message_data['page_id'];
        let data = message_data['payload'];

        console.log(`WebSocket (${route}) received a message with action: ${action}`);

        // If the page id does not match the current page id, then ignore the message.
        if(page_id != WS_PAGE_ID && page_id != 'all_pages') {
            console.log(`The page id ${page_id} does not match the current page id ${WS_PAGE_ID}. Ignoring the message.`);
            return;
        }

        // Call the action function if it exists.
        if(actionFunc) {
            actionFunc(socket, action, data);
        }
    }

    if(socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }

    return socket;
}

/**
 * Gets called when the user socket is opened.
 * @param {Object} socket - The websocket object.
 * @returns {void}
 */
function userSocketOnOpen(socket) {
    console.log('User socket is opened.');
}

/**
 * Gets called when the user socket receives a message.
 * Defines all the actions that the user socket can receive and what to do with them.
 * @param {Object} socket - The websocket object.
 * @param {string} action - The action to perform.
 * @param {Object} data - The data to use for the action.
 * @returns {void}
 */
function userSocketActions(socket, action, data) {
    console.log(`User socket action: ${action}`);
}