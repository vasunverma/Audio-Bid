function reply_click(clicked_id, element_to_get, text_to_display) {
    var element = document.getElementById(element_to_get);
    element.innerHTML = '';

    var job_id = clicked_id;
    const input = document.createElement("input");
    input.id = "jobId";
    input.name = "jobId";
    input.value = job_id;
    input.type = "hidden";
    element.appendChild(input);

    var tag = document.createElement("p");
    var text = document.createTextNode(text_to_display);
    tag.appendChild(text);
    element.appendChild(tag);

    if(element_to_get == "modal_body_upload_transcript"){
        const textFileInput = document.createElement("input");
        textFileInput.classList.add("form-control");
        textFileInput.type = "file";
        textFileInput.id = "transcriptFile";
        textFileInput.name = "transcriptFile";
        element.appendChild(textFileInput);
    }
}