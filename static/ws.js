$(document).ready(function(){
    // WS init
    var WEBSOCKET_ROUTE = "/ws";
    if(window.location.protocol == "http:")         { var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE); }
    else if(window.location.protocol == "https:")   { var ws = new WebSocket("wss://" + window.location.host + WEBSOCKET_ROUTE); }

    //check ws status on html page
    ws.onopen = function(ws_incoming) {   $("#ws-status").html("Connected"); };
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
                var current_symbol = $('#symbol').text()

                data.forEach(function(item, i, data) {
                    if (item.localeCompare(current_symbol)){
                        var link = `<a href='?s=${item}' class='button'>${item}</a>`

                    }
                    else{
                        var link = `<a href='?s=${item}' class='button' style="color: #f4e74d;">${item}</a>`
                    }
                    $('#shortlisted').append(link)
                })

                break;


           case 'update_unlisted_vals':
                $('#unlisted_symbols').empty()
                data.forEach(function(item, i, data) {
                    var link = `<option value="${item}">`
                    $('#unlisted_symbols').append(link)
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
        console.log(event_json);
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

    $("#comment_update_button").mousedown( function()    {
            var symbol = $('#symbol').text();
            var comment = $('#comments_area').val();

            send_ws_event("comment_update_button", [symbol,comment]);
            window.location.reload(false);
        } );

    $("#open_symbol_button").mousedown( function()    {
                var selected_symbol = $('[name="list_input"]').val();
                var url = "?s="+selected_symbol
                window.location = url
            } );


});

