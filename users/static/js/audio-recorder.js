URL = window.URL || window.webkitURL;
var gumStream, rec, input, audioContext;
var AudioContext = window.AudioContext || window.webkitAudioContext;

var red = document.getElementById("red-dot");
var start = document.getElementById("start-rec");
var stop = document.getElementById("stop-rec");
var recording = document.getElementById("record-file");
var recorded = document.getElementById("recorded");

start.addEventListener("click", startRecording);
stop.addEventListener("click", stopRecording);

function startRecording() {
    console.log("STARTING");
    start.style.display = "none";
    stop.style.display = "block";
    red.style.display = "block";
    recording.src = "";

    var constraints = { audio: true, video: false }
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		audioContext = new AudioContext();
		gumStream = stream;
		input = audioContext.createMediaStreamSource(stream);
		rec = new Recorder(input,{numChannels:1});
		rec.record();
	}).catch(function(err) {
        console.log("ERROR", err);
	});
}

function stopRecording() {
    console.log("STOPPING");
    start.style.display = "block";
    stop.style.display = "none";
    red.style.display = "none";

    rec.stop();
	gumStream.getAudioTracks()[0].stop();
	rec.exportWAV(handleBlob);
}

function handleBlob(blob) {
    let url = URL.createObjectURL(blob);
    recording.src = url;

    let file = new File([blob], "test.wav", {type:"audio/wav", lastModified:new Date().getTime()});
    let container = new DataTransfer();
    container.items.add(file);
    recorded.files = container.files;
}