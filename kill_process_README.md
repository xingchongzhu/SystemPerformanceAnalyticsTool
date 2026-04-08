# 定时Kill进程工具 (kill_process.py)

## 功能说明

定时kill进程工具可以在指定时间后自动停止指定的Android应用进程，并在执行过程中实时显示剩余时间。

## 使用前提

1. 确保已安装 adb 工具
2. 确保 adb 已添加到系统 PATH 环境变量
3. 确保 Android 设备已通过 USB 或网络连接

## 使用方法

### 基本用法

```bash
# 等待1分钟后停止百度导航
python3 kill_process.py 1
```

### 指定进程名

```bash
# 等待30分钟后停止指定进程
python3 kill_process.py 30 -p com.baidu.naviauto
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `wait_time` | 等待时间（分钟） | 必填 |
| `--process`, `-p` | 要停止的进程名 | com.baidu.naviauto |

## 示例

```bash
# 等待5分钟后停止百度导航
python3 kill_process.py 5

# 等待10分钟后停止百度导航（长格式）
python3 kill_process.py 10 --process com.baidu.naviauto

# 等待1分钟后停止自定义进程
python3 kill_process.py 1 -p com.example.app
```

## 注意事项

1. 时间单位为**分钟**，不是秒
2. 停止进程使用 `am force-stop` 命令，不需要 root 权限
3. 如果需要使用后台运行，可以使用 `nohup`：
   ```bash
   nohup bash -c "source ~/.bash_profile && python3 kill_process.py 35" > /tmp/kill.log 2>&1 &
   ```

## 常见问题

### adb 命令找不到

确保在执行前先运行：
```bash
source ~/.bash_profile
```

### 进程无法停止

如果普通方式无法停止进程，可以尝试使用 root 权限或调试版本的应用。