#!/bin/bash
# 功能：实时抓取Android系统性能数据（dumpsys），每条数据带时间戳
# 适用：Android车机/手机，无需root

# ===================== 配置项（可修改） =====================
INTERVAL=5          # 抓取间隔（秒），默认5秒
DURATION=0          # 抓取时长（秒），0表示无限抓取（按Ctrl+C终止）
OUTPUT_FILE="sys_perf_$(date +%Y%m%d_%H%M%S).log"  # 输出日志名（带时间戳）
# ============================================================

# ========== 新增：终端实时打印启动信息 ==========
echo -e "\033[32m===== 系统性能抓取脚本启动 =====\033[0m"
echo -e "\033[32m抓取间隔：${INTERVAL}秒 | 输出文件：$OUTPUT_FILE\033[0m"
echo -e "\033[32m启动时间：$(date "+%Y-%m-%d %H:%M:%S")\033[0m"
echo -e "\033[33m提示：按Ctrl+C终止抓取，所有数据已写入日志文件\033[0m"

# 日志文件写入启动信息（保留原逻辑）
echo "===== 系统性能抓取脚本启动 =====" >> $OUTPUT_FILE
echo "抓取间隔：${INTERVAL}秒 | 输出文件：$OUTPUT_FILE" >> $OUTPUT_FILE
echo "启动时间：$(date "+%Y-%m-%d %H:%M:%S")" >> $OUTPUT_FILE
echo "================================" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# 计算结束时间（如果设置了DURATION）
if [ $DURATION -gt 0 ]; then
    END_TIME=$(( $(date +%s) + DURATION ))
    # ========== 新增：终端提示抓取时长 ==========
    echo -e "\033[32m抓取时长：${DURATION}秒，将自动终止\033[0m"
fi

# 主循环：周期性抓取数据
while true; do
    # 1. 记录当前抓取时间（精确到毫秒）
    CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S.%3N")
    # ========== 新增：终端提示正在抓取 ==========
    echo -e "\n\033[36m[${CURRENT_TIME}] 正在抓取性能数据...\033[0m"
    
    # 日志文件写入抓取时间
    echo "===== 抓取时间：$CURRENT_TIME =====" >> $OUTPUT_FILE

    # 2. 抓取核心性能数据（dumpsys）
    echo -e "\n【1. 内存状态】" >> $OUTPUT_FILE
    adb shell dumpsys meminfo | head -20 >> $OUTPUT_FILE  # 系统内存总览

    echo -e "\n【2. CPU状态】" >> $OUTPUT_FILE
    adb shell dumpsys cpuinfo | head -30 >> $OUTPUT_FILE  # CPU占用（前30行）

    echo -e "\n【3. 进程内存（TOP 10）】" >> $OUTPUT_FILE
    adb shell dumpsys meminfo -t | head -15 >> $OUTPUT_FILE  # 内存占用前10进程

    echo -e "\n【4. 电池状态】" >> $OUTPUT_FILE
    adb shell dumpsys battery >> $OUTPUT_FILE  # 电池/电量（车机可注释）

    echo -e "\n【5. 窗口/应用状态】" >> $OUTPUT_FILE
    adb shell dumpsys window | grep -E "mCurrentFocus|mFocusedApp" >> $OUTPUT_FILE  # 当前前台应用

    # 3. 分隔符
    echo -e "\n----------------------------------------\n" >> $OUTPUT_FILE

    # 4. 检查是否达到结束时间
    if [ $DURATION -gt 0 ] && [ $(date +%s) -ge $END_TIME ]; then
        # ========== 新增：终端提示抓取结束 ==========
        echo -e "\033[32m\n抓取时长已到，脚本终止（结束时间：$(date "+%Y-%m-%d %H:%M:%S")）\033[0m"
        echo "抓取时长已到，脚本终止（结束时间：$(date "+%Y-%m-%d %H:%M:%S")）" >> $OUTPUT_FILE
        break
    fi

    # 5. 等待指定间隔（终端提示等待状态）
    echo -e "\033[35m等待${INTERVAL}秒后进行下一次抓取...（按Ctrl+C终止）\033[0m"
    sleep $INTERVAL
done

# ========== 新增：终端提示脚本结束 ==========
echo -e "\033[32m===== 脚本执行结束 =====\033[0m"
echo -e "\033[32m结束时间：$(date "+%Y-%m-%d %H:%M:%S")\033[0m"
echo -e "\033[32m性能数据已保存至：$OUTPUT_FILE\033[0m"

# 日志文件写入结束信息
echo "===== 脚本执行结束 =====" >> $OUTPUT_FILE
echo "结束时间：$(date "+%Y-%m-%d %H:%M:%S")" >> $OUTPUT_FILE