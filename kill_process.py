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


def get_process_pid(process_name):
    """获取进程PID"""
    try:
        result = subprocess.run(
            ['adb', 'shell', 'pidof', process_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        pid = result.stdout.strip()
        if pid:
            return pid
    except Exception as e:
        print(f"查找进程出错: {e}")
    return None


def kill_process(process_name):
    """杀死进程"""
    pid = get_process_pid(process_name)
    if pid:
        try:
            subprocess.run(
                ['adb', 'shell', 'kill', '-9', pid],
                capture_output=True,
                timeout=10
            )
            print(f"已杀死进程 {process_name} (PID: {pid})")
            return True
        except Exception as e:
            print(f"杀死进程出错: {e}")
            return False
    else:
        print(f"未找到进程 {process_name}")
        return False


def format_time(seconds):
    """格式化时间显示"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}小时{minutes}分{secs}秒"
    elif minutes > 0:
        return f"{minutes}分{secs}秒"
    else:
        return f"{secs}秒"


def main():
    parser = argparse.ArgumentParser(description='定时kill进程工具')
    parser.add_argument('wait_time', type=int, help='等待时间（秒）')
    parser.add_argument('--process', '-p', default='com.baidu.naviauto',
                        help='要kill的进程名 (默认: com.baidu.naviauto)')

    args = parser.parse_args()

    process_name = args.process
    wait_seconds = args.wait_time

    if wait_seconds <= 0:
        print("错误: 等待时间必须大于0")
        sys.exit(1)

    print(f"等待 {format_time(wait_seconds)} 后将杀死进程: {process_name}")
    print("-" * 40)

    # 倒计时显示剩余时间
    start_time = time.time()
    last_printed_minute = -1

    while True:
        elapsed = time.time() - start_time
        remaining = wait_seconds - elapsed

        if remaining <= 0:
            break

        # 每秒打印剩余时间
        current_seconds = int(remaining)
        current_minute = current_seconds // 60

        # 只在分钟变化或最后10秒时显示更详细信息
        if current_minute != last_printed_minute or current_seconds <= 10:
            if current_minute > 0:
                print(f"剩余时间: {format_time(remaining)}")
            else:
                print(f"剩余时间: {current_seconds} 秒")
            last_printed_minute = current_minute

        time.sleep(0.5)

    print("-" * 40)
    print("时间到! 开始杀死进程...")

    # 杀死进程
    kill_process(process_name)

    print("执行完成!")


if __name__ == "__main__":
    main()