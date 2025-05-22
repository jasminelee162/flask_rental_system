function column_chart(data) {
    // 数据验证和转换
    try {
        // 如果数据是对象而不是数组，尝试转换
        if (typeof data === 'object' && !Array.isArray(data)) {
            console.log('原始数据:', data);
            // 如果数据在data字段中
            if (data.data && Array.isArray(data.data)) {
                data = data.data;
            } else {
                // 尝试将对象转换为数组
                data = Object.entries(data).map(([key, value]) => [key, value]);
            }
        }

        // 确保数据是数组格式
        if (!Array.isArray(data)) {
            throw new Error('数据必须是数组格式');
        }

        // 确保数据不为空
        if (data.length === 0) {
            throw new Error('数据数组为空');
        }

        // 验证数据格式
        const isValidData = data.every(item => 
            Array.isArray(item) && 
            item.length === 2 && 
            typeof item[0] !== 'undefined' && 
            typeof item[1] !== 'undefined'
        );

        if (!isValidData) {
            throw new Error('数据格式不正确，每项必须包含名称和值');
        }

        console.log('处理后的数据:', data);

        // 确保容器存在
        const container = document.getElementById('scolumn_line');
        if (!container) {
            throw new Error('图表容器不存在');
        }

        // 清除可能存在的旧实例
        echarts.dispose(container);

        // 初始化图表
        const myChart = echarts.init(container, 'dark-purple');
        
        // 设置容器样式
        container.style.width = '100%';
        container.style.height = '380px';

        // 数据处理
        const chartData = data.map(item => ({
            name: String(item[0]),
            value: Number(item[1]) || 0
        }));

        // 图表配置
        const option = {
            title: {
                text: '小区房源数量TOP20',
                subtext: '当前区域热门小区',
                left: 'center',
                top: '3%',
                textStyle: {
                    color: '#fff',
                    fontSize: 16,
                    fontWeight: 'normal'
                },
                subtextStyle: {
                    color: 'rgba(255, 255, 255, 0.7)',
                    fontSize: 12
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                },
                formatter: '{b}: {c} 套',
                backgroundColor: 'rgba(39, 41, 61, 0.95)',
                borderColor: 'rgba(154, 104, 242, 0.3)',
                borderWidth: 1,
                padding: [8, 12],
                textStyle: {
                    color: '#fff'
                }
            },
            grid: {
                left: '5%',
                right: '5%',
                bottom: '15%',
                top: '20%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: chartData.map(item => item.name),
                axisLabel: {
                    interval: 0,
                    rotate: 45,
                    color: 'rgba(255, 255, 255, 0.7)',
                    fontSize: 10,
                    formatter: function(value) {
                        return value.length > 8 ? value.substring(0, 8) + '...' : value;
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    }
                },
                axisTick: {
                    alignWithLabel: true,
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    }
                }
            },
            yAxis: {
                type: 'value',
                name: '房源数量',
                nameTextStyle: {
                    color: 'rgba(255, 255, 255, 0.7)',
                    fontSize: 12,
                    padding: [0, 0, 0, 30]
                },
                axisLabel: {
                    color: 'rgba(255, 255, 255, 0.7)',
                    formatter: '{value} 套'
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.2)'
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        type: 'dashed'
                    }
                }
            },
            series: [{
                name: '房源数量',
                type: 'bar',
                data: chartData.map(item => item.value),
                barWidth: '60%',
                itemStyle: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(154, 104, 242, 0.8)'
                        }, {
                            offset: 1,
                            color: 'rgba(154, 104, 242, 0.2)'
                        }]
                    },
                    borderRadius: [5, 5, 0, 0]
                },
                emphasis: {
                    itemStyle: {
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0,
                                color: 'rgba(154, 104, 242, 1)'
                            }, {
                                offset: 1,
                                color: 'rgba(154, 104, 242, 0.5)'
                            }]
                        }
                    }
                },
                animationDelay: function(idx) {
                    return idx * 50;
                }
            }],
            animation: true,
            animationDuration: 1000,
            animationEasing: 'cubicOut'
        };

        // 设置图表选项
        myChart.setOption(option);
        console.log('图表初始化完成');

        // 监听窗口大小变化
        window.addEventListener('resize', function() {
            if (myChart && !myChart.isDisposed()) {
                myChart.resize();
            }
        });

        // 监听图表点击事件
        myChart.on('click', function(params) {
            console.log('点击了图表项:', params);
        });

    } catch (error) {
        console.error('图表初始化失败:', error);
        const container = document.getElementById('scolumn_line');
        if (container) {
            container.innerHTML = `
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    text-align: center;
                    color: rgba(255,255,255,0.7);
                    width: 100%;
                    padding: 20px;
                ">
                    <i class="fa fa-exclamation-circle" style="font-size: 24px; color: #ff6b6b;"></i>
                    <p style="margin-top: 10px;">图表加载失败: ${error.message}</p>
                    <p style="font-size: 12px; margin-top: 5px;">请刷新页面重试</p>
                </div>
            `;
        }
    }
}