URL = window.URL || window.webkitURL;
var gumStream, rec, input, audioContext;
var AudioContext = window.AudioContext || window.webkitAudioContext;



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
  return subpath;S
}

$('.drop-down-show-hide').hide();

$('#editDropDown').change(function () {
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
    success: function(data){
        $('#edit-name').val(data["name"])
        $('#edit-description').val(data["description"])
        $('#edit-price').val(data["price"])
        $('#edit_end_date').val(data["end_date"])
        $('#cardModal').modal("show");
        },  
    error:function()
        {
        alert("Some error occurred while trying to update the job. Please try again in sometime.");
        window.location.href = path; 
        }

    });

});


$(".editSaveBtn").on('click',function(e){
    idd = $(this).attr('id')
    $("#edit-form").attr('action', "/users/jobs/"+idd+"/");
    $("#edit-form").attr('method', 'post'); 
});


var edit_red = document.getElementById("edit-red-dot");
var edit_start = document.getElementById("edit-start-rec");
var edit_stop = document.getElementById("edit-stop-rec");
var edit_recording = document.getElementById("edit-record-file");
var edit_recorded = document.getElementById("edit-recorded");

edit_start.addEventListener("click", editstartRecording);
edit_stop.addEventListener("click", editstopRecording);

function editstartRecording() {
    console.log("STARTING");
    edit_start.style.display = "none";
    edit_stop.style.display = "block";
    edit_red.style.display = "block";
    edit_recording.src = "";

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

function editstopRecording() {
    console.log("STOPPING");
    edit_start.style.display = "block";
    edit_stop.style.display = "none";
    edit_red.style.display = "none";

    rec.stop();
	gumStream.getAudioTracks()[0].stop();
	rec.exportWAV(edithandleBlob);
}

function edithandleBlob(blob) {
    let url = URL.createObjectURL(blob);
    edit_recording.src = url;

    let file = new File([blob], "test.wav", {type:"audio/wav", lastModified:new Date().getTime()});
    let container = new DataTransfer();
    container.items.add(file);
    edit_recorded.files = container.files;
}

