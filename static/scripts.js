//
// DRIVER CRUD
//
async function addDriver() {
    const data = {
        name: name.value,
        gender: gender.value,
        dob: dob.value,
        doj: doj.value,
        license_number: license_number.value,
        car_id: car_id.value || null
    };

    await fetch("/driver/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    alert("Driver Added");
    loadDrivers();
}

async function loadDrivers() {
    const res = await fetch("/driver/get_all");
    const list = await res.json();
    const box = document.getElementById("driver_list");

    box.innerHTML = list.map(d => `
        <div class="record-card">
            <b>ID:</b> ${d.id}<br>
            <b>Name:</b> ${d.name}<br>
            <b>Gender:</b> ${d.gender}<br>
            <b>License:</b> ${d.license}<br>
            <b>Car:</b> ${d.car_id || "-"}
        </div>
    `).join('');
}

async function deleteDriver() {
    const id = delete_driver_id.value;
    await fetch(`/driver/delete/${id}`, { method: "DELETE" });
    alert("Driver Deleted");
    loadDrivers();
}

async function editDriver() {
    const data = {
        id: Number(edit_driver_id.value),
        name: edit_name.value,
        license_number: edit_license.value,
        car_id: edit_car.value
    };

    await fetch("/driver/edit", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    alert("Driver Updated");
    loadDrivers();
}


//
// CAR CRUD
//
async function addCar() {
    const data = {
        car_id: car_id.value,
        company: company.value,
        model: model.value,
        fuel_type_name: fuel_type.value
    };

    await fetch("/car/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    alert("Car Added");
    loadCars();
}

async function loadCars() {
    const res = await fetch("/car/get_all");
    const list = await res.json();

    car_list.innerHTML = list.map(c => `
        <div class="record-card">
            <b>ID:</b> ${c.car_id}<br>
            <b>Company:</b> ${c.company}<br>
            <b>Model:</b> ${c.model}<br>
            <b>Fuel:</b> ${c.fuel_type}
        </div>
    `).join('');
}

async function deleteCar() {
    const id = delete_car_id.value;
    await fetch(`/car/delete/${id}`, { method: "DELETE" });
    alert("Car Deleted");
    loadCars();
}

async function editCar() {
    const data = {
        car_id: edit_car_id.value,
        company: edit_company.value,
        model: edit_model.value,
        fuel_type_name: edit_fuel_type.value
    };

    await fetch("/car/edit", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    alert("Car Updated");
    loadCars();
}


//
// FUEL LOG CRUD
//
async function addFuelLog() {
    const data = {
        driver_id: Number(driver_id.value),
        car_id: car_id.value,
        fuel_type_name: fuel_type.value,
        fuel_get: Number(fuel_get.value),
        total_fuel: Number(total_fuel.value),
        latest_spent: Number(spent.value),
        petrol_pump_name: pump.value,
        place: place.value
    };

    await fetch("/fuel/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    alert("Fuel Log Added");
    loadFuelLogs();
}

async function loadFuelLogs() {
    const res = await fetch("/fuel/get_all");
    const list = await res.json();
    const box1 = document.getElementById("fuel_log_list");
    const box2 = document.getElementById("logs");

    const html = list.map(f => `
        <div class="record-card">
            <b>ID:</b> ${f.log_id}<br>
            <b>Driver:</b> ${f.driver_id}<br>
            <b>Car:</b> ${f.car_id}<br>
            <b>Fuel:</b> ${f.fuel_type}<br>
            <b>Litres:</b> ${f.fuel_get}<br>
            <b>Spent:</b> ₹${f.spent}<br>
            <b>Pump:</b> ${f.pump}<br>
            <b>Place:</b> ${f.place}
        </div>
    `).join('');

    if (box1) box1.innerHTML = html;
    if (box2) box2.innerHTML = html;
}

async function deleteFuelLog() {
    const id = delete_log_id.value;
    await fetch(`/fuel/delete/${id}`, { method: "DELETE" });
    alert("Fuel Log Deleted");
    loadFuelLogs();
}

async function editFuelLog() {
    const data = {
        log_id: Number(edit_log_id.value),
        fuel_get: Number(edit_fuel_get.value),
        total_fuel: Number(edit_total_fuel.value),
        latest_spent: Number(edit_spent.value),
        petrol_pump_name: edit_pump.value,
        place: edit_place.value
    };

    await fetch("/fuel/edit", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    alert("Fuel Log Updated");
    loadFuelLogs();
}
