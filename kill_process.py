#!/usr/bin/env python3
"""
定时kill进程工具
指定等待时间后，自动kill掉com.baidu.naviauto进程，并打印剩余时间
支持在kill前截图和流量数据截图
"""

import os
import sys
import time
import signal
import argparse
import subprocess
from pathlib import Path


def ensure_adb_env():
    """确保adb环境变量已加载"""
    env = os.environ.copy()
    try:
        result = subprocess.run(
            ['bash', '-l', '-c', 'echo $PATH'],
            capture_output=True,
            text=True,
            timeout=10
        )
        env['PATH'] = result.stdout.strip()
    except:
        pass
    return env


def take_screenshot(output_path, filename):
    """截取屏幕截图"""
    env = ensure_adb_env()
    remote_path = "/sdcard/temp_screenshot.png"
    local_path = os.path.join(output_path, filename)

    try:
        # 执行截图
        subprocess.run(
            ['adb', 'shell', 'screencap', '-p', remote_path],
            env=env,
            capture_output=True,
            timeout=10
        )

        # 拉取到本地
        subprocess.run(
            ['adb', 'pull', remote_path, local_path],
            env=env,
            capture_output=True,
            timeout=30
        )

        # 删除远程临时文件
        subprocess.run(
            ['adb', 'shell', 'rm', remote_path],
            env=env,
            capture_output=True
        )

        if os.path.exists(local_path):
            print(f"截图已保存: {local_path}")
            return True
    except Exception as e:
        print(f"截图失败: {e}")
    return False


def open_traffic_settings(process_name):
    """打开系统设置中的流量使用页面"""
    env = ensure_adb_env()

    try:
        # 尝试打开流量使用统计页面
        # 不同Android版本可能路径不同，尝试多个路径
        commands = [
            # 尝试打开设置应用详情页（流量相关）
            ['adb', 'shell', 'am', 'start', '-a', 'android.settings.DATA_USAGE_SETTINGS'],
            # 备用方案：打开应用信息页面
            ['adb', 'shell', 'am', 'start', '-a', 'android.settings.APPLICATION_SETTINGS'],
        ]

        for cmd in commands:
            result = subprocess.run(
                cmd + ['--user', '0'],
                env=env,
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                print("已打开系统设置页面")
                time.sleep(2)  # 等待页面加载
                return True

    except Exception as e:
        print(f"打开设置页面失败: {e}")

    return False


def kill_process(process_name):
    """杀死进程"""
    env = ensure_adb_env()
    try:
        subprocess.run(
            ['adb', 'shell', 'am', 'force-stop', process_name],
            env=env,
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

    # 创建截图输出目录
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'screenshot')
    os.makedirs(output_dir, exist_ok=True)

    # 生成带时间戳的文件名
    timestamp = time.strftime('%Y%m%d_%H%M%S')

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
    print("时间到! 开始执行截图和流量数据采集...")

    # 步骤1: 截取当前屏幕
    print("\n[1/3] 截取当前屏幕...")
    screenshot_file = f"screen_{timestamp}.png"
    take_screenshot(output_dir, screenshot_file)

    # 步骤2: 打开流量设置页面
    print("\n[2/3] 打开流量使用统计页面...")
    open_traffic_settings(process_name)

    # 等待用户切换到流量页面
    print("请手动切换到百度导航的流量使用页面...")
    print("按回车键继续截图流量数据...")
    input()

    # 步骤3: 截取流量页面
    print("\n[3/3] 截取流量使用页面...")
    traffic_screenshot_file = f"traffic_{timestamp}.png"
    take_screenshot(output_dir, traffic_screenshot_file)

    # 步骤4: 杀死进程
    print("\n[4/4] 杀死进程...")
    kill_process(process_name)

    print("\n执行完成!")
    print(f"截图保存在: {output_dir}")


if __name__ == "__main__":
    main()