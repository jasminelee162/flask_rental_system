function pie_chart(data) {
    var myChart = echarts.init(document.getElementById('pie'), 'dark-purple');
    
    var option = {
        title: {
            text: '户型占比分析',
            subtext: '当前区域房源分布'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            right: 10,
            top: 'center'
        },
        series: [{
            name: '户型占比',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['40%', '50%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: 'rgba(39, 41, 61, 0.8)',
                borderWidth: 2
            },
            label: {
                show: true,
                position: 'outside',
                formatter: '{b}: {d}%'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '16',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: true
            },
            data: data
        }]
    };
    
    myChart.setOption(option);
    
    // 响应式调整
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}