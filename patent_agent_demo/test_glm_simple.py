#!/usr/bin/env python3
"""
简单测试 GLM 客户端
"""

import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from glm_client import GLMClient

async def test_glm_client():
    """测试 GLM 客户端"""
    print("🚀 开始测试 GLM 客户端...")
    
    try:
        # 验证配置
        if not config.validate_config():
            print("❌ 配置验证失败")
            return
        
        # 创建 GLM 客户端
        print(f"🔑 使用 API key: {config.get_glm_api_key()[:20]}...")
        client = GLMClient(config.get_glm_api_key())
        
        # 测试简单对话
        print("\n💬 测试简单对话...")
        prompt = "你好，请简单介绍一下你自己"
        response = await client.generate_response(prompt)
        print(f"🤖 GLM 回复: {response}")
        
        # 测试专利分析
        print("\n📋 测试专利分析...")
        topic = "智能家居控制系统"
        description = "一种基于物联网技术的智能家居控制系统，能够自动调节室内温度、照明和安防设备"
        
        analysis = await client.analyze_patent_topic(topic, description)
        print(f"📊 专利分析结果:")
        print(f"   新颖性评分: {analysis.novelty_score}")
        print(f"   创造性评分: {analysis.inventive_step_score}")
        print(f"   工业实用性: {analysis.industrial_applicability}")
        print(f"   专利性评估: {analysis.patentability_assessment}")
        
        print("\n✅ GLM 客户端测试成功!")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

async def test_patent_draft():
    """测试专利撰写功能"""
    print("\n📝 测试专利撰写功能...")
    
    try:
        client = GLMClient(config.get_glm_api_key())
        
        topic = "电动汽车无线充电系统"
        description = "一种高效、安全的电动汽车无线充电系统，采用磁共振技术实现远距离充电"
        
        draft = await client.draft_patent(topic, description)
        
        print(f"📄 专利草稿:")
        print(f"   标题: {draft.title}")
        print(f"   摘要: {draft.abstract[:100]}...")
        print(f"   权利要求数量: {len(draft.claims)}")
        
        print("\n✅ 专利撰写测试成功!")
        
    except Exception as e:
        print(f"\n❌ 专利撰写测试失败: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""
    print("🔬 GLM 客户端功能测试")
    print("=" * 50)
    
    # 测试基本功能
    await test_glm_client()
    
    # 测试专利撰写
    await test_patent_draft()
    
    print("\n🎉 所有测试完成!")

if __name__ == "__main__":
    asyncio.run(main())