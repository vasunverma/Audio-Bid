URL = window.URL || window.webkitURL;
var gumStream, rec, input, audioContext;
var AudioContext = window.AudioContext || window.webkitAudioContext;
var start, pause, resume, stop, red, recording, recorded;

Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});


$(".btn-create-modal").on('click', function(e) {
    mySelect = document.getElementById('DropDown');
    mySelect.selectedIndex = 0;
    document.getElementById('end_date').value = new Date().toDateInputValue();
    document.getElementById('end_date').setAttribute("min", new Date().toDateInputValue());

    red = document.getElementById("red-dot");
    start = document.getElementById("start-rec");
    pause = document.getElementById("pause-rec");
    resume = document.getElementById("resume-rec");
    stop = document.getElementById("stop-rec");
    recording = document.getElementById("record-file");
    recorded = document.getElementById("recorded");

    start.addEventListener("click", startRecording);
    pause.addEventListener("click", pauseRecording);
    resume.addEventListener("click", resumeRecording);
    stop.addEventListener("click", stopRecording);
});

$('.drop-down-show-hide').hide();

$('#DropDown').change(function() {
    $('.drop-down-show-hide').hide();    
    $('#' + this.value).show();
    if(this.value == "diva"){
        $("#URL").attr('required', ''); 
        $("#audiofile").removeAttr('required');
        $("#recorded").removeAttr('required');
    }
    else if(this.value == "divb"){
        $("#audiofile").attr('required', ''); 
        $("#URL").removeAttr('required');
        $("#recorded").removeAttr('required');
    }
    else if(this.value == "divc"){
        $("#recorded").attr('required', ''); 
        $("#URL").removeAttr('required');
        $("#audiofile").removeAttr('required');
    }
});

// Audio Recorder functions

function startRecording() {
    handleButtons(false, true, false, true, true);
    recording.src = "";

    var constraints = { audio: true, video: false }
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		audioContext = new AudioContext();
		gumStream = stream;
		input = audioContext.createMediaStreamSource(stream);
		rec = new Recorder(input,{numChannels:1});
		rec.record();
	}).catch(function(err) {
        handleButtons(true, false, false, false, false);
        console.log("ERROR", err);
	});
}

function pauseRecording() {
    handleButtons(false, false, true, true, false);
    if (rec.recording) {
        rec.stop();
    }
}

function resumeRecording() {
    handleButtons(false, true, false, true, true);
    if (!rec.recording) {
        rec.record();
    }
}

function stopRecording() {
    handleButtons(true, false, false, false, false);
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

function handleButtons(x1, x2, x3, x4, x5) {
    start.style.display = x1?"block":"none";
    pause.style.display = x2?"block":"none";
    resume.style.display = x3?"block":"none";
    stop.style.display = x4?"block":"none";
    red.style.display = x5?"inline":"none";
}