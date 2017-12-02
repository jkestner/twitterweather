<a href="http://search.twitter.com/search?q=%(termq)s" target="_top">
<div class="weather" style="background-color:%(color)s">
<!--<canvas id="myDrawing" width="200" height="200" style="position:absolute; z-index: 0"></canvas>-->
	<h1>%(term)s</h1>
	<h2>%(score)d</h2>
	<div class="trend">
		<div class="prev">
			%(score_y3)d <div class="bar" style="height:%(score_y3)d%%"></div>
			<div class="day"><script type="text/javascript">printDay(3)</script></div>
		</div>
		<div class="prev">
			%(score_y2)d <div class="bar" style="height:%(score_y2)d%%"></div>
			<div class="day"><script type="text/javascript">printDay(2)</script></div>
		</div>
		<div class="prev">
			%(score_y1)d <div class="bar" style="height:%(score_y1)d%%"></div>
			<div class="day"><script type="text/javascript">printDay(1)</script></div>
		</div>
		<div class="prev">
			%(score_y)d <div class="bar" style="height:%(score_y)d%%"></div>
			<div class="day">Today</div>
		</div>
	</div>
</div></a>