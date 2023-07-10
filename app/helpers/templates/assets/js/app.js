$(document).ready(function () {
  const ctx = document.getElementById("myChart").getContext("2d");

  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [{ label: "Temperature" }],
    },
    options: {
      borderWidth: 3,
      borderColor: ["rgba(255, 99, 132, 1)"],
    },
  });

  function addData(label, data) {
    myChart.data.labels.push(label);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    myChart.update();
  }

  function removeFirstData() {
    myChart.data.labels.splice(0, 1);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 10;
  //connect to the socket server.
  //   var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();

  //receive details from server
  socket.on("updateSensorData", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.value);

    // Show only MAX_DATA_COUNT data
    if (myChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData();
    }
    addData(msg.date, msg.value);
  });

  // const context = document.getElementById("pieChart").getContext("2d");
  // const COLORS = [
  //   "#2ecc71",
  //   "#3498db",
  //   "#95a5a6",
  //   "#9b59b6",
  //   "#f1c40f",
  //   "#e74c3c",
  //   "#34495e"
  // ];  
  // const pieChart = new Chart(context, {
  //   type: "pie",
  //   data: {
  //     labels: ["Green", "Blue", "Gray", "Purple", "Yellow", "Red", "Black"],
  //     datasets: [
  //       {
  //         backgroundColor: COLORS,
  //         data: [12, 19, 3, 17, 28, 24, 7],
  //       },
  //     ],
  //   },
  //   options: {
  //     layout: {
  //       padding: 50,
  //     },
  //     legend: {
  //       display: false,
  //     },
  //     plugins: {
  //       outlabels: {
  //         backgroundColor: null,
  //         color: COLORS,
  //         stretch: 30,
  //         font: {
  //           resizable: true,
  //           minSize: 15,
  //           maxSize: 20,
  //         },
  //         zoomOutPercentage: 100,
  //         textAlign: "start",
  //         backgroundColor: null,
  //       },
  //     },
  //   },
  // });

  // const tambahData = (index, data) => {
  //   pieChart.data.dataset[index].data[data] + 1;
  //   pieChart.update();
  // };
});
