"""
怀宁县自然人出租不动产智能算税助手
本地预览服务器 + 二维码生成

使用方式：
1. 运行此脚本
2. 确保手机和电脑在同一局域网内
3. 手机扫描终端显示的二维码或输入URL即可访问

如需正式部署到外网：
- 将 index.html 上传到 GitHub Pages、Gitee Pages、Vercel 等免费静态托管平台
- 或上传到单位服务器
"""

import http.server
import socketserver
import socket
import qrcode
import os
import sys

PORT = 8765
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def generate_qr_codes(local_ip):
    """生成访问二维码"""
    url = f"http://{local_ip}:{PORT}"
    
    # 生成二维码图片
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 保存二维码
    qr_path = os.path.join(OUTPUT_DIR, "access_qrcode.png")
    img.save(qr_path)
    
    # 打印到终端（ASCII形式）
    print("\n" + "=" * 50)
    print("  手机扫码访问地址：")
    print(f"  {url}")
    print("=" * 50)
    print(f"\n二维码图片已保存到：{qr_path}")
    print("（可打印出来放在前台供纳税人扫码）")
    print("\n提示：确保手机和电脑连接同一WiFi网络\n")
    
    return url

def main():
    os.chdir(OUTPUT_DIR)
    
    # 检查 index.html 是否存在
    if not os.path.exists("index.html"):
        print("错误：未找到 index.html 文件！")
        sys.exit(1)
    
    local_ip = get_local_ip()
    url = generate_qr_codes(local_ip)
    
    # 启动HTTP服务器
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"服务器已启动：{url}")
        print("按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    main()
