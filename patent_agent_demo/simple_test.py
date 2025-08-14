#!/usr/bin/env python3
"""
简化的 GLM API 专利生成测试
"""

import asyncio
import aiohttp
import json
from config import config

async def test_patent_generation():
    """测试专利生成"""
    print("🧪 测试专利生成功能...")
    
    api_key = config.get_glm_api_key()
    base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    print(f"🔑 API Key: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 简化的提示词
    data = {
        "model": "glm-4.5-flash",
        "messages": [
            {
                "role": "user",
                "content": "请为'基于多模态检索增强的生成式人工智能系统'这个发明写一个简短的专利摘要，不超过100字。"
            }
        ],
        "max_tokens": 200,
        "temperature": 0.7,
        "stream": False
    }
    
    try:
        print("\n📡 发送专利生成请求...")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                base_url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                print(f"📊 响应状态: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ 专利生成成功!")
                    
                    # 解析响应
                    if "choices" in result and len(result["choices"]) > 0:
                        message = result["choices"][0]["message"]
                        content = message.get("content", "")
                        reasoning_content = message.get("reasoning_content", "")
                        
                        if content:
                            print(f"📄 专利摘要: {content}")
                        elif reasoning_content:
                            print(f"📄 专利摘要: {reasoning_content}")
                        else:
                            print(f"📄 完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    else:
                        print(f"❌ 响应格式不正确: {result}")
                        
                else:
                    error_text = await response.text()
                    print(f"❌ 专利生成失败: {response.status}")
                    print(f"🔍 错误详情: {error_text}")
                    
    except asyncio.TimeoutError:
        print("⏰ 请求超时")
    except aiohttp.ClientError as e:
        print(f"🌐 网络错误: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""
    print("🚀 简化版专利生成测试")
    print("=" * 50)
    
    await test_patent_generation()
    
    print("\n🎉 测试完成!")

if __name__ == "__main__":
    asyncio.run(main())