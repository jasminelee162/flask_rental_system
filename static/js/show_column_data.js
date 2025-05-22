function column_chart(data) {

    var salaru_line = echarts.init(document.getElementById('scolumn_line'));
    window.addEventListener('resize', function () {
        salaru_line.resize();
    });
    // var XData=['东方凤雅台', '仙桐御景', '仙湖山庄二期', '仙湖枫景家园', '兰亭国际公寓', '华景园御庭轩', '合正锦园一期', '名骏豪庭', '广岭家园', '新世界四季御园', '新世界鹿茵翠地', '桐景花园', '聚宝华府', '金色年华家园', '鸿景翠峰', '鹏兴花园一期', '鹏兴花园三期', '鹏兴花园二期', '鹏兴花园六期', '鹏莲花园'];
    // var yData=[1, 1, 1, 3, 1, 1, 1, 3, 4, 1, 1, 1, 2, 2, 1, 2, 1, 8, 1, 1];
    // {'name_list_x': name_list, 'num_list_y': num_list}
    var XData = data['name_list_x'];
    var yData = data['num_list_y'];

    var dataMin = parseInt(Math.min.apply(null, yData)/2);

    // ... 其他代码保持不变 ...

var option = {
    backgroundColor: "rgba(39, 41, 61, 0.95)", // 修改背景颜色为dark purple
    grid: {
        height:'200px',
        backgroundColor: 'rgba(154, 104, 242, 0.1)', // 添加网格背景色
        borderColor: 'rgba(154, 104, 242, 0.3)' // 添加网格边框色
    },
    xAxis: {
        axisTick: {
            show: false
        },
        splitLine: {
            show: false
        },
        splitArea: {
            show: false
        },
        data: XData,
        axisLabel: {
            formatter: function (value) {
                var ret = "";
                var maxLength = 1;
                var valLength = value.length;
                var rowN = Math.ceil(valLength / maxLength);
                if (rowN > 1) {
                    for (var i = 0; i < rowN; i++) {
                        var temp = "";
                        var start = i * maxLength;
                        var end = start + maxLength;
                        temp = value.substring(start, end) + "\n";
                        ret += temp;
                    }
                    return ret;
                } else {
                    return value;
                }
            },
            interval: 0,
            fontSize: 11,
            fontWeight: 100,
            textStyle: {
                color: 'rgba(255, 255, 255, 0.7)', // 修改文字颜色
            }
        },
        axisLine: {
            lineStyle: {
                color: 'rgba(154, 104, 242, 0.5)' // 修改轴线颜色
            }
        }
    },
    yAxis: {
        axisTick: {
            show: false
        },
        splitLine: {
            lineStyle: {
                color: 'rgba(154, 104, 242, 0.2)' // 修改分割线颜色
            }
        },
        splitArea: {
            show: false
        },
        min: dataMin,
        axisLabel: {
            textStyle: {
                color: 'rgba(255, 255, 255, 0.7)', // 修改文字颜色
                fontSize: 16,
            }
        },
        axisLine: {
            lineStyle: {
                color: 'rgba(154, 104, 242, 0.5)' // 修改轴线颜色
            }
        }
    },
    tooltip: {
        trigger: "item",
        textStyle: {
            fontSize: 12
        },
        formatter: "{b0}: {c0}套",
        backgroundColor: 'rgba(39, 41, 61, 0.95)', // 修改提示框背景色
        borderColor: 'rgba(154, 104, 242, 0.5)' // 修改提示框边框色
    },
    series: [{
        type: "bar",
        itemStyle: {
            normal: {
                color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                        offset: 0,
                        color: 'rgba(154, 104, 242, 0.8)' // 修改渐变起始颜色
                    }, {
                        offset: 1,
                        color: 'rgba(154, 104, 242, 0.2)' // 修改渐变结束颜色
                    }],
                    globalCoord: false
                },
                barBorderRadius: 15,
            }
        },
        data: yData
    }]
};

// ... 其他代码保持不变 ...

    salaru_line.setOption(option, true);
}