let wsScheme = window.location.protocol === 'http:' ? 'ws' : 'wss';
let wsPath = `${wsScheme}://${window.location.host}/ws/counter/`;
let websocket = new WebSocket(wsPath);

websocket.onmessage = function(event) {
    console.log("New data comming from websocket:")
    let data = JSON.parse(event.data);
    console.log(`[ref_office]  comming from websocket : ${data.ref_office}`)
    console.log(`[counter]  comming from websocket : ${data.counter}`)
    updateCounterUI(data);
};

function updateCounterUI(data) {
    const counterOffice = data.counter;
    const refOffice = data.ref_office;
    let msg = "";
    // Update the UI with the latest counter value
    const elementCounterOffice = $(`#counter-office${refOffice}`)
    const elementReferenceOffice = $(`#reference-office${refOffice}`)
    if (elementReferenceOffice !== undefined && elementReferenceOffice != null) {
        console.log("elementReferenceOffice is available ")
        const valueElementReferenceOffice = elementReferenceOffice.text()

        if (refOffice !== valueElementReferenceOffice) {
            msg = `web socket ref_office[${refOffice}] not match elementReferenceOffice [${valueElementReferenceOffice}]`
            console.log(msg);
            return ;
        }
        if (elementCounterOffice === undefined || elementCounterOffice === null) {
            console.log("elementCounterOffice is not  available ")
            return ;
        }
        // update value counter in the user interface in right office card 
        elementCounterOffice.text(counterOffice)
    } else {
        console.log("elementReferenceOffice is not  available ")
    }
}

websocket.onopen = function(event) {
    console.log('WebSocket connection established.');
};

websocket.onerror = function(event) {
    console.error('WebSocket error:', event);
};
