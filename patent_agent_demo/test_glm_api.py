#!/usr/bin/env python3
"""
测试 GLM API 连接
"""

import asyncio
import aiohttp
import json
from config import config

async def test_glm_api():
    """测试 GLM API 连接"""
    print("🧪 测试 GLM API 连接...")
    
    api_key = config.get_glm_api_key()
    base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    print(f"🔑 API Key: {api_key[:20]}...")
    print(f"🌐 API 端点: {base_url}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4.5-flash",
        "messages": [
            {
                "role": "user",
                "content": "你好，请简单介绍一下你自己"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7,
        "stream": False
    }
    
    try:
        print("\n📡 发送测试请求...")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                base_url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                print(f"📊 响应状态: {response.status}")
                print(f"📋 响应头: {dict(response.headers)}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ API 调用成功!")
                    print(f"📄 响应内容: {result}")
                else:
                    error_text = await response.text()
                    print(f"❌ API 调用失败: {response.status}")
                    print(f"🔍 错误详情: {error_text}")
                    
    except asyncio.TimeoutError:
        print("⏰ 请求超时")
    except aiohttp.ClientError as e:
        print(f"🌐 网络错误: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        import traceback
        traceback.print_exc()

async def test_simple_request():
    """测试简单请求"""
    print("\n🧪 测试简单请求...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # 测试基本连接
            async with session.get("https://httpbin.org/get", timeout=10) as response:
                print(f"✅ 基本网络连接正常: {response.status}")
                
    except Exception as e:
        print(f"❌ 基本网络连接失败: {e}")

async def main():
    """主函数"""
    print("🚀 GLM API 连接测试")
    print("=" * 50)
    
    # 测试基本网络连接
    await test_simple_request()
    
    # 测试 GLM API
    await test_glm_api()
    
    print("\n🎉 测试完成!")

if __name__ == "__main__":
    asyncio.run(main())