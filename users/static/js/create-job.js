$(".btn-create-modal").on('click',function(e){

    mySelect = document.getElementById('DropDown');
    mySelect.selectedIndex = 0;
    document.getElementById('end_date').value = new Date().toDateInputValue();
    document.getElementById('end_date').setAttribute("min", new Date().toDateInputValue());

});

$('.drop-down-show-hide').hide();

$('#DropDown').change(function () {
    $('.drop-down-show-hide').hide()    
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
