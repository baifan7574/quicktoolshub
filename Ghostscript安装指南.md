# Ghostscript 安装指南

## ✅ 为什么需要 Ghostscript？

Ghostscript 是专业的 PDF 压缩工具，可以：
- ✅ **显著提升压缩效果**（通常可压缩 30-70%）
- ✅ **完全免费**（开源软件）
- ✅ **专业级压缩**（压缩图片、优化结构）

---

## 📦 安装步骤

### Windows 服务器

1. **下载 Ghostscript**
   - 访问：https://www.ghostscript.com/download/gsdnld.html
   - 下载 Windows 版本（.exe 安装程序）

2. **安装**
   - 运行安装程序
   - 安装到默认路径（通常是 `C:\Program Files\gs\`）
   - 确保添加到系统 PATH

3. **验证安装**
   ```bash
   gs --version
   ```
   如果显示版本号，说明安装成功。

---

### Linux 服务器（Ubuntu/Debian）

```bash
sudo apt-get update
sudo apt-get install ghostscript
```

**验证安装**：
```bash
gs --version
```

---

### Linux 服务器（CentOS/RHEL）

```bash
sudo yum install ghostscript
```

或者使用 dnf（较新版本）：
```bash
sudo dnf install ghostscript
```

---

## 🔧 配置 Next.js 项目

### 1. 检查 Ghostscript 是否可用

代码已经自动检测 Ghostscript 是否可用：
- 如果可用，使用 Ghostscript 压缩（效果好）
- 如果不可用，回退到 pdf-lib（效果有限）

### 2. 测试

1. **启动开发服务器**：
   ```bash
   npm run dev
   ```

2. **测试压缩功能**：
   - 访问 `/tools/pdf-compressor`
   - 上传一个 PDF 文件
   - 选择压缩质量
   - 点击 "Compress PDF"

3. **查看压缩结果**：
   - 如果使用 Ghostscript，压缩效果应该明显更好
   - 如果使用 pdf-lib，会显示提示信息

---

## 📊 压缩质量选项

| 选项 | 质量 | 文件大小 | 适用场景 |
|------|------|----------|----------|
| **Screen** | 最低 | 最小 | 屏幕查看，快速分享 |
| **Ebook** | 中等 | 较小 | 电子书、文档分享（推荐） |
| **Printer** | 高 | 较大 | 打印质量 |
| **Prepress** | 最高 | 最大 | 印刷前处理 |

---

## ⚠️ 注意事项

### 1. 服务器资源

- Ghostscript 处理大文件时可能消耗较多 CPU 和内存
- 建议限制文件大小（当前限制：500MB）
- 处理时间可能较长（大文件可能需要 30-60 秒）

### 2. 安全性

- 临时文件会自动清理
- 文件处理在服务器端进行，不会暴露给客户端

### 3. 兼容性

- Ghostscript 支持所有标准 PDF 文件
- 加密的 PDF 可能需要密码

---

## 🚀 部署到生产服务器

### 腾讯云服务器（Linux）

1. **SSH 连接到服务器**

2. **安装 Ghostscript**：
   ```bash
   sudo apt-get update
   sudo apt-get install ghostscript
   ```

3. **验证安装**：
   ```bash
   gs --version
   ```

4. **部署 Next.js 应用**：
   - 代码已经包含自动检测逻辑
   - 如果 Ghostscript 可用，会自动使用
   - 如果不可用，会回退到 pdf-lib

---

## 📝 故障排除

### 问题1：Ghostscript 命令未找到

**错误信息**：`gs: command not found`

**解决方案**：
1. 确认 Ghostscript 已安装
2. 检查 PATH 环境变量
3. 使用完整路径：`/usr/bin/gs --version`

### 问题2：权限错误

**错误信息**：`Permission denied`

**解决方案**：
```bash
sudo chmod +x /usr/bin/gs
```

### 问题3：压缩失败

**可能原因**：
- PDF 文件损坏
- PDF 已加密
- 文件太大

**解决方案**：
- 检查 PDF 文件是否正常
- 尝试其他 PDF 文件
- 检查服务器日志

---

## ✅ 总结

1. **安装 Ghostscript**（免费）
2. **代码已自动支持**（无需修改）
3. **自动检测并使用**（如果可用）
4. **回退机制**（如果不可用，使用 pdf-lib）

**预期效果**：
- 使用 Ghostscript：压缩 30-70%
- 使用 pdf-lib：压缩 1-5%

---

## 🎯 下一步

1. 在服务器上安装 Ghostscript
2. 测试压缩功能
3. 验证压缩效果

如果遇到问题，请查看服务器日志或联系技术支持。

