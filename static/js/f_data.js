function getdata1(data) {
    console.log('getdata1接收到的数据类型:', typeof data);
    console.log('getdata1接收到的数据是否为数组:', Array.isArray(data));
    console.log('getdata1接收到的数据:', data);

    if (!Array.isArray(data)) {
        console.error('传入的数据不是数组，无法做回归');
        return;
    }

    var myChart = echarts.init(document.getElementById('f_line'), 'dark-purple');

    var myRegression = ecStat.regression('linear', data);
    console.log('回归结果:', myRegression);

if (!myRegression || !myRegression.parameter || typeof myRegression.parameter.gradient !== 'number') {
    console.error('回归计算失败，结果缺少 gradient 或 intercept');
    return;
}

var gradient = myRegression.parameter.gradient;
var intercept = myRegression.parameter.intercept;

    var predictedPoints = data.map(([x]) => [x, gradient * x + intercept]);

    var option = {
        title: {
            text: '房价走势分析',
            subtext: '基于历史数据预测',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'cross' }
        },
        legend: {
            data: ['实际房价', '预测走势'],
            top: '8%'
        },
        grid: {
            left: '8%',
            right: '8%',
            bottom: '20%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            name: '时间点',
            splitLine: { lineStyle: { type: 'dashed' } }
        },
        yAxis: {
            type: 'value',
            name: '价格（元/月）',
            splitLine: { lineStyle: { type: 'dashed' } }
        },
        series: [
            {
                name: '实际房价',
                type: 'scatter',
                data: data,
                symbolSize: 10,
                itemStyle: { opacity: 0.7 }
            },
            {
                name: '预测走势',
                type: 'line',
                data: predictedPoints,
                symbolSize: 0.1,
                lineStyle: { width: 2 },
                markPoint: {
                    label: {
                        show: true,
                        formatter: myRegression.expression,
                        color: '#fff',
                        backgroundColor: 'rgba(154, 104, 242, 0.8)',
                        padding: [5, 10],
                        borderRadius: 5
                    },
                    data: [{ coord: predictedPoints[predictedPoints.length - 1] }]
                }
            }
        ]
    };

    myChart.setOption(option);

    // 创建数据表格（保持不变）
    var tableHtml = '<div class="data-table-container" style="margin-top: 20px; padding: 15px; background: rgba(39, 41, 61, 0.8); border-radius: 10px;">' +
        '<h4 style="color: #fff; margin-bottom: 15px;">房价数据明细</h4>' +
        '<div style="max-height: 300px; overflow-y: auto;">' +
        '<table class="table table-dark table-hover" style="background: transparent;">' +
        '<thead><tr><th>序号</th><th>时间点</th><th>实际价格</th><th>预测价格</th><th>差异</th></tr></thead><tbody>';

    data.forEach(function (item, index) {
        var predictedPrice = predictedPoints[index][1];
        var difference = (item[1] - predictedPrice).toFixed(2);
        var differenceClass = difference > 0 ? 'text-success' : 'text-danger';

        tableHtml += '<tr>' +
            '<td>' + (index + 1) + '</td>' +
            '<td>' + item[0].toFixed(2) + '</td>' +
            '<td>' + item[1].toFixed(2) + '</td>' +
            '<td>' + predictedPrice.toFixed(2) + '</td>' +
            '<td class="' + differenceClass + '">' + difference + '</td>' +
            '</tr>';
    });

    tableHtml += '</tbody></table></div></div>';

    document.getElementById('f_line').insertAdjacentHTML('afterend', tableHtml);

    window.addEventListener('resize', function () {
        myChart.resize();
    });
}
