// function getdata1(data) {
//     var center1 = echarts.init(document.getElementById('f_line'), 'infographic');
//     window.addEventListener('resize', function () {
//         center1.resize();
//     });
//
//     var myRegression = ecStat.regression('linear', data);
//
//     myRegression.points.sort(function (a, b) {
//         return a[0] - b[0];
//     });
//
//     option = {
//         title: {
//             subtext: '根据最近的房价，预测价格走势',
//             left: 'center',
//         },
//
//         tooltip: {
//             trigger: 'axis',
//             axisPointer: {
//                 type: 'cross'
//             }
//         },
//
//         grid: {
//             show: true,//是否显示直角坐标系的网格,true显示，false不显示
//             left: '13%',//grid组件离容器左侧的距离
//             containLabel: false,//grid 区域是否包含坐标轴的刻度标签，在无法确定坐标轴标签的宽度，容器有比较小无法预留较多空间的时候，可以设为 true 防止标签溢出容器。
//
//         },
//
//
//         xAxis: {
//             type: 'value',
//             height: '100px',
//             splitLine: {
//                 lineStyle: {
//                     type: 'dashed'
//                 }
//             },
//         },
//         yAxis: {
//             type: 'value',
//             min: 1.5,
//             splitLine: {
//                 lineStyle: {
//                     type: 'dashed'
//                 }
//             },
//         },
//         series: [{
//             name: '分散值(实际值)',
//             type: 'scatter',
//             label: {
//                 emphasis: {
//                     show: true,
//                     position: 'left',
//                     textStyle: {
//                         color: 'blue',
//                         fontSize: 12
//                     }
//                 }
//             },
//             data: data
//         }, {
//             name: '线性值(预测值)',
//             type: 'line',
//             showSymbol: false,
//             data: myRegression.points,
//             markPoint: {
//                 itemStyle: {
//                     normal: {
//                         color: 'transparent'
//                     }
//                 },
//                 label: {
//                     normal: {
//                         show: true,
//                         position: 'left',
//                         formatter: myRegression.expression,
//                         textStyle: {
//                             color: '#333',
//                             fontSize: 12
//                         }
//                     }
//                 },
//                 data: [{
//                     coord: myRegression.points[myRegression.points.length - 1]
//                 }]
//             }
//         }]
//     };
//     center1.setOption(option, true);
//
// }
function getdata1(data) {
    var myChart = echarts.init(document.getElementById('f_line'), 'dark-purple');
    
    // 计算线性回归
    var myRegression = ecStat.regression('linear', data);
    myRegression.points.sort(function(a, b) {
        return a[0] - b[0];
    });
    
    var option = {
        title: {
            text: '房价走势分析',
            subtext: '基于历史数据预测'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            data: ['实际房价', '预测走势']
        },
        grid: [{
            left: '3%',
            right: '3%',
            bottom: '53%',
            containLabel: true
        }, {
            left: '3%',
            right: '3%',
            top: '55%',
            height: '35%'
        }],
        xAxis: [{
            type: 'value',
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            }
        }, {
            gridIndex: 1,
            type: 'value',
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },
            show: false
        }],
        yAxis: [{
            type: 'value',
            name: '价格（元/月）',
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            }
        }, {
            gridIndex: 1,
            type: 'value',
            name: '价格（元/月）',
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },
            show: false
        }],
        series: [{
            name: '实际房价',
            type: 'scatter',
            data: data,
            symbolSize: 10,
            itemStyle: {
                opacity: 0.7
            }
        }, {
            name: '预测走势',
            type: 'line',
            smooth: true,
            data: myRegression.points,
            symbolSize: 0.1,
            lineStyle: {
                width: 2
            },
            markPoint: {
                label: {
                    show: true,
                    position: 'top',
                    formatter: myRegression.expression,
                    color: '#fff',
                    backgroundColor: 'rgba(154, 104, 242, 0.8)',
                    padding: [5, 10],
                    borderRadius: 5
                },
                data: [{
                    coord: myRegression.points[myRegression.points.length - 1]
                }]
            }
        }, {
            name: '数据表格',
            type: 'custom',
            renderItem: function(params, api) {
                var data = params.dataIndex >= myRegression.points.length ? 
                    data[params.dataIndex - myRegression.points.length] :
                    myRegression.points[params.dataIndex];
                return {
                    type: 'group',
                    children: [{
                        type: 'rect',
                        shape: {
                            x: api.coord([data[0], data[1]])[0] - 40,
                            y: api.coord([data[0], data[1]])[1] - 10,
                            width: 80,
                            height: 20
                        },
                        style: {
                            fill: 'rgba(154, 104, 242, 0.1)'
                        }
                    }, {
                        type: 'text',
                        style: {
                            text: data[0].toFixed(2) + ',' + data[1].toFixed(2),
                            textAlign: 'center',
                            textVerticalAlign: 'middle',
                            x: api.coord([data[0], data[1]])[0],
                            y: api.coord([data[0], data[1]])[1],
                            fill: '#fff'
                        }
                    }]
                };
            },
            data: data.concat(myRegression.points),
            gridIndex: 1,
            z: 100
        }]
    };
    
    myChart.setOption(option);
    
    // 创建数据表格
    var tableHtml = '<div class="data-table-container" style="margin-top: 20px; padding: 15px; background: rgba(39, 41, 61, 0.8); border-radius: 10px;">' +
        '<h4 style="color: #fff; margin-bottom: 15px;">房价数据明细</h4>' +
        '<div style="max-height: 300px; overflow-y: auto;">' +
        '<table class="table table-dark table-hover" style="background: transparent;">' +
        '<thead><tr><th>序号</th><th>时间点</th><th>实际价格</th><th>预测价格</th><th>差异</th></tr></thead>' +
        '<tbody>';
    
    data.forEach(function(item, index) {
        var predictedPrice = myRegression.points[index][1];
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
    
    // 在图表容器后插入表格
    document.getElementById('f_line').insertAdjacentHTML('afterend', tableHtml);
    
    // 响应式调整
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}