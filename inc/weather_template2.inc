<div class="weather" style="background-color:%(color)s">
	<a href="%(url)s" target="_top">
	<h1>%(term)s</h1>
	<h2>%(score)s</h2>
	</a>
	<div class="trend">
		<canvas class="canvas" id="trendline-%(term)s" width="170" height="50">
			<div class="bar" style="height:%(score_y3)s%%;left:0%%;"></div>
			<div class="bar" style="height:%(score_y2)s%%;left:25%%;"></div>
			<div class="bar" style="height:%(score_y1)s%%;left:50%%;"></div>
			<div class="bar" style="height:%(score_y)s%%;left:75%%;"></div>
		</canvas>
		<div class="prev">
			<div class="day"><script type="text/javascript">printDay(3)</script></div>
			<span class="score">%(score_y3)s</span>
		</div>
		<div class="prev">
			<div class="day"><script type="text/javascript">printDay(2)</script></div>
			<span class="score">%(score_y2)s</span>
		</div>
		<div class="prev">
			<div class="day"><script type="text/javascript">printDay(1)</script></div>
			<span class="score">%(score_y1)s</span>
		</div>
		<div class="prev">
			<div class="day">Today</div>
			<span class="score">%(score_y)s</span>
		</div>
	</div>
	<div class="source">
			%(source)s<span class="linkback">, via <a href="http://twitterweather.media.mit.edu" target="_top">Twitter Weather</a></span>
	</div>
</div>

    <script type="text/javascript">  
      draw("trendline-%(term)s",["%(score_y3)s","%(score_y2)s","%(score_y1)s","%(score_y)s"]);
    </script>  
