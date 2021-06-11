var chart = LightweightCharts.createChart(document.getElementById('chart_low_timeframe'), {
	width: 800,
    height: 400,
	layout: {
		backgroundColor: '#000000',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	rightPriceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
});

var candleSeries = chart.addCandlestickSeries({
  upColor: 'green',
  downColor: 'red',
  borderDownColor: 'red',
  borderUpColor: 'green',
  wickDownColor: 'red',
  wickUpColor: 'green',
});

candleSeries.setData(low_time_frame_data);