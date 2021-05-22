$(document).ready(function(){
    // WS init
    var WEBSOCKET_ROUTE = "/ws";
    if(window.location.protocol == "http:")         { var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE); }
    else if(window.location.protocol == "https:")   { var ws = new WebSocket("wss://" + window.location.host + WEBSOCKET_ROUTE); }

    //check ws status on html page
    //ws.onopen = function(ws_incoming) {   $("#ws-status").html("Connected"); };
    //ws.onclose = function(ws_incoming) {  $("#ws-status").html("Disconnected"); };

    // entrance point for events from the server
    ws.onmessage = function(ws_incoming) {

        var ws_json = JSON.parse(ws_incoming.data);
        var event = ws_json.event_name;
        var data = ws_json.event_data;
        // events processing
        switch(event){
            case 'update_shortlist_vals':
                $('#shortlisted').empty()
                data.forEach(function(item, i, data) {
                    var link = `<a href='?s=${item}' class='button'>${item}</a>`
                    $('#shortlisted').append(link)
                })
                break;

           case 'update_unlisted_vals':
                $('#unlisted').empty()
                data.forEach(function(item, i, data) {
                    var link = `<a href='?s=${item}' class='button'>${item}</a>`
                    $('#unlisted').append(link)
                })
                break;

            default:
                alert(event);
        }

    };


    // json events protocol implementation
    function send_ws_event(event_name, event_data) {
        let event = {
        event_name: event_name,
        event_data: event_data
        };

        let event_json = JSON.stringify(event);
        ws.send(event_json);
        return event_json;
    }


    // WS events to send to the server
    $("#shortlist_add_button").mousedown( function()    {
        input = $('#symbol').text();
        send_ws_event("shortlist_add_button", input);
    } );

    $("#shortlist_rem_button").mousedown( function()    {
            input = $('#symbol').text();
            send_ws_event("shortlist_rem_button", input);
        } );



});

