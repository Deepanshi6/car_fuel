//
// GET DOM ELEMENTS (important!)
//

// Driver inputs
const nameInput = document.getElementById("name");
const genderInput = document.getElementById("gender");
const dobInput = document.getElementById("dob");
const dojInput = document.getElementById("doj");
const licenseInput = document.getElementById("license_number");
const carIdInput = document.getElementById("car_id");

// Edit driver inputs
const editDriverId = document.getElementById("edit_driver_id");
const editName = document.getElementById("edit_name");
const editLicense = document.getElementById("edit_license");
const editCar = document.getElementById("edit_car");

// Delete driver input
const deleteDriverId = document.getElementById("delete_driver_id");

// CAR inputs
const car_id = document.getElementById("car_id");
const company = document.getElementById("company");
const model = document.getElementById("model");
const fuel_type = document.getElementById("fuel_type");

// Edit car inputs
const edit_car_id = document.getElementById("edit_car_id");
const edit_company = document.getElementById("edit_company");
const edit_model = document.getElementById("edit_model");
const edit_fuel_type = document.getElementById("edit_fuel_type");

// Delete car input
const delete_car_id = document.getElementById("delete_car_id");

// Fuel Log inputs
const driver_id = document.getElementById("driver_id");
const fuel_car_id = document.getElementById("car_id");
const fuel_type_input = document.getElementById("fuel_type");
const fuel_get = document.getElementById("fuel_get");
const total_fuel = document.getElementById("total_fuel");
const spent = document.getElementById("spent");
const pump = document.getElementById("pump");
const place = document.getElementById("place");

// Edit fuel log inputs
const edit_log_id = document.getElementById("edit_log_id");
const edit_fuel_get = document.getElementById("edit_fuel_get");
const edit_total_fuel = document.getElementById("edit_total_fuel");
const edit_spent = document.getElementById("edit_spent");
const edit_pump = document.getElementById("edit_pump");
const edit_place = document.getElementById("edit_place");


//
// DRIVER CRUD
//
async function addDriver() {
    const data = {
        name: nameInput.value,
        gender: genderInput.value,
        dob: dobInput.value,
        doj: dojInput.value,
        license_number: licenseInput.value,
        car_id: carIdInput.value || null
    };

    const response = await fetch("/driver/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const res = await response.json();
    alert(res.message);
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
    const id = deleteDriverId.value;

    const res = await fetch(`/driver/delete/${id}`, { method: "DELETE" });
    alert("Driver Deleted");
    loadDrivers();
}

async function editDriver() {
    const data = {
        id: Number(editDriverId.value),
        name: editName.value,
        license_number: editLicense.value,
        car_id: editCar.value
    };

    const response = await fetch("/driver/edit", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const res = await response.json();
    alert(res.message);
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

    const response = await fetch("/car/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const res = await response.json();
    alert(res.message);
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

    const response = await fetch("/car/edit", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const res = await response.json();
    alert(res.message);
    loadCars();
}



//
// FUEL LOG CRUD
//
async function addFuelLog() {
    const data = {
        driver_id: Number(driver_id.value),
        car_id: fuel_car_id.value,
        fuel_type_name: fuel_type_input.value,
        fuel_get: Number(fuel_get.value),
        total_fuel: Number(total_fuel.value),
        latest_spent: Number(spent.value),
        petrol_pump_name: pump.value,
        place: place.value
    };

    const response = await fetch("/fuel/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const res = await response.json();
    alert(res.message);
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

    const response = await fetch("/fuel/edit", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const res = await response.json();
    alert(res.message);
    loadFuelLogs();
}
