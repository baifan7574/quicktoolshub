#!/usr/bin/env node

/**
 * 服务器监控脚本
 * 监控 CPU、内存、磁盘、PM2 进程、Nginx 状态
 * 
 * 使用方法：
 * node scripts/monitor-server.js
 * 
 * 或添加到 cron：
 * */5 * * * * cd /var/www/quicktoolshub && node scripts/monitor-server.js >> logs/monitor.log 2>&1
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');

const execAsync = promisify(exec);

// 告警阈值
const THRESHOLDS = {
  cpu: 80,        // CPU 使用率超过 80% 告警
  memory: 85,     // 内存使用率超过 85% 告警
  disk: 80,       // 磁盘使用率超过 80% 告警
};

// 日志文件路径
const LOG_DIR = path.join(__dirname, '../logs');
const LOG_FILE = path.join(LOG_DIR, 'monitor.log');

/**
 * 获取 CPU 使用率
 */
async function getCpuUsage() {
  try {
    const { stdout } = await execAsync("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'");
    return parseFloat(stdout.trim());
  } catch (error) {
    console.error('获取 CPU 使用率失败:', error.message);
    return null;
  }
}

/**
 * 获取内存使用率
 */
async function getMemoryUsage() {
  try {
    const { stdout } = await execAsync("free | grep Mem | awk '{printf \"%.2f\", $3/$2 * 100.0}'");
    return parseFloat(stdout.trim());
  } catch (error) {
    console.error('获取内存使用率失败:', error.message);
    return null;
  }
}

/**
 * 获取磁盘使用率
 */
async function getDiskUsage() {
  try {
    const { stdout } = await execAsync("df -h / | awk 'NR==2 {print $5}' | sed 's/%//'");
    return parseFloat(stdout.trim());
  } catch (error) {
    console.error('获取磁盘使用率失败:', error.message);
    return null;
  }
}

/**
 * 检查 PM2 进程状态
 */
async function checkPM2Status() {
  try {
    const { stdout } = await execAsync('pm2 jlist');
    const processes = JSON.parse(stdout);
    
    const status = {
      total: processes.length,
      online: 0,
      stopped: 0,
      errored: 0,
      restarting: 0,
    };
    
    processes.forEach(proc => {
      switch (proc.pm2_env.status) {
        case 'online':
          status.online++;
          break;
        case 'stopped':
          status.stopped++;
          break;
        case 'errored':
          status.errored++;
          break;
        case 'restarting':
          status.restarting++;
          break;
      }
    });
    
    return status;
  } catch (error) {
    console.error('检查 PM2 状态失败:', error.message);
    return null;
  }
}

/**
 * 检查 Nginx 状态
 */
async function checkNginxStatus() {
  try {
    await execAsync('systemctl is-active --quiet nginx');
    return { status: 'running' };
  } catch (error) {
    return { status: 'stopped' };
  }
}

/**
 * 写入日志
 */
async function writeLog(message) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}\n`;
  
  try {
    // 确保日志目录存在
    await fs.mkdir(LOG_DIR, { recursive: true });
    await fs.appendFile(LOG_FILE, logMessage);
  } catch (error) {
    console.error('写入日志失败:', error.message);
  }
  
  console.log(logMessage.trim());
}

/**
 * 发送告警（可以扩展为邮件、微信等）
 */
async function sendAlert(alert) {
  const message = `⚠️ 告警: ${alert}`;
  await writeLog(message);
  // TODO: 可以添加邮件、微信、钉钉等通知方式
}

/**
 * 主监控函数
 */
async function monitor() {
  await writeLog('=== 开始服务器监控 ===');
  
  // 1. 检查 CPU
  const cpuUsage = await getCpuUsage();
  if (cpuUsage !== null) {
    await writeLog(`CPU 使用率: ${cpuUsage.toFixed(2)}%`);
    if (cpuUsage > THRESHOLDS.cpu) {
      await sendAlert(`CPU 使用率过高: ${cpuUsage.toFixed(2)}% (阈值: ${THRESHOLDS.cpu}%)`);
    }
  }
  
  // 2. 检查内存
  const memoryUsage = await getMemoryUsage();
  if (memoryUsage !== null) {
    await writeLog(`内存使用率: ${memoryUsage.toFixed(2)}%`);
    if (memoryUsage > THRESHOLDS.memory) {
      await sendAlert(`内存使用率过高: ${memoryUsage.toFixed(2)}% (阈值: ${THRESHOLDS.memory}%)`);
    }
  }
  
  // 3. 检查磁盘
  const diskUsage = await getDiskUsage();
  if (diskUsage !== null) {
    await writeLog(`磁盘使用率: ${diskUsage.toFixed(2)}%`);
    if (diskUsage > THRESHOLDS.disk) {
      await sendAlert(`磁盘使用率过高: ${diskUsage.toFixed(2)}% (阈值: ${THRESHOLDS.disk}%)`);
    }
  }
  
  // 4. 检查 PM2
  const pm2Status = await checkPM2Status();
  if (pm2Status) {
    await writeLog(`PM2 进程: 总计 ${pm2Status.total}, 运行中 ${pm2Status.online}, 停止 ${pm2Status.stopped}, 错误 ${pm2Status.errored}, 重启中 ${pm2Status.restarting}`);
    if (pm2Status.errored > 0) {
      await sendAlert(`PM2 有进程处于错误状态: ${pm2Status.errored} 个`);
    }
    if (pm2Status.online === 0 && pm2Status.total > 0) {
      await sendAlert('PM2 所有进程都已停止！');
    }
  }
  
  // 5. 检查 Nginx
  const nginxStatus = await checkNginxStatus();
  await writeLog(`Nginx 状态: ${nginxStatus.status}`);
  if (nginxStatus.status === 'stopped') {
    await sendAlert('Nginx 服务已停止！');
  }
  
  await writeLog('=== 监控完成 ===\n');
}

// 运行监控
if (require.main === module) {
  monitor().catch(error => {
    console.error('监控脚本执行失败:', error);
    process.exit(1);
  });
}

module.exports = { monitor };

