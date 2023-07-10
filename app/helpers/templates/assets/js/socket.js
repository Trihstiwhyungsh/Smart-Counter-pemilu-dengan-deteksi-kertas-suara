$(document).ready( _ => {
    const context = document.getElementById("pieChart").getContext("2d");
    const COLORS = [
        "#FFB84C",
        "#F266AB",
        "#A459D1"
    ]
    const myChart = new Chart(context, {
        type: "doughnut",
        data: {
            labels: ["Paslon 1", "Paslon 2", "Tidak Sah"],
            datasets: [
                {
                    backgroundColor: COLORS,
                    data: [1, 1, 1],
                },
            ],
        }
    });

    const addData = label => {
        if (label == "P1") {
            myChart.data.datasets[0].data[0] += 1;
        } else if (label == "P2") {
            myChart.data.datasets[0].data[1] += 1;
        } else {
            myChart.data.datasets[0].data[2] += 1;
        }
    }

    const socket = io.connect();
    socket.on('count', data => {
        addData(data.paslon);
        myChart.update();
    });
});