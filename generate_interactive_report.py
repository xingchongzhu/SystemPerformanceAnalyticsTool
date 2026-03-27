import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import os
import argparse

# 设置中文字体配置
go.Figure().layout.font = dict(family="SimHei, Arial Unicode MS", size=12)

# 解析命令行参数
parser = argparse.ArgumentParser(description='生成交互式性能报告')
parser.add_argument('--excel', type=str, help='要处理的Excel文件路径')
args = parser.parse_args()

# 获取生成的Excel文件
output_dir = './output'

if args.excel:
    # 使用命令行参数指定的Excel文件
    excel_file = args.excel
    if not os.path.exists(excel_file):
        print(f"指定的Excel文件不存在: {excel_file}")
        exit()
else:
    # 处理默认情况，获取第一个Excel文件
    excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx')]
    
    if not excel_files:
        print("没有找到Excel文件")
        exit()
    
    # 读取第一个Excel文件（假设只有一个）
    excel_file = os.path.join(output_dir, excel_files[0])

# 读取内存数据
df_mem = pd.read_excel(excel_file, sheet_name='内存数据')
# 读取CPU数据
df_cpu = pd.read_excel(excel_file, sheet_name='CPU数据')
# 读取交换空间数据（如果存在）
try:
    df_swap = pd.read_excel(excel_file, sheet_name='交换空间数据')
    has_swap = True
except:
    has_swap = False

# 转换时间列为datetime类型
df_mem['抓取时间'] = pd.to_datetime(df_mem['抓取时间'])
df_cpu['抓取时间'] = pd.to_datetime(df_cpu['抓取时间'])
if has_swap:
    df_swap['抓取时间'] = pd.to_datetime(df_swap['抓取时间'])

# 设置时间格式显示到秒
df_mem['时间显示'] = df_mem['抓取时间'].dt.strftime('%Y-%m-%d %H:%M:%S')
df_cpu['时间显示'] = df_cpu['抓取时间'].dt.strftime('%Y-%m-%d %H:%M:%S')
if has_swap:
    df_swap['时间显示'] = df_swap['抓取时间'].dt.strftime('%Y-%m-%d %H:%M:%S')

# 计算统计信息
mem_stats = df_mem.describe()
cpu_stats = df_cpu.describe()

# 百度导航的统计信息
baidu_mem_stats = df_mem['百度导航内存(M)'].describe()
baidu_cpu_stats = df_cpu['百度导航CPU(%)'].describe()

# -------------------- 内存使用情况图表（交互式）--------------------
fig_mem = go.Figure()

# 添加内存数据系列
fig_mem.add_trace(go.Scatter(
    x=df_mem['时间显示'],
    y=df_mem['已用内存(M)'],
    mode='lines+markers',
    name='已用内存(M)',
    line=dict(color='blue', width=1.5),
    marker=dict(size=4, color='blue')
))

fig_mem.add_trace(go.Scatter(
    x=df_mem['时间显示'],
    y=df_mem['可用内存(M)'],
    mode='lines+markers',
    name='可用内存(M)',
    line=dict(width=1.5),
    marker=dict(size=4)
))

fig_mem.add_trace(go.Scatter(
    x=df_mem['时间显示'],
    y=df_mem['缓冲区(M)'],
    mode='lines+markers',
    name='缓冲区(M)',
    line=dict(width=1.5),
    marker=dict(size=4)
))

fig_mem.add_trace(go.Scatter(
    x=df_mem['时间显示'],
    y=df_mem['百度导航内存(M)'],
    mode='lines+markers',
    name='百度导航内存(M)',
    line=dict(color='purple', width=1.5),
    marker=dict(size=4, color='purple')
))

# 设置图表属性
fig_mem.update_layout(
    title='内存使用情况趋势图',
    xaxis_title='时间',
    yaxis_title='内存大小 (MB)',
    template='plotly_white',
    height=600,
    width=1200,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_tickangle=45,
    hovermode='x unified'
)

# -------------------- CPU使用情况图表（交互式）--------------------
fig_cpu = go.Figure()

# 添加CPU数据系列
fig_cpu.add_trace(go.Scatter(
    x=df_cpu['时间显示'],
    y=df_cpu['CPU总使用率(%)'],
    mode='lines+markers',
    name='CPU总使用率(%)',
    line=dict(width=1.5),
    marker=dict(size=4)
))

fig_cpu.add_trace(go.Scatter(
    x=df_cpu['时间显示'],
    y=df_cpu['用户态CPU(%)'],
    mode='lines+markers',
    name='用户态CPU(%)',
    line=dict(color='blue', width=1.5),
    marker=dict(size=4, color='blue')
))

fig_cpu.add_trace(go.Scatter(
    x=df_cpu['时间显示'],
    y=df_cpu['系统态CPU(%)'],
    mode='lines+markers',
    name='系统态CPU(%)',
    line=dict(width=1.5),
    marker=dict(size=4)
))

fig_cpu.add_trace(go.Scatter(
    x=df_cpu['时间显示'],
    y=df_cpu['空闲CPU(%)'],
    mode='lines+markers',
    name='空闲CPU(%)',
    line=dict(width=1.5),
    marker=dict(size=4)
))

fig_cpu.add_trace(go.Scatter(
    x=df_cpu['时间显示'],
    y=df_cpu['百度导航CPU(%)'],
    mode='lines+markers',
    name='百度导航CPU(%)',
    line=dict(color='red', width=1.5),
    marker=dict(size=4, color='red')
))

# 设置图表属性
fig_cpu.update_layout(
    title='CPU使用情况趋势图',
    xaxis_title='时间',
    yaxis_title='CPU使用率 (%)',
    template='plotly_white',
    height=600,
    width=1200,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_tickangle=45,
    hovermode='x unified'
)

# -------------------- 百度导航性能图表（交互式）--------------------
# 创建子图
fig_baidu = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                           subplot_titles=('百度导航内存使用趋势', '百度导航CPU使用趋势'))

# 添加百度导航内存数据
fig_baidu.add_trace(go.Scatter(
    x=df_mem['时间显示'],
    y=df_mem['百度导航内存(M)'],
    mode='lines+markers',
    name='百度导航内存(M)',
    line=dict(color='red', width=1.5),
    marker=dict(size=4, color='red')
), row=1, col=1)

# 添加百度导航CPU数据
fig_baidu.add_trace(go.Scatter(
    x=df_cpu['时间显示'],
    y=df_cpu['百度导航CPU(%)'],
    mode='lines+markers',
    name='百度导航CPU(%)',
    line=dict(color='blue', width=1.5),
    marker=dict(size=4, color='blue')
), row=2, col=1)

# 设置图表属性
fig_baidu.update_layout(
    template='plotly_white',
    height=800,
    width=1200,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode='x unified'
)

fig_baidu.update_xaxes(title_text='时间', tickangle=45, row=2, col=1)
fig_baidu.update_yaxes(title_text='内存大小 (MB)', row=1, col=1)
fig_baidu.update_yaxes(title_text='CPU使用率 (%)', row=2, col=1)

# -------------------- 交换空间图表（交互式，仅当有数据时）--------------------
if has_swap:
    fig_swap = go.Figure()
    
    # 添加交换空间数据系列
    fig_swap.add_trace(go.Scatter(
        x=df_swap['时间显示'],
        y=df_swap['已用交换空间(M)'],
        mode='lines+markers',
        name='已用交换空间(M)',
        line=dict(color='purple', width=1.5),
        marker=dict(size=4, color='purple')
    ))
    
    fig_swap.add_trace(go.Scatter(
        x=df_swap['时间显示'],
        y=df_swap['缓存(M)'],
        mode='lines+markers',
        name='缓存(M)',
        line=dict(color='green', width=1.5),
        marker=dict(size=4, color='green')
    ))
    
    # 设置图表属性
    fig_swap.update_layout(
        title='交换空间使用情况趋势图',
        xaxis_title='时间',
        yaxis_title='大小 (MB)',
        template='plotly_white',
        height=600,
        width=1200,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_tickangle=45,
        hovermode='x unified'
    )

# 生成图表的HTML代码
mem_chart_html = fig_mem.to_html(full_html=False, include_plotlyjs='cdn')
cpu_chart_html = fig_cpu.to_html(full_html=False, include_plotlyjs='cdn')
baidu_chart_html = fig_baidu.to_html(full_html=False, include_plotlyjs='cdn')

# 生成HTML报告
report_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>系统性能监控报告</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 2px solid #4CAF50;
        }
        h2 {
            color: #4CAF50;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
            padding-left: 10px;
        }
        h3 {
            color: #555;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        .chart-container {
            margin: 20px 0;
            text-align: center;
        }
        .chart-container .plotly-graph-div {
            margin: 0 auto;
            max-width: 100%;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #e8f5e9;
        }
        .summary-stats {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            flex: 1;
            min-width: 200px;
            background-color: #e8f5e9;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .stat-card h4 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 14px;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }
        .nav-menu {
            text-align: center;
            margin: 30px 0;
        }
        .nav-menu a {
            display: inline-block;
            padding: 10px 20px;
            margin: 0 10px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .nav-menu a:hover {
            background-color: #45a049;
        }
        .data-sample {
            margin: 20px 0;
            overflow-x: auto;
        }
        .report-info {
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 4px solid #2196F3;
        }
        .report-info p {
            margin: 5px 0;
        }
        .legend-hint {
            color: #666;
            font-size: 14px;
            margin: 10px 0;
            text-align: center;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>系统性能监控报告</h1>
        
        <div class="report-info">
            <p><strong>报告生成时间:</strong> %%GENERATION_TIME%%</p>
            <p><strong>数据来源:</strong> %%DATA_SOURCE%%</p>
            <p><strong>数据点数量:</strong> %%DATA_COUNT%% 个</p>
            <p><strong>监控时间段:</strong> %%TIME_RANGE%%</p>
        </div>

        <div class="nav-menu">
            <a href="#memory">内存分析</a>
            <a href="#cpu">CPU分析</a>
            <a href="#baidu">百度导航性能</a>
            <a href="#swap">交换空间</a>
            <a href="#data">原始数据</a>
        </div>

        <!-- 内存分析 -->
        <section id="memory">
            <h2>内存使用情况分析</h2>
            
            <div class="summary-stats">
                <div class="stat-card">
                    <h4>平均已用内存</h4>
                    <div class="stat-value">%%MEM_AVG_USED%% MB</div>
                </div>
                <div class="stat-card">
                    <h4>平均可用内存</h4>
                    <div class="stat-value">%%MEM_AVG_FREE%% MB</div>
                </div>
                <div class="stat-card">
                    <h4>平均缓冲区</h4>
                    <div class="stat-value">%%MEM_AVG_BUFFER%% MB</div>
                </div>
                <div class="stat-card">
                    <h4>平均百度导航内存</h4>
                    <div class="stat-value">%%BAIDU_AVG_MEM%% MB</div>
                </div>
            </div>

            <div class="chart-container">
                <h3>内存使用趋势</h3>
                <p class="legend-hint">点击图例可以显示/隐藏数据系列</p>
                %%MEM_CHART%%
            </div>

            <h3>内存统计信息</h3>
            <div class="data-sample">
                %%MEM_STATS_TABLE%%
            </div>
        </section>

        <!-- CPU分析 -->
        <section id="cpu">
            <h2>CPU使用情况分析</h2>
            
            <div class="summary-stats">
                <div class="stat-card">
                    <h4>平均用户态CPU</h4>
                    <div class="stat-value">%%CPU_AVG_USER%% %</div>
                </div>
                <div class="stat-card">
                    <h4>平均系统态CPU</h4>
                    <div class="stat-value">%%CPU_AVG_SYS%% %</div>
                </div>
                <div class="stat-card">
                    <h4>平均空闲CPU</h4>
                    <div class="stat-value">%%CPU_AVG_IDLE%% %</div>
                </div>
                <div class="stat-card">
                    <h4>平均百度导航CPU</h4>
                    <div class="stat-value">%%BAIDU_AVG_CPU%% %</div>
                </div>
            </div>

            <div class="chart-container">
                <h3>CPU使用趋势</h3>
                <p class="legend-hint">点击图例可以显示/隐藏数据系列</p>
                %%CPU_CHART%%
            </div>

            <h3>CPU统计信息</h3>
            <div class="data-sample">
                %%CPU_STATS_TABLE%%
            </div>
        </section>

        <!-- 百度导航性能 -->
        <section id="baidu">
            <h2>百度导航性能分析</h2>
            
            <div class="summary-stats">
                <div class="stat-card">
                    <h4>百度导航内存最大值</h4>
                    <div class="stat-value">%%BAIDU_MAX_MEM%% MB</div>
                </div>
                <div class="stat-card">
                    <h4>百度导航内存最小值</h4>
                    <div class="stat-value">%%BAIDU_MIN_MEM%% MB</div>
                </div>
                <div class="stat-card">
                    <h4>百度导航CPU最大值</h4>
                    <div class="stat-value">%%BAIDU_MAX_CPU%% %</div>
                </div>
                <div class="stat-card">
                    <h4>百度导航CPU最小值</h4>
                    <div class="stat-value">%%BAIDU_MIN_CPU%% %</div>
                </div>
            </div>

            <div class="chart-container">
                <h3>百度导航性能趋势</h3>
                <p class="legend-hint">点击图例可以显示/隐藏数据系列</p>
                %%BAIDU_CHART%%
            </div>
        </section>

        <!-- 交换空间 -->
        <section id="swap">
            <h2>交换空间使用情况</h2>
            
            %%SWAP_SECTION%%
        </section>

        <!-- 原始数据 -->
        <section id="data">
            <h2>原始数据样本</h2>
            
            <h3>内存数据前10行</h3>
            <div class="data-sample">
                %%MEM_DATA_SAMPLE%%
            </div>

            <h3>CPU数据前10行</h3>
            <div class="data-sample">
                %%CPU_DATA_SAMPLE%%
            </div>

            %%SWAP_DATA_SAMPLE%%
        </section>

        <footer>
            <p style="text-align: center; margin-top: 50px; color: #666; font-size: 14px;">
                系统性能监控报告 | 生成时间: %%GENERATION_TIME%%
            </p>
        </footer>
    </div>
</body>
</html>
'''

# 准备替换的数据
report_data = {
    'GENERATION_TIME': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
    'DATA_SOURCE': os.path.basename(excel_file),
    'DATA_COUNT': str(len(df_mem)),
    'TIME_RANGE': f"{df_mem['时间显示'].min()} 至 {df_mem['时间显示'].max()}",
    'MEM_AVG_USED': f"{mem_stats['已用内存(M)']['mean']:.2f}",
    'MEM_AVG_FREE': f"{mem_stats['可用内存(M)']['mean']:.2f}",
    'MEM_AVG_BUFFER': f"{mem_stats['缓冲区(M)']['mean']:.2f}",
    'BAIDU_AVG_MEM': f"{baidu_mem_stats['mean']:.2f}",
    'CPU_AVG_USER': f"{cpu_stats['用户态CPU(%)']['mean']:.2f}",
    'CPU_AVG_SYS': f"{cpu_stats['系统态CPU(%)']['mean']:.2f}",
    'CPU_AVG_IDLE': f"{cpu_stats['空闲CPU(%)']['mean']:.2f}",
    'BAIDU_AVG_CPU': f"{baidu_cpu_stats['mean']:.2f}",
    'BAIDU_MAX_MEM': f"{baidu_mem_stats['max']:.2f}",
    'BAIDU_MIN_MEM': f"{baidu_mem_stats['min']:.2f}",
    'BAIDU_MAX_CPU': f"{baidu_cpu_stats['max']:.2f}",
    'BAIDU_MIN_CPU': f"{baidu_cpu_stats['min']:.2f}",
    'MEM_CHART': mem_chart_html,
    'CPU_CHART': cpu_chart_html,
    'BAIDU_CHART': baidu_chart_html,
    'MEM_STATS_TABLE': mem_stats.to_html(classes='stats-table', na_rep='-', float_format='%.2f'),
    'CPU_STATS_TABLE': cpu_stats.to_html(classes='stats-table', na_rep='-', float_format='%.2f'),
    'MEM_DATA_SAMPLE': df_mem.head(10).to_html(classes='data-table', index=False, na_rep='-', float_format='%.2f', columns=['时间显示', '总内存(M)', '已用内存(M)', '可用内存(M)', '缓冲区(M)', '百度导航内存(M)']),
    'CPU_DATA_SAMPLE': df_cpu.head(10).to_html(classes='data-table', index=False, na_rep='-', float_format='%.2f', columns=['时间显示', 'CPU总使用率(%)', '用户态CPU(%)', '系统态CPU(%)', '空闲CPU(%)', '百度导航CPU(%)']),
}

# 处理交换空间部分
if has_swap:
    swap_chart_html = fig_swap.to_html(full_html=False, include_plotlyjs='cdn')
    report_data['SWAP_SECTION'] = f'''
    <div class="summary-stats">
        <div class="stat-card">
            <h4>平均已用交换空间</h4>
            <div class="stat-value">{df_swap['已用交换空间(M)'].mean():.2f} MB</div>
        </div>
        <div class="stat-card">
            <h4>平均缓存</h4>
            <div class="stat-value">{df_swap['缓存(M)'].mean():.2f} MB</div>
        </div>
    </div>

    <div class="chart-container">
        <h3>交换空间使用趋势</h3>
        <p class="legend-hint">点击图例可以显示/隐藏数据系列</p>
        {swap_chart_html}
    </div>
    
    <h3>交换空间统计信息</h3>
    <div class="data-sample">
        {df_swap.describe().to_html(classes='stats-table', na_rep='-', float_format='%.2f')}
    </div>
    '''
    report_data['SWAP_DATA_SAMPLE'] = f'''
    <h3>交换空间数据前10行</h3>
    <div class="data-sample">
        {df_swap.head(10).to_html(classes='data-table', index=False, na_rep='-', float_format='%.2f', columns=['时间显示', '总交换空间(M)', '已用交换空间(M)', '可用交换空间(M)', '缓存(M)'])}
    </div>
    '''
else:
    report_data['SWAP_SECTION'] = '<p>未收集交换空间数据</p>'
    report_data['SWAP_DATA_SAMPLE'] = ''

# 替换HTML模板中的占位符
for key, value in report_data.items():
    report_html = report_html.replace(f'%%{key}%%', value)

# 获取原始日志文件名（从Excel文件名推断）
original_log_name = os.path.splitext(os.path.basename(excel_file))[0]

# 保存HTML报告，使用与日志文件相同的名称
html_output_file = os.path.join(output_dir, f'{original_log_name}.html')
with open(html_output_file, 'w', encoding='utf-8') as f:
    f.write(report_html)

print(f"交互式HTML报告已生成: {html_output_file}")
print("您可以直接在浏览器中打开该文件查看报告")
print("提示：点击图表上方的图例可以显示/隐藏对应的数据系列")
