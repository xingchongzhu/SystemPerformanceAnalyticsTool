import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import base64
from io import BytesIO

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 获取生成的Excel文件
output_dir = './output'
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
    df_swap['抓取时间'] = pd.to_datetime(df_swap['抓取时间'])
    has_swap = True
except:
    has_swap = False

# 转换时间列为datetime类型
df_mem['抓取时间'] = pd.to_datetime(df_mem['抓取时间'])
df_cpu['抓取时间'] = pd.to_datetime(df_cpu['抓取时间'])

# 为图表绘制保留原始datetime对象的副本
mem_time_for_chart = df_mem['抓取时间'].copy()
cpu_time_for_chart = df_cpu['抓取时间'].copy()

# 设置原始数据的时间格式显示到秒
df_mem['抓取时间'] = df_mem['抓取时间'].dt.strftime('%Y-%m-%d %H:%M:%S')
df_cpu['抓取时间'] = df_cpu['抓取时间'].dt.strftime('%Y-%m-%d %H:%M:%S')

# 计算统计信息
mem_stats = df_mem.describe()
cpu_stats = df_cpu.describe()

# 百度导航的统计信息
baidu_mem_stats = df_mem['百度导航内存(M)'].describe()
baidu_cpu_stats = df_cpu['百度导航CPU(%)'].describe()

# 生成图表的函数，确保时间刻度显示每一个点
def generate_chart_as_base64(fig, time_data):
    # 获取当前的轴
    ax = fig.gca()
    
    # 设置x轴刻度显示所有数据点
    if hasattr(ax, 'xaxis') and time_data is not None:
        # 设置所有时间点为刻度
        ax.set_xticks(time_data)
        
        # 设置时间格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        
        # 旋转标签以便更好地显示，使用更小的字体
        plt.xticks(rotation=60, ha='right', fontsize=6)
    
    # 保存图表
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{image_base64}"

# -------------------- 内存使用情况图表 --------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(mem_time_for_chart, df_mem['已用内存(M)'], label='已用内存(M)', marker='o', markersize=3, linewidth=1.5)
ax.plot(mem_time_for_chart, df_mem['可用内存(M)'], label='可用内存(M)', marker='s', markersize=3, linewidth=1.5)
ax.plot(mem_time_for_chart, df_mem['缓冲区(M)'], label='缓冲区(M)', marker='^', markersize=3, linewidth=1.5)
ax.plot(mem_time_for_chart, df_mem['百度导航内存(M)'], label='百度导航内存(M)', marker='D', markersize=3, linewidth=1.5, color='red')
ax.set_title('内存使用情况趋势图', fontsize=14, fontweight='bold')
ax.set_xlabel('时间', fontsize=12)
ax.set_ylabel('内存大小 (MB)', fontsize=12)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper right', fontsize=10)
plt.tight_layout()
mem_chart_base64 = generate_chart_as_base64(fig, mem_time_for_chart)

# -------------------- CPU使用情况图表 --------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(cpu_time_for_chart, df_cpu['CPU总使用率(%)'], label='CPU总使用率(%)', marker='o', markersize=3, linewidth=1.5)
ax.plot(cpu_time_for_chart, df_cpu['用户态CPU(%)'], label='用户态CPU(%)', marker='s', markersize=3, linewidth=1.5)
ax.plot(cpu_time_for_chart, df_cpu['系统态CPU(%)'], label='系统态CPU(%)', marker='^', markersize=3, linewidth=1.5)
ax.plot(cpu_time_for_chart, df_cpu['空闲CPU(%)'], label='空闲CPU(%)', marker='v', markersize=3, linewidth=1.5)
ax.plot(cpu_time_for_chart, df_cpu['百度导航CPU(%)'], label='百度导航CPU(%)', marker='D', markersize=3, linewidth=1.5, color='red')
ax.set_title('CPU使用情况趋势图', fontsize=14, fontweight='bold')
ax.set_xlabel('时间', fontsize=12)
ax.set_ylabel('CPU使用率 (%)', fontsize=12)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper right', fontsize=10)
plt.tight_layout()
cpu_chart_base64 = generate_chart_as_base64(fig, cpu_time_for_chart)

# -------------------- 百度导航性能图表 --------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
ax1.plot(mem_time_for_chart, df_mem['百度导航内存(M)'], label='百度导航内存(M)', marker='o', markersize=3, linewidth=1.5, color='red')
ax1.set_title('百度导航内存使用趋势', fontsize=12, fontweight='bold')
ax1.set_ylabel('内存大小 (MB)', fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(loc='upper right', fontsize=9)
ax2.plot(cpu_time_for_chart, df_cpu['百度导航CPU(%)'], label='百度导航CPU(%)', marker='s', markersize=3, linewidth=1.5, color='blue')
ax2.set_title('百度导航CPU使用趋势', fontsize=12, fontweight='bold')
ax2.set_xlabel('时间', fontsize=10)
ax2.set_ylabel('CPU使用率 (%)', fontsize=10)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(loc='upper right', fontsize=9)
plt.tight_layout()
baidu_chart_base64 = generate_chart_as_base64(fig, mem_time_for_chart)

# 如果有交换空间数据，生成交换空间图表
if has_swap:
    # 为交换空间图表保留原始datetime对象
    swap_time_for_chart = df_swap['抓取时间'].copy()
    # 设置交换空间数据的时间格式显示到秒
    df_swap['抓取时间'] = df_swap['抓取时间'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(swap_time_for_chart, df_swap['已用交换空间(M)'], label='已用交换空间(M)', marker='o', markersize=3, linewidth=1.5, color='purple')
    ax.plot(swap_time_for_chart, df_swap['缓存(M)'], label='缓存(M)', marker='s', markersize=3, linewidth=1.5, color='green')
    ax.set_title('交换空间使用情况趋势图', fontsize=14, fontweight='bold')
    ax.set_xlabel('时间', fontsize=12)
    ax.set_ylabel('大小 (MB)', fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', fontsize=10)
    plt.tight_layout()
    swap_chart_base64 = generate_chart_as_base64(fig, swap_time_for_chart)
    
    # 预计算交换空间部分的HTML
    swap_section_html = f"""
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
        <img src="{swap_chart_base64}" alt="交换空间使用情况趋势图">
    </div>
    
    <h3>交换空间统计信息</h3>
    <div class="data-sample">
        {df_swap.describe().to_html(classes='stats-table', na_rep='-', float_format='%.2f')}
    </div>
    """
    
    # 预计算交换空间数据样本的HTML
    swap_data_sample = f"""
    <h3>交换空间数据前10行</h3>
    <div class="data-sample">
        {df_swap.head(10).to_html(classes='data-table', index=False, na_rep='-', float_format='%.2f')}
    </div>
    """
else:
    swap_section_html = ""
    swap_data_sample = ""

# 生成HTML报告
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>系统性能监控报告</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 2px solid #4CAF50;
        }}
        h2 {{
            color: #4CAF50;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
            padding-left: 10px;
        }}
        h3 {{
            color: #555;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        .chart-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        th, td {{
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #e8f5e9;
        }}
        .summary-stats {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            flex: 1;
            min-width: 200px;
            background-color: #e8f5e9;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        .stat-card h4 {{
            margin: 0 0 10px 0;
            color: #333;
            font-size: 14px;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }}
        .nav-menu {{
            text-align: center;
            margin: 30px 0;
        }}
        .nav-menu a {{
            display: inline-block;
            padding: 10px 20px;
            margin: 0 10px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }}
        .nav-menu a:hover {{
            background-color: #45a049;
        }}
        .data-sample {{
            margin: 20px 0;
            overflow-x: auto;
        }}
        .report-info {{
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 4px solid #2196F3;
        }}
        .report-info p {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>系统性能监控报告</h1>
        
        <div class="report-info">
            <p><strong>报告生成时间:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>数据来源:</strong> {os.path.basename(excel_file)}</p>
            <p><strong>数据点数量:</strong> {len(df_mem)} 个</p>
            <p><strong>监控时间段:</strong> {mem_time_for_chart.min().strftime('%Y-%m-%d %H:%M:%S')} 至 {mem_time_for_chart.max().strftime('%Y-%m-%d %H:%M:%S')}</p>
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
                    <div class="stat-value">{mem_stats['已用内存(M)']['mean']:.2f} MB</div>
                </div>
                <div class="stat-card">
                    <h4>平均可用内存</h4>
                    <div class="stat-value">{mem_stats['可用内存(M)']['mean']:.2f} MB</div>
                </div>
                <div class="stat-card">
                    <h4>平均缓冲区</h4>
                    <div class="stat-value">{mem_stats['缓冲区(M)']['mean']:.2f} MB</div>
                </div>
                <div class="stat-card">
                    <h4>平均百度导航内存</h4>
                    <div class="stat-value">{baidu_mem_stats['mean']:.2f} MB</div>
                </div>
            </div>

            <div class="chart-container">
                <h3>内存使用趋势</h3>
                <img src="{mem_chart_base64}" alt="内存使用情况趋势图">
            </div>

            <h3>内存统计信息</h3>
            <div class="data-sample">
                {mem_stats.to_html(classes='stats-table', na_rep='-', float_format='%.2f')}
            </div>
        </section>

        <!-- CPU分析 -->
        <section id="cpu">
            <h2>CPU使用情况分析</h2>
            
            <div class="summary-stats">
                <div class="stat-card">
                    <h4>平均用户态CPU</h4>
                    <div class="stat-value">{cpu_stats['用户态CPU(%)']['mean']:.2f} %</div>
                </div>
                <div class="stat-card">
                    <h4>平均系统态CPU</h4>
                    <div class="stat-value">{cpu_stats['系统态CPU(%)']['mean']:.2f} %</div>
                </div>
                <div class="stat-card">
                    <h4>平均空闲CPU</h4>
                    <div class="stat-value">{cpu_stats['空闲CPU(%)']['mean']:.2f} %</div>
                </div>
                <div class="stat-card">
                    <h4>平均百度导航CPU</h4>
                    <div class="stat-value">{baidu_cpu_stats['mean']:.2f} %</div>
                </div>
            </div>

            <div class="chart-container">
                <h3>CPU使用趋势</h3>
                <img src="{cpu_chart_base64}" alt="CPU使用情况趋势图">
            </div>

            <h3>CPU统计信息</h3>
            <div class="data-sample">
                {cpu_stats.to_html(classes='stats-table', na_rep='-', float_format='%.2f')}
            </div>
        </section>

        <!-- 百度导航性能 -->
        <section id="baidu">
            <h2>百度导航性能分析</h2>
            
            <div class="summary-stats">
                <div class="stat-card">
                    <h4>百度导航内存最大值</h4>
                    <div class="stat-value">{baidu_mem_stats['max']:.2f} MB</div>
                </div>
                <div class="stat-card">
                    <h4>百度导航内存最小值</h4>
                    <div class="stat-value">{baidu_mem_stats['min']:.2f} MB</div>
                </div>
                <div class="stat-card">
                    <h4>百度导航CPU最大值</h4>
                    <div class="stat-value">{baidu_cpu_stats['max']:.2f} %</div>
                </div>
                <div class="stat-card">
                    <h4>百度导航CPU最小值</h4>
                    <div class="stat-value">{baidu_cpu_stats['min']:.2f} %</div>
                </div>
            </div>

            <div class="chart-container">
                <h3>百度导航性能趋势</h3>
                <img src="{baidu_chart_base64}" alt="百度导航性能趋势图">
            </div>
        </section>

        <!-- 交换空间 -->
        <section id="swap">
            <h2>交换空间使用情况</h2>
            
            {swap_section_html if has_swap else "<p>未收集交换空间数据</p>"}
        </section>

        <!-- 原始数据 -->
        <section id="data">
            <h2>原始数据样本</h2>
            
            <h3>内存数据前10行</h3>
            <div class="data-sample">
                {df_mem.head(10).to_html(classes='data-table', index=False, na_rep='-', float_format='%.2f')}
            </div>

            <h3>CPU数据前10行</h3>
            <div class="data-sample">
                {df_cpu.head(10).to_html(classes='data-table', index=False, na_rep='-', float_format='%.2f')}
            </div>

            <!-- 交换空间数据前10行 -->
            {swap_data_sample if has_swap else ""}
        </section>

        <footer>
            <p style="text-align: center; margin-top: 50px; color: #666; font-size: 14px;">
                系统性能监控报告 | 生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </footer>
    </div>
</body>
</html>"""

# 获取原始日志文件名（从Excel文件名推断）
original_log_name = os.path.splitext(os.path.basename(excel_file))[0]

# 保存HTML报告，使用与日志文件相同的名称
html_output_file = os.path.join(output_dir, f'{original_log_name}.html')
with open(html_output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML报告已生成: {html_output_file}")
print("您可以直接在浏览器中打开该文件查看报告")
