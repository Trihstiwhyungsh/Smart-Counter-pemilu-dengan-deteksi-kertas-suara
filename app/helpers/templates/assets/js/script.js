const socket = io.connect(window.location.protocol + '//' + document.domain + ':' + location.port);
socket.on('connect', () => {
    console.log("Connected...!", socket.connected);
});

const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const video = document.querySelector("#videoElement");

video.width = 400;
video.height = 300;

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({
        video: true
    })
        .then(stream => {
            video.srcObject = stream;
            video.play();
        }).catch(err => {});
};

setInterval(() => {
    width = video.width;
    height = video.height;
    context.drawImage(video, 0, 0, width, height);
    var data = canvas.toDataURL('image/jpeg', 0.5);
    context.clearRect(0, 0, width, height);
    socket.emit('image', data);
}, 25);

socket.on('processed_image', image => {
    photo.setAttribute('src', image);
});
