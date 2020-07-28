$('#exit').click(function(){
  confirm("Are you sure you want to Exit!");
});

$('#cancle').click(function(){
  confirm("Are you sure you want to Cancle!");
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

 $('#open').click(function(){
   $('.url').css("visibility","visible");
 });

 $('.url-submit').click(function(){
   $('.url').css("visibility","hidden");
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

$('.apply-button').click(function(){
 console.log("apply button clicked");
});

$('.cancle-button').click(function(){
 console.log("cancle button clicked");
});

