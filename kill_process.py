#!/usr/bin/env python3
"""
定时kill进程工具
指定等待时间后，自动kill掉com.baidu.naviauto进程，并打印剩余时间
"""

import os
import sys
import time
import signal
import argparse
import subprocess


def kill_process(process_name):
    """杀死进程"""
    try:
        subprocess.run(
            ['adb', 'shell', 'am', 'force-stop', process_name],
            capture_output=True,
            timeout=10
        )
        print(f"已停止进程 {process_name}")
        return True
    except Exception as e:
        print(f"停止进程出错: {e}")
        return False


def format_time(minutes):
    """格式化时间显示"""
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    if hours > 0:
        return f"{hours}小时{mins}分钟"
    else:
        return f"{mins}分钟"


def main():
    parser = argparse.ArgumentParser(description='定时kill进程工具')
    parser.add_argument('wait_time', type=int, help='等待时间（分钟）')
    parser.add_argument('--process', '-p', default='com.baidu.naviauto',
                        help='要kill的进程名 (默认: com.baidu.naviauto)')

    args = parser.parse_args()

    process_name = args.process
    wait_minutes = args.wait_time

    if wait_minutes <= 0:
        print("错误: 等待时间必须大于0")
        sys.exit(1)

    wait_seconds = wait_minutes * 60
    print(f"等待 {wait_minutes} 分钟后将杀死进程: {process_name}")
    print("-" * 40)

    # 倒计时显示剩余时间
    start_time = time.time()
    last_printed_minute = -1

    while True:
        elapsed = time.time() - start_time
        remaining = wait_seconds - elapsed

        if remaining <= 0:
            break

        # 每30秒打印一次剩余时间
        current_seconds = int(remaining)
        current_minute = current_seconds // 60

        if current_minute != last_printed_minute:
            print(f"剩余时间: {current_minute} 分 {current_seconds % 60} 秒")
            last_printed_minute = current_minute

        time.sleep(0.5)

    print("-" * 40)
    print("时间到! 开始杀死进程...")

    # 杀死进程
    kill_process(process_name)

    print("执行完成!")


if __name__ == "__main__":
    main()