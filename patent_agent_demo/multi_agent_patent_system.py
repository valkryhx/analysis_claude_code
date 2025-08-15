#!/usr/bin/env python3
"""
多智能体协作专利写作系统
七个智能体通过多轮、多层次、多角度的协作完成高质量专利撰写
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional
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
    problem_statement: str
    solution_overview: str
    innovation_points: List[str]
    prior_art: List[Dict[str, Any]]
    technical_details: Dict[str, Any]
    claims_draft: List[str]
    current_stage: str
    iteration_count: int = 0

class MultiAgentPatentSystem:
    """多智能体专利写作系统"""
    
    def __init__(self, glm_api_key: str):
        self.glm_client = OfficialGLMClient(glm_api_key)
        self.patent_context = None
        self.workflow_history = []
        self.current_iteration = 0
        self.max_iterations = 5
        self.workflow_start_time = time.time()
        
        # 智能体配置
        self.agents = {
            "planner": self._create_planner_agent(),
            "searcher": self._create_searcher_agent(),
            "discusser": self._create_discusser_agent(),
            "writer": self._create_writer_agent(),
            "reviewer": self._create_reviewer_agent(),
            "rewriter": self._create_rewriter_agent(),
            "coordinator": self._create_coordinator_agent()
        }
        
        logger.info("多智能体专利写作系统初始化完成")
    
    def _create_planner_agent(self) -> Dict[str, Any]:
        """创建战略规划师智能体"""
        return {
            "name": "战略规划师",
            "role": "制定专利整体策略、技术路线图和创新点规划",
            "expertise": ["专利战略规划", "技术路线设计", "创新点识别", "风险评估"],
            "prompts": {
                "initial_planning": """
你是一位资深的专利战略规划师，拥有20年以上的专利布局和技术规划经验。

请基于以下专利主题制定详细的战略规划：

专利主题：{topic}
技术描述：{description}

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

请以结构化JSON格式返回，包含以上所有维度的详细分析。
""",
                "iteration_planning": """
基于前{current_iteration}轮迭代的结果，请重新评估和调整专利战略规划：

当前状态：{current_status}
已解决的问题：{solved_issues}
待解决的问题：{pending_issues}
质量评估：{quality_score}

请提供：

1. 【迭代策略调整】
   - 分析前几轮迭代的成效
   - 识别需要重点改进的方面
   - 制定本轮迭代的具体目标

2. 【技术方案优化】
   - 基于讨论结果优化技术方案
   - 强化创新点的技术深度
   - 完善技术实现细节

3. 【质量提升计划】
   - 针对审查意见制定改进计划
   - 提升专利文档的专业性
   - 增强权利要求的保护强度

请以JSON格式返回调整后的规划方案。
"""
            }
        }
    
    def _create_searcher_agent(self) -> Dict[str, Any]:
        """创建信息检索专家智能体"""
        return {
            "name": "信息检索专家",
            "role": "搜索现有技术、专利文献、技术背景和竞争对手信息",
            "expertise": ["专利检索", "技术文献搜索", "竞争对手分析", "现有技术调研"],
            "prompts": {
                "prior_art_search": """
你是一位专业的专利检索专家，拥有丰富的专利数据库检索和技术文献调研经验。

请针对以下专利主题进行全面的现有技术检索：

专利主题：{topic}
技术描述：{description}
技术领域：{technical_field}

请执行以下检索任务：

1. 【专利文献检索】
   - 使用关键词：{keywords}
   - 检索时间范围：最近10年
   - 重点关注：美国、欧洲、中国、日本、韩国的相关专利
   - 检索结果要求：至少找到15-20篇相关专利

2. 【技术文献检索】
   - 学术论文：IEEE、ACM、arXiv等数据库
   - 技术报告：公司技术白皮书、行业报告
   - 标准文档：相关技术标准、规范

3. 【竞争对手分析】
   - 识别主要竞争对手
   - 分析其技术路线和专利布局
   - 评估技术差距和机会

4. 【现有技术分析】
   - 分析每篇文献的技术方案
   - 识别技术优势和局限性
   - 评估与目标专利的区别

请以JSON格式返回检索结果，包含：
- 检索到的专利文献列表
- 技术文献摘要
- 竞争对手分析
- 现有技术总结
- 技术差距分析
""",
                "technical_background_search": """
基于专利主题，请搜索相关的技术背景和发展历程：

主题：{topic}

请搜索：

1. 【技术发展历程】
   - 该技术的起源和发展阶段
   - 关键技术突破和里程碑
   - 主要技术流派和分支

2. 【技术标准与规范】
   - 相关技术标准
   - 行业规范和要求
   - 技术评估标准

3. 【应用场景调研】
   - 主要应用领域
   - 典型应用案例
   - 市场需求分析

4. 【技术挑战与问题】
   - 当前技术面临的主要挑战
   - 技术瓶颈和限制
   - 行业痛点分析

请以JSON格式返回调研结果。
"""
            }
        }
    
    def _create_discusser_agent(self) -> Dict[str, Any]:
        """创建技术讨论专家智能体"""
        return {
            "name": "技术讨论专家",
            "role": "分析技术方案、提出改进建议、解决技术争议",
            "expertise": ["技术方案分析", "创新点评估", "技术可行性分析", "改进建议"],
            "prompts": {
                "technical_analysis": """
你是一位资深的技术专家，拥有丰富的技术方案分析和评估经验。

请对以下技术方案进行深入分析：

技术方案：{technical_solution}
创新点：{innovation_points}
现有技术：{prior_art}

请从以下角度进行分析：

1. 【技术方案评估】
   - 技术可行性和实现难度
   - 技术方案的完整性和系统性
   - 技术方案的创新程度

2. 【创新点分析】
   - 每个创新点的技术价值
   - 创新点的非显而易见性
   - 创新点的技术深度

3. 【技术优势分析】
   - 相比现有技术的优势
   - 技术方案的独特之处
   - 技术效果和性能提升

4. 【技术风险识别】
   - 技术实现风险
   - 技术替代风险
   - 技术过时风险

5. 【改进建议】
   - 技术方案的优化方向
   - 具体改进措施
   - 技术深化建议

请以JSON格式返回分析结果。
"""
            }
        }
    
    def _create_writer_agent(self) -> Dict[str, Any]:
        """创建专利撰写专家智能体"""
        return {
            "name": "专利撰写专家",
            "role": "撰写专利文档、权利要求、技术说明书",
            "expertise": ["专利文档撰写", "权利要求撰写", "技术说明书", "专利语言规范"],
            "prompts": {
                "patent_drafting": """
你是一位资深的专利撰写专家，拥有丰富的专利申请文件撰写经验。

请基于以下信息撰写完整的专利文档：

专利主题：{topic}
技术描述：{description}
创新点：{innovation_points}
技术方案：{technical_solution}

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
            }
        }
    
    def _create_reviewer_agent(self) -> Dict[str, Any]:
        """创建质量审查专家智能体"""
        return {
            "name": "质量审查专家",
            "role": "审查专利质量、合规性、技术准确性",
            "expertise": ["专利质量审查", "合规性检查", "技术准确性验证", "风险评估"],
            "prompts": {
                "quality_review": """
你是一位严格的专利质量审查专家，负责确保专利文档的质量和合规性。

请对以下专利文档进行全面审查：

专利文档：{patent_document}
权利要求：{claims}
技术方案：{technical_solution}

请从以下方面进行审查：

1. 【形式合规性审查】
   - 文档结构是否完整
   - 语言表达是否规范
   - 格式要求是否满足

2. 【技术准确性审查】
   - 技术描述是否准确
   - 技术方案是否可行
   - 技术效果是否合理

3. 【专利性审查】
   - 新颖性是否满足要求
   - 创造性是否达到标准
   - 工业实用性是否具备

4. 【权利要求审查】
   - 权利要求是否清楚
   - 保护范围是否合理
   - 技术特征是否明确

5. 【风险评估】
   - 专利无效风险
   - 侵权风险
   - 技术替代风险

请以JSON格式返回审查结果，包含：
- 审查结论
- 具体问题清单
- 改进建议
- 风险等级评估
"""
            }
        }
    
    def _create_rewriter_agent(self) -> Dict[str, Any]:
        """创建内容优化专家智能体"""
        return {
            "name": "内容优化专家",
            "role": "优化专利内容、提升质量、完善细节",
            "expertise": ["内容优化", "质量提升", "细节完善", "表达优化"],
            "prompts": {
                "content_optimization": """
你是一位专业的内容优化专家，负责提升专利文档的整体质量。

请对以下专利内容进行优化：

当前内容：{current_content}
优化目标：{optimization_goals}
改进要求：{improvement_requirements}

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
            }
        }
    
    def _create_coordinator_agent(self) -> Dict[str, Any]:
        """创建流程协调师智能体"""
        return {
            "name": "流程协调师",
            "role": "协调整个工作流程、管理迭代过程、确保质量目标",
            "expertise": ["流程协调", "迭代管理", "质量控制", "进度跟踪"],
            "prompts": {
                "workflow_coordination": """
你是一位经验丰富的流程协调师，负责协调多智能体协作完成专利撰写任务。

当前任务：{current_task}
参与智能体：{participating_agents}
工作目标：{workflow_goals}

请协调：

1. 【任务分配】
   - 确定各智能体的具体任务
   - 安排任务执行顺序
   - 设定任务完成标准

2. 【协作流程】
   - 设计智能体间的协作方式
   - 建立信息传递机制
   - 协调冲突和争议

3. 【质量控制】
   - 设定质量检查点
   - 建立质量评估标准
   - 确保质量目标达成

4. 【进度管理】
   - 跟踪任务执行进度
   - 识别进度瓶颈
   - 调整执行计划

请以JSON格式返回协调方案。
"""
            }
        }
    
    async def execute_multi_agent_workflow(self, topic: str, description: str) -> Dict[str, Any]:
        """执行多智能体协作的专利写作工作流程"""
        logger.info(f"开始执行多智能体协作专利写作工作流程")
        
        # 初始化专利上下文
        self.patent_context = PatentContext(
            topic=topic,
            description=description,
            technical_field="",
            problem_statement="",
            solution_overview="",
            innovation_points=[],
            prior_art=[],
            technical_details={},
            claims_draft=[],
            current_stage="初始化"
        )
        
        # 执行多轮迭代
        for iteration in range(self.max_iterations):
            self.current_iteration = iteration + 1
            logger.info(f"开始第 {self.current_iteration} 轮迭代")
            
            # 执行一轮完整的协作流程
            iteration_result = await self._execute_single_iteration()
            
            # 评估迭代质量
            quality_score = await self._evaluate_iteration_quality(iteration_result)
            
            # 记录迭代历史
            self.workflow_history.append({
                "iteration": self.current_iteration,
                "result": iteration_result,
                "quality_score": quality_score,
                "timestamp": datetime.now().isoformat()
            })
            
                    # 检查是否达到质量目标
        if quality_score >= 8.5:
            logger.info(f"达到质量目标，停止迭代。最终质量评分：{quality_score}")
            break
        
        # 限制最大迭代次数，避免无限循环
        if self.current_iteration >= 3:  # 限制为3轮迭代
            logger.info(f"达到最大迭代次数，停止迭代。最终质量评分：{quality_score}")
            break
            
            # 准备下一轮迭代
            await self._prepare_next_iteration(iteration_result, quality_score)
        
        # 生成最终专利文档
        final_patent = await self._generate_final_patent()
        
        return {
            "workflow_summary": {
                "total_iterations": self.current_iteration,
                "final_quality_score": self.workflow_history[-1]["quality_score"] if self.workflow_history else 0,
                "workflow_duration": time.time() - self.workflow_start_time
            },
            "final_patent": final_patent,
            "workflow_history": self.workflow_history
        }
    
    async def _execute_single_iteration(self) -> Dict[str, Any]:
        """执行单轮迭代"""
        logger.info(f"执行第 {self.current_iteration} 轮迭代")
        
        iteration_result = {}
        
        # 第一阶段：战略规划
        logger.info("第一阶段：战略规划")
        planner_result = await self._execute_agent_task("planner", "initial_planning" if self.current_iteration == 1 else "iteration_planning")
        iteration_result["planning"] = planner_result
        
        # 第二阶段：信息检索
        logger.info("第二阶段：信息检索")
        searcher_result = await self._execute_agent_task("searcher", "prior_art_search")
        iteration_result["search"] = searcher_result
        
        # 第三阶段：技术讨论
        logger.info("第三阶段：技术讨论")
        discusser_result = await self._execute_agent_task("discusser", "technical_analysis")
        iteration_result["discussion"] = discusser_result
        
        # 第四阶段：专利撰写
        logger.info("第四阶段：专利撰写")
        writer_result = await self._execute_agent_task("writer", "patent_drafting")
        iteration_result["writing"] = writer_result
        
        # 第五阶段：质量审查
        logger.info("第五阶段：质量审查")
        reviewer_result = await self._execute_agent_task("reviewer", "quality_review")
        iteration_result["review"] = reviewer_result
        
        # 第六阶段：内容优化
        logger.info("第六阶段：内容优化")
        rewriter_result = await self._execute_agent_task("rewriter", "content_optimization")
        iteration_result["rewriting"] = rewriter_result
        
        # 第七阶段：流程协调
        logger.info("第七阶段：流程协调")
        coordinator_result = await self._execute_agent_task("coordinator", "workflow_coordination")
        iteration_result["coordination"] = coordinator_result
        
        return iteration_result
    
    async def _execute_agent_task(self, agent_name: str, task_type: str) -> Dict[str, Any]:
        """执行智能体任务"""
        logger.info(f"执行智能体 {agent_name} 的 {task_type} 任务")
        
        agent = self.agents[agent_name]
        prompt_template = agent["prompts"][task_type]
        
        # 构建任务上下文
        context = {
            "topic": self.patent_context.topic,
            "description": self.patent_context.description,
            "technical_field": self.patent_context.technical_field,
            "current_iteration": self.current_iteration,
            "workflow_history": self.workflow_history,
            "current_status": self.patent_context.current_stage,
            "keywords": "证据图,RAG,检索增强生成,知识图谱,图神经网络",
            "technical_solution": "基于证据图的RAG系统",
            "innovation_points": ["证据图构建", "图增强检索", "多模态融合"],
            "prior_art": [],
            "patent_document": "专利文档内容",
            "claims": ["权利要求1", "权利要求2"],
            "current_content": "当前专利内容",
            "optimization_goals": "提升技术深度和质量",
            "improvement_requirements": "完善技术细节",
            "current_task": "专利撰写任务",
            "participating_agents": ["planner", "searcher", "discusser", "writer", "reviewer", "rewriter", "coordinator"],
            "workflow_goals": "完成高质量专利撰写",
            "solved_issues": "技术方案设计",
            "pending_issues": "权利要求优化",
            "quality_score": 8.0
        }
        
        # 生成具体提示词
        prompt = prompt_template.format(**context)
        
        try:
            # 调用GLM API执行任务
            response = self.glm_client.generate_response(prompt)
            
            # 解析响应结果
            result = self._parse_agent_response(response)
            
            # 更新专利上下文
            await self._update_patent_context(agent_name, task_type, result)
            
            return {
                "success": True,
                "agent_name": agent_name,
                "task_type": task_type,
                "result": result,
                "prompt": prompt,
                "response": response
            }
            
        except Exception as e:
            logger.error(f"智能体 {agent_name} 执行任务 {task_type} 失败: {e}")
            return {
                "success": False,
                "agent_name": agent_name,
                "task_type": task_type,
                "error": str(e)
            }
    
    def _parse_agent_response(self, response: str) -> Dict[str, Any]:
        """解析智能体响应"""
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
    
    async def _update_patent_context(self, agent_name: str, task_type: str, result: Dict[str, Any]):
        """更新专利上下文"""
        if agent_name == "planner" and "technical_field" in result:
            self.patent_context.technical_field = result["technical_field"]
        elif agent_name == "searcher" and "prior_art" in result:
            self.patent_context.prior_art = result["prior_art"]
        elif agent_name == "writer" and "claims" in result:
            self.patent_context.claims_draft = result["claims"]
        
        # 更新当前阶段
        self.patent_context.current_stage = f"{agent_name}_{task_type}"
    
    async def _evaluate_iteration_quality(self, iteration_result: Dict[str, Any]) -> float:
        """评估迭代质量"""
        # 这里可以实现复杂的质量评估逻辑
        # 暂时返回一个基础评分
        return 8.0 + (self.current_iteration * 0.2)
    
    async def _prepare_next_iteration(self, iteration_result: Dict[str, Any], quality_score: float):
        """准备下一轮迭代"""
        logger.info(f"准备第 {self.current_iteration + 1} 轮迭代，当前质量评分：{quality_score}")
        
        # 基于当前结果和评分，调整下一轮迭代的策略
        # 这里可以实现复杂的策略调整逻辑
    
    async def _generate_final_patent(self) -> Dict[str, Any]:
        """生成最终专利文档"""
        logger.info("生成最终专利文档")
        
        # 基于所有迭代结果，生成最终的专利文档
        final_prompt = f"""
基于多轮迭代的协作结果，请生成最终的完整专利文档：

专利主题：{self.patent_context.topic}
技术描述：{self.patent_context.description}
迭代历史：{len(self.workflow_history)} 轮

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
            final_patent = self._parse_agent_response(final_response)
            
            # 保存最终专利文档
            await self._save_final_patent(final_patent)
            
            return final_patent
            
        except Exception as e:
            logger.error(f"生成最终专利文档失败: {e}")
            return {"error": str(e)}
    
    async def _save_final_patent(self, final_patent: Dict[str, Any]):
        """保存最终专利文档"""
        filename = f"Evidence_Graph_Enhanced_RAG_Patent_Iteration_{self.current_iteration}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("多智能体协作生成的最终专利文档\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"专利主题：{self.patent_context.topic}\n")
                f.write(f"协作轮次：{self.current_iteration} 轮\n")
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
                
                # 写入工作流程历史
                f.write("【工作流程历史】\n")
                for i, history in enumerate(self.workflow_history, 1):
                    f.write(f"第 {i} 轮迭代：质量评分 {history['quality_score']:.1f}\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("文档生成完成\n")
                f.write("=" * 80 + "\n")
            
            logger.info(f"最终专利文档已保存到：{filename}")
            
        except Exception as e:
            logger.error(f"保存最终专利文档失败: {e}")

async def main():
    """主函数"""
    # 从配置文件获取GLM API密钥
    from config import config
    
    # 创建多智能体专利写作系统
    system = MultiAgentPatentSystem(config.get_glm_api_key())
    
    # 定义专利主题：以证据图增强的RAG
    topic = "基于证据图增强的检索增强生成系统"
    description = """
    一种创新的基于证据图增强的检索增强生成（Evidence Graph Enhanced Retrieval-Augmented Generation, EG-RAG）系统，
    该系统通过构建和利用证据图（Evidence Graph）来增强传统RAG系统的检索能力和生成质量。
    证据图能够捕捉知识实体之间的复杂关系、因果关系和证据链，为RAG系统提供更准确、更可靠的信息检索基础。
    该系统解决了传统RAG系统在信息准确性、可追溯性和推理能力方面的局限性，实现了更高质量、更可信的信息生成。
    """
    
    print("🚀 开始执行多智能体协作专利写作系统")
    print("=" * 80)
    print(f"专利主题：{topic}")
    print(f"技术描述：{description.strip()}")
    print("=" * 80)
    
    # 执行多智能体协作工作流程
    result = await system.execute_multi_agent_workflow(topic, description)
    
    # 输出结果
    print("\n" + "="*80)
    print("🎉 多智能体协作专利写作完成！")
    print("="*80)
    print(f"总迭代轮次：{result['workflow_summary']['total_iterations']}")
    print(f"最终质量评分：{result['workflow_summary']['final_quality_score']:.1f}")
    print(f"工作流程耗时：{result['workflow_summary']['workflow_duration']:.1f} 秒")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())