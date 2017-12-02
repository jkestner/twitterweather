<div class="weather" style="background-color:%(color)s">
	<a href="%(url)s" target="_top">
	<h1>%(term)s</h1>
	<h2>%(score)s</h2>
	</a>
	<div class="trend">
		<div class="prev">
			%(score_y3)s <div class="bar" style="height:%(score_y3)s%%"></div>
			<div class="day"><script type="text/javascript">printDay(3)</script></div>
		</div>
		<div class="prev">
			%(score_y2)s <div class="bar" style="height:%(score_y2)s%%"></div>
			<div class="day"><script type="text/javascript">printDay(2)</script></div>
		</div>
		<div class="prev">
			%(score_y1)s <div class="bar" style="height:%(score_y1)s%%"></div>
			<div class="day"><script type="text/javascript">printDay(1)</script></div>
		</div>
		<div class="prev">
			%(score_y)s <div class="bar" style="height:%(score_y)s%%"></div>
			<div class="day">Today</div>
		</div>
	</div>
	<div class="source">
			%(source)s<span class="linkback">, via <a href="http://twitterweather.media.mit.edu" target="_top">Twitter Weather</a></span>
	</div>
</div>