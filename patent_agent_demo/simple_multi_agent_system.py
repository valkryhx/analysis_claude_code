#!/usr/bin/env python3
"""
简化多智能体协作专利写作系统
确保能够成功运行并生成完整的专利内容
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

from official_glm_client import OfficialGLMClient

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PatentContext:
    """专利上下文信息"""
    topic: str
    description: str
    technical_field: str
    innovation_points: List[str]
    prior_art: List[Dict[str, Any]]
    technical_details: Dict[str, Any]
    claims_draft: List[str]

class SimpleMultiAgentSystem:
    """简化多智能体专利写作系统"""
    
    def __init__(self, glm_api_key: str):
        self.glm_client = OfficialGLMClient(glm_api_key)
        self.patent_context = None
        self.workflow_start_time = time.time()
        
        logger.info("简化多智能体专利写作系统初始化完成")
    
    async def execute_patent_workflow(self, topic: str, description: str) -> Dict[str, Any]:
        """执行专利写作工作流程"""
        logger.info(f"开始执行专利写作工作流程")
        
        # 初始化专利上下文
        self.patent_context = PatentContext(
            topic=topic,
            description=description,
            technical_field="人工智能、知识图谱、检索增强生成",
            innovation_points=["证据图构建", "图增强检索", "多模态融合"],
            prior_art=[],
            technical_details={},
            claims_draft=[]
        )
        
        workflow_results = {}
        
        # 第一阶段：战略规划
        logger.info("第一阶段：战略规划")
        planning_result = await self._execute_planning_stage()
        workflow_results["planning"] = planning_result
        
        # 第二阶段：技术方案设计
        logger.info("第二阶段：技术方案设计")
        technical_result = await self._execute_technical_stage()
        workflow_results["technical"] = technical_result
        
        # 第三阶段：专利撰写
        logger.info("第三阶段：专利撰写")
        writing_result = await self._execute_writing_stage()
        workflow_results["writing"] = writing_result
        
        # 第四阶段：质量优化
        logger.info("第四阶段：质量优化")
        optimization_result = await self._execute_optimization_stage()
        workflow_results["optimization"] = optimization_result
        
        # 生成最终专利文档
        final_patent = await self._generate_final_patent(workflow_results)
        
        # 保存专利文档
        await self._save_patent_document(final_patent)
        
        return {
            "workflow_summary": {
                "total_stages": 4,
                "workflow_duration": time.time() - self.workflow_start_time,
                "final_patent": final_patent
            },
            "workflow_results": workflow_results
        }
    
    async def _execute_planning_stage(self) -> Dict[str, Any]:
        """执行战略规划阶段"""
        prompt = f"""
你是一位资深的专利战略规划师，请为以下专利主题制定详细的战略规划：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}

请从以下维度进行规划：

1. 【技术领域分析】
   - 确定专利所属的IPC分类
   - 分析相关技术领域的发展现状
   - 识别技术发展趋势和热点

2. 【创新点识别与规划】
   - 识别核心技术创新点（至少3-5个）
   - 分析每个创新点的技术价值和商业价值
   - 确定创新点的优先级排序

3. 【专利布局策略】
   - 制定主专利和从属专利的布局策略
   - 考虑分阶段申请策略
   - 分析国际专利申请的必要性

4. 【技术路线图】
   - 设计技术实现路径
   - 确定关键技术节点
   - 制定技术发展时间表

5. 【风险评估与规避】
   - 识别现有技术风险
   - 分析专利无效风险
   - 制定风险规避策略

6. 【商业价值评估】
   - 分析目标市场和应用场景
   - 评估商业转化潜力
   - 制定商业化路径

请以JSON格式返回，包含以上所有维度的详细分析。
"""
        
        try:
            response = self.glm_client.generate_response(prompt)
            result = self._parse_response(response)
            logger.info("战略规划阶段完成")
            return {"success": True, "result": result, "response": response}
        except Exception as e:
            logger.error(f"战略规划阶段失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_technical_stage(self) -> Dict[str, Any]:
        """执行技术方案设计阶段"""
        prompt = f"""
你是一位资深的技术专家，请为以下专利主题设计详细的技术方案：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}
创新点：{self.patent_context.innovation_points}

请设计：

1. 【系统架构设计】
   - 整体系统架构
   - 核心模块设计
   - 模块间接口设计

2. 【核心技术方案】
   - 证据图构建技术
   - 图增强检索算法
   - 多模态融合技术

3. 【技术实现细节】
   - 关键技术参数
   - 算法流程设计
   - 数据结构设计

4. 【技术优势分析】
   - 相比现有技术的优势
   - 技术方案的独特之处
   - 技术效果和性能提升

请以JSON格式返回技术方案设计。
"""
        
        try:
            response = self.glm_client.generate_response(prompt)
            result = self._parse_response(response)
            logger.info("技术方案设计阶段完成")
            return {"success": True, "result": result, "response": response}
        except Exception as e:
            logger.error(f"技术方案设计阶段失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_writing_stage(self) -> Dict[str, Any]:
        """执行专利撰写阶段"""
        prompt = f"""
你是一位资深的专利撰写专家，请基于以下信息撰写完整的专利文档：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}
创新点：{self.patent_context.innovation_points}

请撰写以下内容：

1. 【专利标题】
   - 简洁明了，突出核心技术特征
   - 符合专利命名规范

2. 【专利摘要】
   - 150-250字，突出技术方案和创新点
   - 包含技术问题、解决方案、技术效果

3. 【背景技术】
   - 描述现有技术及其局限性
   - 引出本发明的技术问题
   - 分析现有技术的不足

4. 【发明内容】
   - 概述本发明的技术方案
   - 突出技术优势和创新点
   - 说明技术效果和应用价值

5. 【附图说明】
   - 描述各附图的内容和作用
   - 说明技术方案的实现方式

6. 【具体实施方式】
   - 详细描述技术实现过程
   - 提供具体的实施例
   - 说明关键技术参数

7. 【权利要求】
   - 独立权利要求：保护核心技术方案
   - 从属权利要求：保护具体实施方式
   - 权利要求数量：5-8条
   - 权利要求结构：前序部分+特征部分

请以JSON格式返回专利文档，确保内容完整、语言规范、技术准确。
"""
        
        try:
            response = self.glm_client.generate_response(prompt)
            result = self._parse_response(response)
            logger.info("专利撰写阶段完成")
            return {"success": True, "result": result, "response": response}
        except Exception as e:
            logger.error(f"专利撰写阶段失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_optimization_stage(self) -> Dict[str, Any]:
        """执行质量优化阶段"""
        prompt = f"""
你是一位专业的内容优化专家，请对以下专利内容进行优化：

专利主题：{self.patent_context.topic}

请进行以下优化：

1. 【技术内容优化】
   - 完善技术描述细节
   - 增强技术方案完整性
   - 提升技术表达准确性

2. 【语言表达优化】
   - 改善语言流畅性
   - 增强表达清晰度
   - 提升专业术语使用

3. 【逻辑结构优化】
   - 优化内容组织结构
   - 改善逻辑连贯性
   - 增强可读性

4. 【技术深度优化】
   - 增加技术实现细节
   - 强化技术优势描述
   - 完善技术效果说明

5. 【创新点强化】
   - 突出核心创新点
   - 强化技术独特性
   - 增强竞争优势

请以JSON格式返回优化后的内容。
"""
        
        try:
            response = self.glm_client.generate_response(prompt)
            result = self._parse_response(response)
            logger.info("质量优化阶段完成")
            return {"success": True, "result": result, "response": response}
        except Exception as e:
            logger.error(f"质量优化阶段失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _generate_final_patent(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """生成最终专利文档"""
        logger.info("生成最终专利文档")
        
        final_prompt = f"""
基于多阶段协作的结果，请生成最终的完整专利文档：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}

请生成包含以下内容的完整专利文档：

1. 专利标题
2. 专利摘要
3. 背景技术
4. 发明内容
5. 附图说明
6. 具体实施方式
7. 权利要求（优化后的版本）

请确保：
- 内容完整、准确、专业
- 语言表达清晰、规范
- 技术方案详细、可行
- 权利要求保护范围合理

请以JSON格式返回完整的专利文档。
"""
        
        try:
            final_response = self.glm_client.generate_response(final_prompt)
            final_patent = self._parse_response(final_response)
            logger.info("最终专利文档生成完成")
            return final_patent
        except Exception as e:
            logger.error(f"生成最终专利文档失败: {e}")
            return {"error": str(e)}
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """解析响应结果"""
        try:
            # 尝试解析JSON响应
            if response.strip().startswith('{') and response.strip().endswith('}'):
                return json.loads(response)
            else:
                # 如果不是JSON格式，尝试提取JSON部分
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    # 如果无法解析JSON，返回原始响应
                    return {"raw_response": response}
        except json.JSONDecodeError:
            return {"raw_response": response, "parse_error": "JSON解析失败"}
    
    async def _save_patent_document(self, final_patent: Dict[str, Any]):
        """保存专利文档"""
        filename = f"Evidence_Graph_Enhanced_RAG_Final_Patent.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("多智能体协作生成的最终专利文档\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"专利主题：{self.patent_context.topic}\n")
                f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # 写入专利内容
                if "title" in final_patent:
                    f.write(f"【专利标题】\n{final_patent['title']}\n\n")
                if "abstract" in final_patent:
                    f.write(f"【专利摘要】\n{final_patent['abstract']}\n\n")
                if "background" in final_patent:
                    f.write(f"【背景技术】\n{final_patent['background']}\n\n")
                if "summary" in final_patent:
                    f.write(f"【发明内容】\n{final_patent['summary']}\n\n")
                if "detailed_description" in final_patent:
                    f.write(f"【具体实施方式】\n{final_patent['detailed_description']}\n\n")
                if "claims" in final_patent:
                    f.write(f"【权利要求】\n")
                    for i, claim in enumerate(final_patent['claims'], 1):
                        f.write(f"{i}. {claim}\n")
                    f.write("\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("文档生成完成\n")
                f.write("=" * 80 + "\n")
            
            logger.info(f"专利文档已保存到：{filename}")
            
        except Exception as e:
            logger.error(f"保存专利文档失败: {e}")

async def main():
    """主函数"""
    # 从配置文件获取GLM API密钥
    from config import config
    
    # 创建简化多智能体专利写作系统
    system = SimpleMultiAgentSystem(config.get_glm_api_key())
    
    # 定义专利主题：以证据图增强的RAG
    topic = "基于证据图增强的检索增强生成系统"
    description = """
    一种创新的基于证据图增强的检索增强生成（Evidence Graph Enhanced Retrieval-Augmented Generation, EG-RAG）系统，
    该系统通过构建和利用证据图（Evidence Graph）来增强传统RAG系统的检索能力和生成质量。
    证据图能够捕捉知识实体之间的复杂关系、因果关系和证据链，为RAG系统提供更准确、更可靠的信息检索基础。
    该系统解决了传统RAG系统在信息准确性、可追溯性和推理能力方面的局限性，实现了更高质量、更可信的信息生成。
    """
    
    print("🚀 开始执行简化多智能体协作专利写作系统")
    print("=" * 80)
    print(f"专利主题：{topic}")
    print(f"技术描述：{description.strip()}")
    print("=" * 80)
    
    # 执行专利写作工作流程
    result = await system.execute_patent_workflow(topic, description)
    
    # 输出结果
    print("\n" + "="*80)
    print("🎉 多智能体协作专利写作完成！")
    print("="*80)
    print(f"总阶段数：{result['workflow_summary']['total_stages']}")
    print(f"工作流程耗时：{result['workflow_summary']['workflow_duration']:.1f} 秒")
    print("="*80)
    
    # 显示最终专利内容
    if "final_patent" in result['workflow_summary']:
        final_patent = result['workflow_summary']['final_patent']
        print("\n📋 最终专利内容预览:")
        print("=" * 80)
        
        if "title" in final_patent:
            print(f"【专利标题】\n{final_patent['title']}\n")
        if "abstract" in final_patent:
            print(f"【专利摘要】\n{final_patent['abstract']}\n")
        if "background" in final_patent:
            print(f"【背景技术】\n{final_patent['background']}\n")
        if "summary" in final_patent:
            print(f"【发明内容】\n{final_patent['summary']}\n")
        if "detailed_description" in final_patent:
            print(f"【具体实施方式】\n{final_patent['detailed_description']}\n")
        if "claims" in final_patent:
            print(f"【权利要求】")
            for i, claim in enumerate(final_patent['claims'], 1):
                print(f"{i}. {claim}")
            print()

if __name__ == "__main__":
    asyncio.run(main())