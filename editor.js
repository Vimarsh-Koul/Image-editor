
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$('#exit').click(function(){
  confirm("Are you sure you want to Exit!");
});

$('#cancle').click(function(){
  confirm("Are you sure you want to Cancle!");
});

$('#save').click(function(){
  alert("Changes saved");
});

$('#save2').click(function(){
  alert("Changes saved");
});

var count = 0

 $('#pen').click(function abcd() {
   count = count + 1;
   if (count % 2 != 0) {
     $('body').css("cursor", "crosshair");
   }
   if (count % 2 == 0) {
     $('body').css("cursor", "auto");
   }
 });
