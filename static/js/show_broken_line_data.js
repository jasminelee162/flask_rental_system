function broken_line_chart(data) {
    var salaru_line = echarts.init(document.getElementById('broken_line'), 'infographic');
    window.addEventListener('resize', function () {
        salaru_line.resize();
    });

    var Data1 = data['3室2厅'];
    var Data2 = data['2室2厅'];
    var Data3 = data['2室1厅'];
    var Data4 = data['1室1厅'];
    var date_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];

    var option = {
        backgroundColor: "rgba(39, 41, 61, 0.95)", // 修改背景颜色为dark purple
        tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(39, 41, 61, 0.95)', // 修改提示框背景色
            borderColor: 'rgba(154, 104, 242, 0.5)', // 修改提示框边框色
            textStyle: {
                color: '#fff'
            }
        },
        grid: {
            containLabel: true,
            left: '3%',
            right: '4%',
            bottom: '3%',
            backgroundColor: 'rgba(154, 104, 242, 0.1)', // 添加网格背景色
            borderColor: 'rgba(154, 104, 242, 0.3)' // 添加网格边框色
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: date_list,
            axisLabel: {
                color: 'rgba(255, 255, 255, 0.7)', // 修改文字颜色
                fontSize: 12
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(154, 104, 242, 0.5)' // 修改轴线颜色
                }
            },
            splitLine: {
                lineStyle: {
                    color: 'rgba(154, 104, 242, 0.2)' // 修改分割线颜色
                }
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                color: 'rgba(255, 255, 255, 0.7)', // 修改文字颜色
                fontSize: 12
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(154, 104, 242, 0.5)' // 修改轴线颜色
                }
            },
            splitLine: {
                lineStyle: {
                    color: 'rgba(154, 104, 242, 0.2)' // 修改分割线颜色
                }
            }
        },
        series: [
            {
                name: '3室2厅',
                type: 'line',
                smooth: true,
                data: Data1,
                lineStyle: {
                    color: '#9a68f2', // 修改线条颜色
                    width: 2
                },
                itemStyle: {
                    color: '#9a68f2' // 修改点颜色
                }
            },
            {
                name: '2室2厅',
                type: 'line',
                smooth: true,
                data: Data2,
                lineStyle: {
                    color: '#00d386', // 修改线条颜色
                    width: 2
                },
                itemStyle: {
                    color: '#00d386' // 修改点颜色
                }
            },
            {
                name: '2室1厅',
                type: 'line',
                smooth: true,
                data: Data3,
                lineStyle: {
                    color: '#ff69b4', // 修改线条颜色
                    width: 2
                },
                itemStyle: {
                    color: '#ff69b4' // 修改点颜色
                }
            },
            {
                name: '1室1厅',
                type: 'line',
                smooth: true,
                data: Data4,
                lineStyle: {
                    color: '#ffa07a', // 修改线条颜色
                    width: 2
                },
                itemStyle: {
                    color: '#ffa07a' // 修改点颜色
                }
            }
        ]
    };

    salaru_line.setOption(option);
}