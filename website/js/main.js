let infoDisplayActive = false;
let infoClient = '';
let active_clients = {}

let test = {
    
    "power_condition": {
        "throttling_occurred": 0,
        "arm_frequency_capped_occurred": 0,
        "under_voltage_occurred": 0,
        "currently_throttled": 0,
        "arm_frequency_capped": 0,
        "under_voltage": 0
    },
    "temperature": "51.5",
    "disk_usage": {
        "total": 15383.74,
        "used": 2449.17,
        "free": 12277.03,
        "percent": 85.00
    },
    "memory_usage": {
        "total": 971.06,
        "available": 839.94,
        "percent": 50.00,
        "used": 70.78,
        "free": 710.81,
        "active": 125.98,
        "inactive": 82.58,
        "buffers": 21.08,
        "cached": 168.39,
        "shared": 6.55
    },
    "swap_memory_usage": {
        "total": 104.85,
        "used": 0.0,
        "free": 104.85,
        "percent": 12.6,
        "sin": 0.00,
        "sout": 0.00
    },
    "cpu_usage": 20
    
}

/*idtest = "testing"  
active_clients[idtest] = test;
load_titles(idtest, active_clients[idtest]['address']);
load_graphs(idtest, active_clients[idtest]['specs'])
load_logger(active_clients[idtest]['logger']);*/

const element_template = (name, data) => {
    console.log(data)

    let insert = 
    `<section onclick='load_info("${ name }", true)' id='${ name }' class='device'>
        <section class="dotContainer"> <section class='${ data.active ? 'active' : 'disabled' }'> </section> </section>
        <section id='name'> <section class="deviceName"> ${ name } </section> <section class="ip"> ${ data.address[0] } </section> </section>
    </section>`

    let target = document.getElementById('sidePanelContent');
    target.insertAdjacentHTML( 'beforeend', insert );
}

const handle_response = json_data => {
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

const load_logger = logger => {
    let target = document.getElementById('logger');
    target.innerHTML = '';
    
    for (let log in logger) {
        classType = logger[log]['logType'] == 'Error' ? 'errorLogMeesage' : '';

        let insert = `<li className="${ classType }"> ${ logger[log]['message'] } </li>`;

        target.insertAdjacentHTML('beforeend', insert);
    }
}

const load_graphs = specs => {

    document.querySelector('#virtual_memory .text').textContent = specs['memory_usage']['percent'] + "%";
    document.querySelector('#virtual_memory circle.circle-chart-circle').style.strokeDasharray = `${75 * (specs['memory_usage']['percent'] / 100)},100`;

    document.querySelector('#swap_memory .text').textContent = specs['swap_memory_usage']['percent'] + "%";
    document.querySelector('#swap_memory circle.circle-chart-circle').style.strokeDasharray = `${75 * (specs['swap_memory_usage']['percent'] / 100)},100`;

    document.querySelector('#disk_usage .text').textContent = specs['disk_usage']['percent'] + "%";
    document.querySelector('#disk_usage circle.circle-chart-circle').style.strokeDasharray = `${75 * (specs['disk_usage']['percent'] / 100)},100`;

    document.querySelector('#cpu_usage .text').textContent = specs['cpu_usage'] + "%";
    document.querySelector('#cpu_usage circle.circle-chart-circle').style.strokeDasharray = `${75 * (specs['cpu_usage'] / 100)},100`;

    //document.querySelector('#virtual_memory section').style.height = specs['memory_usage']['percent'] + "%";
    //document.querySelector('#swap_memory section').style.height = specs['swap_memory_usage']['percent'] + "%";
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
    load_graphs(active_clients[id]['specs'])
    //load_graphs(test)
    load_logger(active_clients[id]['logger']);
}

const ChangeServerStat = (active) => {
    serverstat = document.getElementById('serverConnectionStatus');

    serverstat.classList.add(active ? 'active' : 'disabled');
    serverstat.classList.remove(active ? 'disabled' : 'active');
}