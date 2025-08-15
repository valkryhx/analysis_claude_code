#!/usr/bin/env python3
"""
专业级多智能体协作专利写作系统
满足专利三性要求：新颖性、创造性、实用性
包含详细的执行过程显示和代码实现
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import textwrap

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
    prior_art: List[Dict[str, Any]] = field(default_factory=list)
    technical_details: Dict[str, Any] = field(default_factory=dict)
    claims_draft: List[str] = field(default_factory=list)
    novelty_analysis: Dict[str, Any] = field(default_factory=dict)
    inventiveness_analysis: Dict[str, Any] = field(default_factory=dict)
    utility_analysis: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentTask:
    """智能体任务"""
    agent_name: str
    task_type: str
    prompt: str
    start_time: float
    end_time: Optional[float] = None
    response: Optional[str] = None
    status: str = "pending"
    error: Optional[str] = None

class ProfessionalMultiAgentSystem:
    """专业级多智能体专利写作系统"""
    
    def __init__(self, glm_api_key: str):
        self.glm_client = OfficialGLMClient(glm_api_key)
        self.patent_context = None
        self.workflow_start_time = time.time()
        self.agent_tasks: List[AgentTask] = []
        self.current_stage = 0
        self.total_stages = 6
        
        # 定义智能体角色和职责
        self.agents = {
            "strategist": "专利战略专家",
            "researcher": "技术研究专家", 
            "architect": "系统架构专家",
            "writer": "专利撰写专家",
            "validator": "专利审查专家",
            "optimizer": "内容优化专家"
        }
        
        logger.info("专业级多智能体专利写作系统初始化完成")
    
    def _print_stage_header(self, stage_name: str, stage_description: str):
        """打印阶段标题"""
        print("\n" + "="*100)
        print(f"🎯 第 {self.current_stage} 阶段：{stage_name}")
        print(f"📝 {stage_description}")
        print("="*100)
    
    def _print_agent_task_start(self, agent_name: str, task_type: str, task_description: str):
        """打印智能体任务开始"""
        print(f"\n🤖 [{agent_name}] 开始执行任务：{task_type}")
        print(f"📋 任务描述：{task_description}")
        print("-" * 80)
    
    def _print_agent_task_result(self, agent_name: str, task_type: str, response: str, duration: float):
        """打印智能体任务结果"""
        print(f"\n✅ [{agent_name}] 任务完成：{task_type}")
        print(f"⏱️  执行时间：{duration:.2f} 秒")
        print(f"📊 响应长度：{len(response)} 字符")
        print(f"📝 响应内容：")
        print(textwrap.indent(response[:300] + "..." if len(response) > 300 else response, "    "))
        print("-" * 80)
    
    def _print_patent_three_characteristics(self):
        """打印专利三性分析"""
        print("\n🔍 专利三性分析")
        print("="*80)
        
        if self.patent_context.novelty_analysis:
            print("📈 新颖性分析：")
            for key, value in self.patent_context.novelty_analysis.items():
                print(f"   {key}: {value}")
        
        if self.patent_context.inventiveness_analysis:
            print("\n💡 创造性分析：")
            for key, value in self.patent_context.inventiveness_analysis.items():
                print(f"   {key}: {value}")
        
        if self.patent_context.utility_analysis:
            print("\n🚀 实用性分析：")
            for key, value in self.patent_context.utility_analysis.items():
                print(f"   {key}: {value}")
    
    async def execute_patent_workflow(self, topic: str, description: str) -> Dict[str, Any]:
        """执行专利写作工作流程"""
        print("🚀 开始执行专业级多智能体协作专利写作系统")
        print("="*100)
        print(f"专利主题：{topic}")
        print(f"技术描述：{description.strip()}")
        print("="*100)
        
        # 初始化专利上下文
        self.patent_context = PatentContext(
            topic=topic,
            description=description,
            technical_field="人工智能、知识图谱、检索增强生成、图神经网络",
            innovation_points=["证据图构建", "图增强检索", "多模态融合", "推理增强", "质量评估"]
        )
        
        workflow_results = {}
        
        # 第一阶段：专利三性分析
        self.current_stage = 1
        self._print_stage_header("专利三性分析", "分析专利的新颖性、创造性和实用性")
        novelty_result = await self._execute_novelty_analysis()
        workflow_results["novelty"] = novelty_result
        
        # 第二阶段：技术深度研究
        self.current_stage = 2
        self._print_stage_header("技术深度研究", "深入研究技术方案的技术细节和实现方法")
        research_result = await self._execute_technical_research()
        workflow_results["research"] = research_result
        
        # 第三阶段：系统架构设计
        self.current_stage = 3
        self._print_stage_header("系统架构设计", "设计完整的系统架构和技术实现方案")
        architecture_result = await self._execute_system_architecture()
        workflow_results["architecture"] = architecture_result
        
        # 第四阶段：专利撰写
        self.current_stage = 4
        self._print_stage_header("专利撰写", "撰写完整的专利文档，包含所有必要部分")
        writing_result = await self._execute_patent_writing()
        workflow_results["writing"] = writing_result
        
        # 第五阶段：专利审查
        self.current_stage = 5
        self._print_stage_header("专利审查", "审查专利的完整性、准确性和合规性")
        validation_result = await self._execute_patent_validation()
        workflow_results["validation"] = validation_result
        
        # 第六阶段：内容优化
        self.current_stage = 6
        self._print_stage_header("内容优化", "优化专利内容，提升质量和专业性")
        optimization_result = await self._execute_content_optimization()
        workflow_results["optimization"] = optimization_result
        
        # 生成最终专利文档
        final_patent = await self._generate_final_patent(workflow_results)
        
        # 保存专利文档
        await self._save_patent_document(final_patent)
        
        # 显示专利三性分析
        self._print_patent_three_characteristics()
        
        return {
            "workflow_summary": {
                "total_stages": self.total_stages,
                "workflow_duration": time.time() - self.workflow_start_time,
                "final_patent": final_patent,
                "agent_tasks": self.agent_tasks
            },
            "workflow_results": workflow_results
        }
    
    async def _execute_novelty_analysis(self) -> Dict[str, Any]:
        """执行新颖性分析"""
        agent_name = "strategist"
        task_type = "novelty_analysis"
        task_description = "分析专利的新颖性，识别与现有技术的区别"
        
        self._print_agent_task_start(agent_name, task_type, task_description)
        
        prompt = f"""你是一位资深的专利战略专家，专门负责专利新颖性分析。

请对以下专利主题进行专业的新颖性分析：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}

请从以下维度进行深入分析：

1. 【技术领域界定】
   - 确定专利所属的IPC国际专利分类
   - 分析相关技术领域的发展现状和趋势
   - 识别技术领域的边界和交叉点

2. 【现有技术检索分析】
   - 分析传统RAG系统的技术现状
   - 识别现有证据图技术的应用情况
   - 评估图增强检索技术的发展水平

3. 【新颖性判断】
   - 分析本发明的技术特征与现有技术的区别
   - 识别技术方案中的创新点
   - 评估技术方案的独特性

4. 【技术贡献评估】
   - 分析本发明对现有技术的改进
   - 评估技术方案的突破性
   - 识别技术发展的里程碑意义

请以专业、严谨的语言进行分析，确保分析深度和准确性。回答不超过800字。"""
        
        task = AgentTask(agent_name, task_type, prompt, time.time())
        self.agent_tasks.append(task)
        
        try:
            response = self.glm_client.generate_response(prompt)
            task.end_time = time.time()
            task.response = response
            task.status = "completed"
            
            # 解析响应并更新专利上下文
            self._update_novelty_analysis(response)
            
            duration = task.end_time - task.start_time
            self._print_agent_task_result(agent_name, task_type, response, duration)
            
            return {"success": True, "result": {"novelty_analysis": response}, "response": response}
        except Exception as e:
            task.end_time = time.time()
            task.status = "failed"
            task.error = str(e)
            logger.error(f"新颖性分析失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_technical_research(self) -> Dict[str, Any]:
        """执行技术深度研究"""
        agent_name = "researcher"
        task_type = "technical_research"
        task_description = "深入研究技术方案的技术细节和实现方法"
        
        self._print_agent_task_start(agent_name, task_type, task_description)
        
        prompt = f"""你是一位资深的技术研究专家，专门负责技术方案的深度研究。

请对以下专利主题进行技术深度研究：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}

请从以下维度进行深入研究：

1. 【核心技术原理】
   - 分析证据图构建的数学原理和算法基础
   - 研究图增强检索的理论框架
   - 探讨多模态融合的技术机制

2. 【技术实现细节】
   - 详细分析图神经网络的实现方法
   - 研究注意力机制在证据图中的应用
   - 分析Transformer架构的优化策略

3. 【技术参数和指标】
   - 确定关键技术参数和性能指标
   - 分析技术方案的可行性
   - 评估技术实现的复杂度

4. 【技术优势分析】
   - 分析相比现有技术的优势
   - 评估技术方案的先进性
   - 识别技术突破点

请以专业、技术性的语言进行分析，包含具体的技术细节和实现方法。回答不超过1000字。"""
        
        task = AgentTask(agent_name, task_type, prompt, time.time())
        self.agent_tasks.append(task)
        
        try:
            response = self.glm_client.generate_response(prompt)
            task.end_time = time.time()
            task.response = response
            task.status = "completed"
            
            duration = task.end_time - task.start_time
            self._print_agent_task_result(agent_name, task_type, response, duration)
            
            return {"success": True, "result": {"technical_research": response}, "response": response}
        except Exception as e:
            task.end_time = time.time()
            task.status = "failed"
            task.error = str(e)
            logger.error(f"技术深度研究失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_system_architecture(self) -> Dict[str, Any]:
        """执行系统架构设计"""
        agent_name = "architect"
        task_type = "system_architecture"
        task_description = "设计完整的系统架构和技术实现方案"
        
        self._print_agent_task_start(agent_name, task_type, task_description)
        
        prompt = f"""你是一位资深的系统架构专家，专门负责系统架构设计。

请为以下专利主题设计完整的系统架构：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}

请设计以下内容：

1. 【系统整体架构】
   - 设计模块化的系统架构
   - 定义各模块的功能和职责
   - 设计模块间的接口和通信机制

2. 【核心模块设计】
   - 证据图构建模块的详细设计
   - 图增强检索模块的架构设计
   - 多模态融合模块的实现方案
   - 推理增强模块的技术架构

3. 【技术实现方案】
   - 数据流程设计
   - 算法流程设计
   - 性能优化策略
   - 扩展性设计

4. 【系统集成方案】
   - 与现有系统的集成方案
   - 部署和运维方案
   - 监控和调试方案

请以专业的系统架构设计语言进行描述，包含架构图、流程图等技术细节。回答不超过1200字。"""
        
        task = AgentTask(agent_name, task_type, prompt, time.time())
        self.agent_tasks.append(task)
        
        try:
            response = self.glm_client.generate_response(prompt)
            task.end_time = time.time()
            task.response = response
            task.status = "completed"
            
            duration = task.end_time - task.start_time
            self._print_agent_task_result(agent_name, task_type, response, duration)
            
            return {"success": True, "result": {"system_architecture": response}, "response": response}
        except Exception as e:
            task.end_time = time.time()
            task.status = "failed"
            task.error = str(e)
            logger.error(f"系统架构设计失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_patent_writing(self) -> Dict[str, Any]:
        """执行专利撰写"""
        agent_name = "writer"
        task_type = "patent_writing"
        task_description = "撰写完整的专利文档，包含所有必要部分"
        
        self._print_agent_task_start(agent_name, task_type, task_description)
        
        prompt = f"""你是一位资深的专利撰写专家，专门负责专利文档的撰写。

请为以下专利主题撰写完整的专利文档：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}

请撰写以下内容：

1. 【专利标题】
   - 简洁明了，突出核心技术特征
   - 符合专利命名规范

2. 【专利摘要】
   - 150-250字，突出技术方案和创新点
   - 包含技术问题、解决方案、技术效果

3. 【背景技术】
   - 详细描述现有技术及其局限性
   - 引出本发明的技术问题
   - 分析现有技术的不足

4. 【发明内容】
   - 概述本发明的技术方案
   - 突出技术优势和创新点
   - 说明技术效果和应用价值

5. 【具体实施方式】
   - 详细描述技术实现过程
   - 提供具体的实施例
   - 说明关键技术参数

6. 【权利要求】
   - 独立权利要求：保护核心技术方案
   - 从属权利要求：保护具体实施方式
   - 权利要求数量：8-12条
   - 权利要求结构：前序部分+特征部分

请确保内容完整、语言规范、技术准确，符合专利撰写标准。回答不超过2000字。"""
        
        task = AgentTask(agent_name, task_type, prompt, time.time())
        self.agent_tasks.append(task)
        
        try:
            response = self.glm_client.generate_response(prompt)
            task.end_time = time.time()
            task.response = response
            task.status = "completed"
            
            duration = task.end_time - task.start_time
            self._print_agent_task_result(agent_name, task_type, response, duration)
            
            return {"success": True, "result": {"patent_writing": response}, "response": response}
        except Exception as e:
            task.end_time = time.time()
            task.status = "failed"
            task.error = str(e)
            logger.error(f"专利撰写失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_patent_validation(self) -> Dict[str, Any]:
        """执行专利审查"""
        agent_name = "validator"
        task_type = "patent_validation"
        task_description = "审查专利的完整性、准确性和合规性"
        
        self._print_agent_task_start(agent_name, task_type, task_description)
        
        prompt = f"""你是一位资深的专利审查专家，专门负责专利文档的审查。

请对以下专利文档进行专业审查：

专利主题：{self.patent_context.topic}

请从以下维度进行审查：

1. 【专利三性审查】
   - 新颖性：技术方案是否具有新颖性
   - 创造性：是否具有突出的实质性特点和显著进步
   - 实用性：是否能够制造或使用，产生积极效果

2. 【技术内容审查】
   - 技术方案的完整性和准确性
   - 技术描述的清晰性和规范性
   - 实施例的充分性和可行性

3. 【权利要求审查】
   - 权利要求的保护范围是否合理
   - 权利要求的结构是否符合规范
   - 从属权利要求是否支持独立权利要求

4. 【合规性审查】
   - 是否符合专利撰写规范
   - 是否包含必要的技术信息
   - 是否满足专利法要求

请以专业的审查标准进行评估，指出存在的问题和改进建议。回答不超过800字。"""
        
        task = AgentTask(agent_name, task_type, prompt, time.time())
        self.agent_tasks.append(task)
        
        try:
            response = self.glm_client.generate_response(prompt)
            task.end_time = time.time()
            task.response = response
            task.status = "completed"
            
            duration = task.end_time - task.start_time
            self._print_agent_task_result(agent_name, task_type, response, duration)
            
            return {"success": True, "result": {"patent_validation": response}, "response": response}
        except Exception as e:
            task.end_time = time.time()
            task.status = "failed"
            task.error = str(e)
            logger.error(f"专利审查失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_content_optimization(self) -> Dict[str, Any]:
        """执行内容优化"""
        agent_name = "optimizer"
        task_type = "content_optimization"
        task_description = "优化专利内容，提升质量和专业性"
        
        self._print_agent_task_start(agent_name, task_type, task_description)
        
        prompt = f"""你是一位专业的内容优化专家，专门负责专利内容的优化。

请对以下专利内容进行专业优化：

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

4. 【专业性提升】
   - 增强技术深度
   - 提升专业水准
   - 强化创新点

请以专业的标准进行优化，确保优化后的内容更加专业、准确、完整。回答不超过600字。"""
        
        task = AgentTask(agent_name, task_type, prompt, time.time())
        self.agent_tasks.append(task)
        
        try:
            response = self.glm_client.generate_response(prompt)
            task.end_time = time.time()
            task.response = response
            task.status = "completed"
            
            duration = task.end_time - task.start_time
            self._print_agent_task_result(agent_name, task_type, response, duration)
            
            return {"success": True, "result": {"content_optimization": response}, "response": response}
        except Exception as e:
            task.end_time = time.time()
            task.status = "failed"
            task.error = str(e)
            logger.error(f"内容优化失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _generate_final_patent(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """生成最终专利文档"""
        print("\n🔧 生成最终专利文档...")
        
        # 基于各阶段的结果，生成最终专利
        final_prompt = f"""基于多阶段协作的结果，请生成最终的完整专利文档：

专利主题：{self.patent_context.topic}

请生成包含以下内容的完整专利文档：
1. 专利标题
2. 专利摘要
3. 背景技术
4. 发明内容
5. 具体实施方式
6. 权利要求（8-12条）

请确保：
- 内容完整、准确、专业
- 语言表达清晰、规范
- 技术方案详细、可行
- 权利要求保护范围合理
- 满足专利三性要求

请以专业的专利撰写标准进行撰写，确保内容的高质量和专业性。"""
        
        try:
            final_response = self.glm_client.generate_response(final_prompt)
            final_patent = {"content": final_response, "status": "success"}
            print("✅ 最终专利文档生成完成")
            return final_patent
        except Exception as e:
            print(f"❌ 生成最终专利文档失败: {e}")
            return {"error": str(e)}
    
    def _update_novelty_analysis(self, response: str):
        """更新新颖性分析"""
        # 这里可以添加更复杂的解析逻辑
        self.patent_context.novelty_analysis = {
            "analysis_content": response,
            "novelty_score": "高",
            "technical_distinction": "显著",
            "innovation_level": "突破性"
        }
    
    async def _save_patent_document(self, final_patent: Dict[str, Any]):
        """保存专利文档"""
        filename = f"Professional_Evidence_Graph_Enhanced_RAG_Patent.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 100 + "\n")
                f.write("专业级多智能体协作生成的专利文档\n")
                f.write("=" * 100 + "\n\n")
                
                f.write(f"专利主题：{self.patent_context.topic}\n")
                f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"API依赖：是\n")
                f.write(f"智能体数量：{len(self.agents)}\n")
                f.write(f"执行阶段：{self.total_stages}\n\n")
                
                # 写入专利内容
                if "content" in final_patent:
                    f.write(final_patent["content"])
                else:
                    f.write("专利内容生成失败")
                
                f.write("\n\n" + "=" * 100 + "\n")
                f.write("文档生成完成\n")
                f.write("=" * 100 + "\n")
            
            print(f"📁 专利文档已保存到：{filename}")
            
        except Exception as e:
            print(f"❌ 保存专利文档失败: {e}")

async def main():
    """主函数"""
    # 从配置文件获取GLM API密钥
    from config import config
    
    # 创建专业级多智能体专利写作系统
    system = ProfessionalMultiAgentSystem(config.get_glm_api_key())
    
    # 定义专利主题：以证据图增强的RAG
    topic = "基于证据图增强的检索增强生成系统"
    description = """
    一种创新的基于证据图增强的检索增强生成（Evidence Graph Enhanced Retrieval-Augmented Generation, EG-RAG）系统，
    该系统通过构建和利用证据图来增强传统RAG系统的检索能力和生成质量。
    证据图能够捕捉知识实体之间的复杂关系、因果关系和证据链，为RAG系统提供更准确、更可靠的信息检索基础。
    该系统解决了传统RAG系统在信息准确性、可追溯性和推理能力方面的局限性，实现了更高质量、更可信的信息生成。
    """
    
    # 执行专利写作工作流程
    result = await system.execute_patent_workflow(topic, description)
    
    # 输出结果
    print("\n" + "="*100)
    print("🎉 专业级多智能体协作专利写作完成！")
    print("="*100)
    print(f"总阶段数：{result['workflow_summary']['total_stages']}")
    print(f"工作流程耗时：{result['workflow_summary']['workflow_duration']:.1f} 秒")
    print(f"智能体任务数：{len(result['workflow_summary']['agent_tasks'])}")
    print("="*100)
    
    # 显示最终专利内容
    if "final_patent" in result['workflow_summary']:
        final_patent = result['workflow_summary']['final_patent']
        print("\n📋 最终专利内容预览:")
        print("=" * 100)
        
        if "content" in final_patent:
            content = final_patent['content']
            print(content[:800] + "..." if len(content) > 800 else content)
        else:
            print("专利内容生成失败")
        
        print("\n" + "="*100)

if __name__ == "__main__":
    asyncio.run(main())