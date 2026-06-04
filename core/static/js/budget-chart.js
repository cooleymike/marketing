// budget-chart.js
function initBudgetChart(datapointsRaw) {
    var chartDom = document.getElementById('chartContainer');

    if (!chartDom) {
        console.warn('Chart container not found');
        return;
    }

    if (!datapointsRaw || datapointsRaw.length === 0) {
        chartDom.innerHTML = '<p class="text-center text-gray-500 text-sm">No budget data to display</p>';
        return;
    }

    // Transform data for ECharts
    var labels = datapointsRaw.map(d => d.label);
    var values = datapointsRaw.map(d => d.y);

    var myChart = echarts.init(chartDom);

    var option = {
        title: {
            text: 'Budget Allocation',
            left: 'center'
        },
        xAxis: {
            type: 'category',
            data: labels
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '${value}'
            }
        },
        series: [
            {
                data: values,
                type: 'bar',
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#667eea' },
                        { offset: 1, color: '#764ba2' }
                    ])
                },
                animationDuration: 1200,
                animationEasing: 'cubicOut'
            }
        ],
        grid: {
            left: '3%',
            right: '3%',
            bottom: '10%',
            containLabel: true
        }
    };

    myChart.setOption(option);

    window.addEventListener('resize', function() {
        myChart.resize();
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initBudgetChart(window.chartData);
});
