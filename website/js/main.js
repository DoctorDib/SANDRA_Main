let infoDisplayActive = false;
let infoClient = '';
let active_clients = {}

const element_template = (name, data) => {
    let element = document.getElementById(client);

    let insert = 
    `<section onclick='load_info("${ name }", true)' id='${ name }' class='device'>
        <section class="dotContainer"> <section class='${ data.active ? 'active' : 'disabled' }'> </section> </section>
        <section id='name'> <section class="deviceName"> ${ name } </section> <section class="ip"> ${ data.address[0] } </section> </section>
    </section>`

    let target = document.getElementById('sidePanelContent');
    target.insertAdjacentHTML( 'beforeend', insert );
}

const handle_response = (json_data) => {
    active_clients = json_data;
    
    for (client in json_data) {
        data = json_data[client];
        
        if (client === "server") {
            let version = document.getElementById("version");
            version.textContent = data["version"];
            continue;
        }

        let element = document.getElementById(client);

        if (!element) {
            element_template(client, data);
        }

        let target = document.querySelectorAll('#' + client + ' > .dotContainer > section');
        target[0].className = data.active ? 'active' : 'disabled';
    }
}

const load_logger = (logger) => {
    let target = document.getElementById('logger');
    target.innerHTML = '';
    
    for (let log in logger) {
        classType = logger[log]['logType'] == 'Error' ? 'errorLogMeesage' : '';

        let insert = `<li className="${ classType }"> ${ logger[log]['message'] } </li>`;

        target.insertAdjacentHTML( 'beforeend', insert );
    }
}

const load_titles = (id, address) => {
    let mainTitleTarget = document.getElementById('detailsName');
    let mainIPTarget = document.getElementById('detailsIP');

    mainTitleTarget.textContent = id;
    mainIPTarget.textContent = address[0];
}

const ResetSelection = () => {
    let devices = document.getElementsByClassName('device');
    for (let device in devices) {
        if (devices[device].classList != undefined) {
            devices[device].classList.remove('selected');
        }
    }
}

const load_info = (id, toggle) => {
    let detailsSection = document.getElementById("detailsParent");
    let selection = document.getElementById(id);
    
    ResetSelection();
    selection.classList.add('selected');

    if ((infoDisplayActive && infoClient == id) && toggle) {
        infoDisplayActive = false;
        detailsSection.className = "hide";
        selection.classList.remove('selected');
        return;
    }

    infoClient = id;
    infoDisplayActive = true;
    detailsSection.className = "show";

    load_titles(id, active_clients[id]['address']);
    load_logger(active_clients[id]['logger']);
}

const ChangeServerStat = (active) => {
    serverstat = document.getElementById('serverConnectionStatus');

    serverstat.classList.add(active ? 'active' : 'disabled');
    serverstat.classList.remove(active ? 'disabled' : 'active');
}