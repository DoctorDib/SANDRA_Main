const connect = () => {
    console.log("Attempting to connect");
    websocket = new WebSocket(`ws://${window.location.hostname}:8765/`);
    console.log("Connected...");
    
    const interval = setInterval(() => {
        try {
            websocket.send(JSON.stringify({'ID': 'Webserver', 'type': 'get-info'}));
        } catch (error) {
            console.log(error);
            console.log("Error connecting")
        }
    }, 5000);

    websocket.onmessage = (event) => {
        data = JSON.parse(event.data);

        switch (data.type) {
            case 'data_response':
                if (infoDisplayActive) {
                    load_info(infoClient, false)
                }

                handle_response(data.content)
                break;
            
            default:
                console.error("unsupported event", data);
        }
    };

    websocket.onopen = (e) => {
        ChangeServerStat(true);
    }

    // Solution
    // https://stackoverflow.com/questions/22431751/websocket-how-to-automatically-reconnect-after-it-dies
    websocket.onclose = (e) => {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        ChangeServerStat(false);
        setTimeout(() => {
            clearInterval(interval);
            connect();
        }, 5000);
    };

    websocket.onerror = (error) => {
        console.log(error);
        console.log("Error connecting");
        websocket.close();
    };
}

const updateServer = () => {
    websocket.send(JSON.stringify({'ID': 'Webserver', 'type': 'update-sandra'}));
}

let websocket = null;

connect();

// initialising

setTimeout(() => { 
    try {
        websocket.send(JSON.stringify({'ID': 'Webserver', 'type': 'get-info'}));
    } catch (error) {
        console.log("Error connecting");
    }
}, 250);