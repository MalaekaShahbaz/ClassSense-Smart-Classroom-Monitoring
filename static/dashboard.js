
async function updateDashboard() {
    try {
        const response = await fetch("/api/readings");

        if (!response.ok) {
            throw new Error("Unable to fetch readings");
        }

        const data = await response.json();

        document.getElementById("temperature").textContent =
            Number(data.temperature).toFixed(1) + " °C";

        document.getElementById("humidity").textContent =
            Number(data.humidity).toFixed(1) + " %";

        document.getElementById("sensor-status").textContent =
            data.source === "simulation"
                ? "Simulation Active"
                : "Sensor Active";

    } catch (error) {
        document.getElementById("sensor-status").textContent =
            "Connection Error";

        console.error(error);
    }
}

updateDashboard();

setInterval(updateDashboard, 5000);
