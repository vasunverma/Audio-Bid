URL = window.URL || window.webkitURL;
var gumStream, rec, input, audioContext;
var AudioContext = window.AudioContext || window.webkitAudioContext;

var start = document.getElementById("start-rec");
var stop = document.getElementById("stop-rec");
var recording = document.getElementById("record-file");

start.addEventListener("click", startRecording);
stop.addEventListener("click", stopRecording);

function startRecording() {
    console.log("STARTING");
    start.style.display = "none";
    stop.style.display = "block";
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

    rec.stop();
	gumStream.getAudioTracks()[0].stop();
	rec.exportWAV(handleBlob);
}

function handleBlob(blob) {
    var url = URL.createObjectURL(blob);
    recording.src = url;
}