import { NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy'
  timestamp: string
  services: {
    database: {
      status: 'up' | 'down'
      responseTime?: number
    }
    pm2: {
      status: 'up' | 'down'
      processes?: any[]
    }
    nginx: {
      status: 'up' | 'down'
    }
  }
  system?: {
    cpu?: number
    memory?: number
    disk?: number
  }
}

/**
 * 健康检查端点
 * GET /api/health
 */
export async function GET() {
  const startTime = Date.now()
  const health: HealthStatus = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    services: {
      database: { status: 'down' },
      pm2: { status: 'down' },
      nginx: { status: 'down' },
    },
  }

  try {
    // 1. 检查数据库连接
    const dbStartTime = Date.now()
    try {
      const { error } = await supabase.from('tools').select('id').limit(1)
      if (error) throw error
      health.services.database = {
        status: 'up',
        responseTime: Date.now() - dbStartTime,
      }
    } catch (error) {
      health.services.database.status = 'down'
      health.status = 'unhealthy'
    }

    // 2. 检查 PM2 进程
    try {
      const { stdout } = await execAsync('pm2 jlist')
      const processes = JSON.parse(stdout)
      const quicktoolshub = processes.find((p: any) => p.name === 'quicktoolshub')
      
      if (quicktoolshub && quicktoolshub.pm2_env.status === 'online') {
        health.services.pm2 = {
          status: 'up',
          processes: processes.map((p: any) => ({
            name: p.name,
            status: p.pm2_env.status,
            uptime: p.pm2_env.pm_uptime,
            memory: p.monit.memory,
            cpu: p.monit.cpu,
          })),
        }
      } else {
        health.services.pm2.status = 'down'
        health.status = health.status === 'healthy' ? 'degraded' : 'unhealthy'
      }
    } catch (error) {
      health.services.pm2.status = 'down'
      health.status = health.status === 'healthy' ? 'degraded' : 'unhealthy'
    }

    // 3. 检查 Nginx
    try {
      await execAsync('systemctl is-active --quiet nginx')
      health.services.nginx.status = 'up'
    } catch (error) {
      health.services.nginx.status = 'down'
      health.status = health.status === 'healthy' ? 'degraded' : 'unhealthy'
    }

    // 4. 获取系统资源（可选，需要权限）
    try {
      const [cpuResult, memoryResult, diskResult] = await Promise.allSettled([
        execAsync("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'"),
        execAsync("free | grep Mem | awk '{printf \"%.2f\", $3/$2 * 100.0}'"),
        execAsync("df -h / | awk 'NR==2 {print $5}' | sed 's/%//'"),
      ])

      health.system = {}
      if (cpuResult.status === 'fulfilled') {
        health.system.cpu = parseFloat(cpuResult.value.stdout.trim())
      }
      if (memoryResult.status === 'fulfilled') {
        health.system.memory = parseFloat(memoryResult.value.stdout.trim())
      }
      if (diskResult.status === 'fulfilled') {
        health.system.disk = parseFloat(diskResult.value.stdout.trim())
      }
    } catch (error) {
      // 系统信息获取失败不影响健康检查
    }

    const statusCode = health.status === 'healthy' ? 200 : health.status === 'degraded' ? 200 : 503

    return NextResponse.json(health, { status: statusCode })
  } catch (error: any) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error.message,
      },
      { status: 503 }
    )
  }
}

