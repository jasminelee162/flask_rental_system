function pie_chart(data) {
    // 使用 dark-purple 主题
    var myChart = echarts.init(document.getElementById('pie'), 'dark-purple');

    window.addEventListener('resize', function () {
        myChart.resize();
    });

    var option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)",
            backgroundColor: 'rgba(26,26,46,0.9)',
            textStyle: {
                color: '#ffffff'
            }
        },
        series: [{
            name: '户型的占比',
            type: 'pie',
            radius: ['10%', '50%'],
            center: ['50%', '50%'],
            // 优化后的配色方案（与dark-purple背景协调的宝石色调）
            color: [
                '#8A2BE2', // 蓝紫色
                '#9370DB', // 中紫色
                '#BA55D3', // 中等兰花紫
                '#9932CC', // 暗兰花紫
                '#DA70D6', // 兰花紫
                '#FF69B4', // 热粉红
                '#FF1493', // 深粉红
                '#C71585', // 中紫红色
                '#DB7093', // 苍紫罗兰红
                '#FFA07A'  // 浅鲑鱼色
            ],
            label: {
                color: '#ffffff',
                fontSize: 14,
                fontWeight: 'bold'  // 加粗标签文字
            },
            labelLine: {
                lineStyle: {
                    color: 'rgba(255, 255, 255, 0.3)',
                    width: 1.5
                }
            },
            itemStyle: {
                borderColor: 'rgba(0,0,0,0.3)',
                borderWidth: 1,
                emphasis: {
                    shadowBlur: 15,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(255, 255, 255, 0.5)', // 白色阴影更协调
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }
            },
            data: data
        }]
    };

    myChart.setOption(option);
}