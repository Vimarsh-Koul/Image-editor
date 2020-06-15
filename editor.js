
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

 $('#new').click(function(){
  console.log("new button clicked");
});

$('#crop').click(function(){
  console.log("crop button clicked");
});

$('#rectangle-shape').click(function(){
  console.log("rectangle-shape button clicked");
});

$('#circle-shape').click(function(){
  console.log("circle-shape button clicked");
});

$('#triangle-shape').click(function(){
  console.log("triangle-shape button clicked");
});

$('#saturation').click(function(){
  console.log("saturation clicked");
});

$('#temperature').click(function(){
  console.log("temperature clicked");
});

$('#brightness').click(function(){
  console.log("brightess clicked");
});

$('#filter').click(function(){
  console.log("filter button clicked");
});

$('#rotate-right').click(function(){
  console.log("rotate-right button clicked");
});

$('#rotate-left').click(function(){
  console.log("rotate-left button clicked");
});

$('#horizontal-flip').click(function(){
  console.log("horizontal-flip button clicked");
});

$('#vertical-flip').click(function(){
  console.log("vertical-flip button clicked");
});

$('#resize').click(function(){
  console.log("resize button clicked");
});

$('#setting').click(function(){
  console.log("setting button clicked");
});

$('#undo').click(function(){
  console.log("undo button clicked");
});

$('#redo').click(function(){
  console.log("redo button clicked");
});
