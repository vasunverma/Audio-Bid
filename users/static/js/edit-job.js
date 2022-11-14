URL = window.URL || window.webkitURL;
var gumStream, rec, input, audioContext;
var AudioContext = window.AudioContext || window.webkitAudioContext;
var startEdit, pauseEdit, resumeEdit, stopEdit, redEdit, recordingEdit, recordedEdit;

Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});

document.getElementById('edit_end_date').value = new Date().toDateInputValue();

function getSubpath(path, subpathLevel) {
  arr = path.split("/");
  subpath = "";
  for(i = 0; i < subpathLevel && i < arr.length; i++)
      subpath += "/" + arr[i+1];
  return subpath;
}

$('.drop-down-show-hide').hide();

$('#editDropDown').change(function() {
    $('.drop-down-show-hide').hide()    
    $('#' + this.value).show();
    if(this.value == "div1"){
        $("#edit-URL").attr('required', ''); 
        $("#edit-audiofile").removeAttr('required');
        $("#edit-recorded").removeAttr('required');
    }
    else if(this.value == "div2"){
        $("#edit-audiofile").attr('required', ''); 
        $("#edit-URL").removeAttr('required');
        $("#edit-recorded").removeAttr('required');
    }
    else{
        $("#edit-recorded").attr('required', ''); 
        $("#edit-record-file").attr('required', '');
        $("#edit-URL").removeAttr('required');
        $("#edit-audiofile").removeAttr('required');
    }
});

$(".btn-modal").on('click',function(e){

    id = $(this).attr('id');
    document.querySelector('.editSaveBtn').id = id

    mySelect = document.getElementById('editDropDown');
    mySelect.selectedIndex = 0;
    document.getElementById('edit_end_date').setAttribute("min", new Date().toDateInputValue());
    currentLocation = window.location.toString()
    path = getSubpath(currentLocation, 2)
    e.preventDefault();
    
    $.ajax({
    url: "/users/jobs/"+id+"/",
    type:'GET',
    datatype: 'json',
    success: function(data) {
        $('#edit-name').val(data["name"])
        $('#edit-description').val(data["description"])
        $('#edit-price').val(data["price"])
        $('#edit_end_date').val(data["end_date"])
        $('#cardModal').modal("show");
    },  
    error:function() {
        alert("Some error occurred while trying to update the job. Please try again in sometime.");
        window.location.href = path; 
    }});

});

$(".editSaveBtn").on('click', function(e) {
    idd = $(this).attr('id')
    $("#edit-form").attr('action', "/users/jobs/"+idd+"/");
    $("#edit-form").attr('method', 'post'); 
});

redEdit = document.getElementById("edit-red-dot");
startEdit = document.getElementById("edit-start-rec");
pauseEdit = document.getElementById("edit-pause-rec");
resumeEdit = document.getElementById("edit-resume-rec");
stopEdit = document.getElementById("edit-stop-rec");
recordingEdit = document.getElementById("edit-record-file");
recordedEdit = document.getElementById("edit-recorded");

startEdit.addEventListener("click", startEditRecording);
pauseEdit.addEventListener("click", pauseEditRecording);
resumeEdit.addEventListener("click", resumeEditRecording);
stopEdit.addEventListener("click", stopEditRecording);

// Audio Recorder functions

function startEditRecording() {
    handleEditButtons(false, true, false, true, true);
    recordingEdit.src = "";

    var constraints = { audio: true, video: false }
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		audioContext = new AudioContext();
		gumStream = stream;
		input = audioContext.createMediaStreamSource(stream);
		rec = new Recorder(input,{numChannels:1});
		rec.record();
	}).catch(function(err) {
        handleEditButtons(true, false, false, false, false);
        console.log("ERROR", err);
	});
}

function pauseEditRecording() {
    handleEditButtons(false, false, true, true, false);
    if (rec.recording) {
        rec.stop();
    }
}

function resumeEditRecording() {
    handleEditButtons(false, true, false, true, true);
    if (!rec.recording) {
        rec.record();
    }
}

function stopEditRecording() {
    handleEditButtons(true, false, false, false, false);
    rec.stop();
	gumStream.getAudioTracks()[0].stop();
	rec.exportWAV(handleEditBlob);
}

function handleEditBlob(blob) {
    let url = URL.createObjectURL(blob);
    recordingEdit.src = url;

    let file = new File([blob], "test.wav", {type:"audio/wav", lastModified:new Date().getTime()});
    let container = new DataTransfer();
    container.items.add(file);
    recordedEdit.files = container.files;
}

function handleEditButtons(x1, x2, x3, x4, x5) {
    startEdit.style.display = x1?"block":"none";
    pauseEdit.style.display = x2?"block":"none";
    resumeEdit.style.display = x3?"block":"none";
    stopEdit.style.display = x4?"block":"none";
    redEdit.style.display = x5?"inline":"none";
}

