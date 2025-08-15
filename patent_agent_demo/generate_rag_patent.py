#!/usr/bin/env python3
"""
生成 RAG (Retrieval-Augmented Generation) 相关专利的脚本
"""

import asyncio
import sys
import os
from typing import Dict, Any

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from official_glm_client import OfficialGLMClient

async def generate_rag_patent():
    """生成 RAG 相关专利"""
    print("🚀 开始生成 RAG 相关专利...")
    print("=" * 80)
    
    try:
        # 验证配置
        if not config.validate_config():
            print("❌ 配置验证失败")
            return
        
        # 创建 GLM 客户端
        print(f"🔑 使用 GLM API key: {config.get_glm_api_key()[:20]}...")
        client = OfficialGLMClient(config.get_glm_api_key())
        
        # RAG 专利主题和描述
        topic = "基于多模态检索增强的生成式人工智能系统"
        description = """
        一种创新的多模态检索增强生成（Multi-Modal Retrieval-Augmented Generation, MM-RAG）系统，
        该系统能够智能地从多种数据源（文本、图像、音频、视频）中检索相关信息，
        并将检索到的信息与生成式AI模型相结合，生成高质量、准确且可追溯的响应。
        该系统解决了传统生成式AI模型存在的幻觉问题、信息时效性不足以及缺乏可追溯性等问题。
        """
        
        print(f"📋 专利主题: {topic}")
        print(f"📝 专利描述: {description.strip()}")
        print("\n" + "="*80)
        
        # 第一步：专利主题分析
        print("\n🔍 第一步：专利主题分析")
        print("-" * 40)
        
        analysis = client.analyze_patent_topic(topic, description)
        
        print(f"📊 专利分析结果:")
        print(f"   新颖性评分: {analysis.novelty_score}/10")
        print(f"   创造性评分: {analysis.inventive_step_score}/10")
        print(f"   工业实用性: {'✅' if analysis.industrial_applicability else '❌'}")
        print(f"   专利性评估: {analysis.patentability_assessment}")
        print(f"   商业潜力: {analysis.commercial_potential}")
        
        print(f"\n💡 改进建议:")
        for i, rec in enumerate(analysis.recommendations, 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "="*80)
        
        # 第二步：撰写专利文档
        print("\n✍️  第二步：撰写专利文档")
        print("-" * 40)
        
        draft = client.draft_patent(topic, description)
        
        print(f"📄 专利草稿生成完成!")
        print(f"   标题: {draft.title}")
        print(f"   摘要: {draft.abstract}")
        print(f"   权利要求数量: {len(draft.claims)}")
        
        print("\n" + "="*80)
        
        # 第三步：专利性评估
        print("\n📊 第三步：专利性评估")
        print("-" * 40)
        
        assessment_prompt = f"""
        请对以下专利进行全面的专利性评估:
        
        标题: {draft.title}
        摘要: {draft.abstract}
        权利要求: {chr(10).join(draft.claims)}
        
        请从以下方面进行评估:
        1. 新颖性 (0-10分) - 与现有技术的区别
        2. 创造性 (0-10分) - 技术方案的创新程度
        3. 工业实用性 - 是否能够实际应用
        4. 技术先进性 - 技术方案的先进程度
        5. 市场前景 - 商业应用潜力
        6. 整体专利性评估 - 综合评分和建议
        7. 改进建议 - 如何增强专利性
        """
        
        assessment = client.generate_response(assessment_prompt)
        
        print("📊 专利性评估结果:")
        print(assessment)
        
        print("\n" + "="*80)
        
        # 第四步：保存专利文档
        print("\n💾 第四步：保存专利文档")
        print("-" * 40)
        
        filename = "RAG_Patent_Draft.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("基于多模态检索增强的生成式人工智能系统\n")
            f.write("专利文档草稿\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("【专利标题】\n")
            f.write(f"{draft.title}\n\n")
            
            f.write("【专利摘要】\n")
            f.write(f"{draft.abstract}\n\n")
            
            f.write("【背景技术】\n")
            f.write(f"{draft.background}\n\n")
            
            f.write("【发明内容】\n")
            f.write(f"{draft.summary}\n\n")
            
            f.write("【详细描述】\n")
            f.write(f"{draft.detailed_description}\n\n")
            
            f.write("【权利要求】\n")
            for i, claim in enumerate(draft.claims, 1):
                f.write(f"{i}. {claim}\n")
            f.write("\n")
            
            f.write("【附图说明】\n")
            f.write(f"{draft.drawings_description}\n\n")
            
            f.write("【技术图表】\n")
            for i, diagram in enumerate(draft.technical_diagrams, 1):
                f.write(f"图{i}: {diagram}\n")
            f.write("\n")
            
            f.write("【专利分析】\n")
            f.write(f"新颖性评分: {analysis.novelty_score}/10\n")
            f.write(f"创造性评分: {analysis.inventive_step_score}/10\n")
            f.write(f"工业实用性: {'是' if analysis.industrial_applicability else '否'}\n")
            f.write(f"专利性评估: {analysis.patentability_assessment}\n")
            f.write(f"商业潜力: {analysis.commercial_potential}\n\n")
            
            f.write("【改进建议】\n")
            for i, rec in enumerate(analysis.recommendations, 1):
                f.write(f"{i}. {rec}\n")
            f.write("\n")
            
            f.write("【专利性评估】\n")
            f.write(assessment + "\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("文档生成完成\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ 专利文档已保存到: {filename}")
        
        print("\n" + "="*80)
        print("🎉 RAG 专利生成完成!")
        print("=" * 80)
        
        # 显示完整的专利内容
        print("\n📋 完整专利内容预览:")
        print("=" * 80)
        print(f"【专利标题】\n{draft.title}\n")
        print(f"【专利摘要】\n{draft.abstract}\n")
        print(f"【背景技术】\n{draft.background}\n")
        print(f"【发明内容】\n{draft.summary}\n")
        print(f"【详细描述】\n{draft.detailed_description}\n")
        print(f"【权利要求】")
        for i, claim in enumerate(draft.claims, 1):
            print(f"{i}. {claim}")
        print(f"\n【附图说明】\n{draft.drawings_description}\n")
        print(f"【技术图表】")
        for i, diagram in enumerate(draft.technical_diagrams, 1):
            print(f"图{i}: {diagram}")
        
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""
    await generate_rag_patent()

if __name__ == "__main__":
    asyncio.run(main())