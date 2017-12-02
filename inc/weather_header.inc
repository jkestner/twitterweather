<script type="text/javascript">
<!--
var dow = ["Sun","Mon","Tue","Wed","Thur","Fri","Sat"];
function printDay(ago) {
	var day = (new Date().getDay() + 7 - ago) % 7
	document.write(dow[day])
}

function draw(weatherId,yy){
	var canvas = document.getElementById(weatherId);  
	if (canvas.getContext){
	  for (x=0;x<yy.length;x++)
		if (yy[x] == "?") yy[x] = 50;
	  var ctx = canvas.getContext('2d');  
	
		//neutral line
		ctx.strokeStyle = "rgba(255, 255, 255, 0.3)"; 
		ctx.beginPath();
		ctx.moveTo(0,25);  
		ctx.lineTo(170,25);  
		ctx.stroke();
		
		//lines between scores
		for (yi=0;yi<yy.length-1;yi++) {
			ctx.strokeStyle = "rgba(255, 255, 255, "+(yi*0.2+0.3)+")"; 
			ctx.beginPath();
			ctx.moveTo(20+yi*42.5,(100-yy[yi])/2);  
			ctx.lineTo(20+(yi+1)*42.5,(100-yy[yi+1])/2);  
			ctx.stroke();
		}
		
		//dot for current score
		ctx.fillStyle = "rgba(255, 255, 255, "+((yy.length-1)*0.2+0.3)+")";  
		ctx.arc(20+(3)*42.5,(100-yy[yy.length-1])/2,1.5,0,Math.PI*2,true);
		ctx.fill();
		ctx.fillStyle = "rgba(255, 255, 255, "+((yy.length-1)*0.1+0.3)+")";  
		ctx.arc(20+(3)*42.5,(100-yy[yy.length-1])/2,3,0,Math.PI*2,true);
		ctx.fill();
	
	} else {
		//presumably, no canvas support
	}
}  

//-->
</script>