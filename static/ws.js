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
            case 'rndm_btn_resp':
                $('#img_url').attr('src',data);
                break;
            default:
                alert('event name is not recognised');
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


    var refreshIntervalId = 0;
    // WS events to send to the server
    $("#next_btn").mousedown( function()    {
        try {clearInterval(refreshIntervalId);} catch {};
        input = "next_btn"
        send_ws_event("next_btn", input);
    } );

    $("#rndm_btn").mousedown( function()    {
        try {clearInterval(refreshIntervalId);} catch {};
        input = "rndm_btn"
        send_ws_event("rndm_btn", input);
    } );

    $("#save_btn").mousedown( function()    {
        input = $('#img_url').attr('src');
        send_ws_event("save_btn", input);
    } );

    $("#auto_next_btn").mousedown( function()    {
        var interval = $("#refresh").val()*1000;
        refreshIntervalId = setInterval(function(){send_ws_event("next_btn", "next_btn");}, interval);
    } );

    $("#auto_rndm_btn").mousedown( function()    {
            var interval = $("#refresh").val()*1000;
            refreshIntervalId = setInterval(function(){send_ws_event("rndm_btn", "rndm_btn");}, interval);
     } );


    //example of repeating function
    //setInterval(function(){ update_joystick_coords() }, joy_update_interval_ms);

});

