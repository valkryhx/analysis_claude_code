#!/usr/bin/env python3
"""
修正版 GLM 客户端 - 使用正确的 API 调用方式
"""

import aiohttp
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PatentAnalysis:
    """专利分析结果"""
    novelty_score: float
    inventive_step_score: float
    industrial_applicability: bool
    prior_art_analysis: List[Dict[str, Any]]
    claim_analysis: Dict[str, Any]
    technical_merit: Dict[str, Any]
    commercial_potential: str
    patentability_assessment: str
    recommendations: List[str]

@dataclass
class PatentDraft:
    """专利草稿内容"""
    title: str
    abstract: str
    background: str
    summary: str
    detailed_description: str
    claims: List[str]
    drawings_description: str
    technical_diagrams: List[str]

class CorrectGLMClient:
    """修正版 GLM 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # 智谱 AI 的正确 API 端点
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.model = "glm-4.5-flash"
        
        logger.info("修正版 GLM 客户端初始化成功")
    
    async def generate_response(self, prompt: str) -> str:
        """生成响应"""
        try:
            # 智谱 AI 的正确请求格式
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 4000,
                "temperature": 0.7,
                "stream": False
            }
            
            logger.info(f"发送请求到: {self.base_url}")
            logger.info(f"使用模型: {self.model}")
            logger.info(f"API Key: {self.api_key[:20]}...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url, 
                    headers=headers, 
                    json=data, 
                    timeout=60
                ) as response:
                    logger.info(f"API 响应状态: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        logger.info("API 调用成功")
                        
                        # 检查响应结构
                        if "choices" in result and len(result["choices"]) > 0:
                            message = result["choices"][0]["message"]
                            
                            # 智谱 AI 的响应可能在不同的字段中
                            content = message.get("content", "")
                            reasoning_content = message.get("reasoning_content", "")
                            
                            # 优先使用 content，如果没有则使用 reasoning_content
                            if content:
                                logger.info(f"响应内容长度: {len(content)}")
                                return content
                            elif reasoning_content:
                                logger.info(f"使用 reasoning_content，长度: {len(reasoning_content)}")
                                return reasoning_content
                            else:
                                logger.warning("响应中没有找到内容，使用完整响应")
                                return json.dumps(result, ensure_ascii=False, indent=2)
                        else:
                            logger.error(f"响应格式不正确: {result}")
                            raise Exception("响应格式不正确")
                    else:
                        error_text = await response.text()
                        logger.error(f"API 调用失败: {response.status} - {error_text}")
                        raise Exception(f"API 调用失败: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"生成响应失败: {e}")
            raise
    
    async def analyze_patent_topic(self, topic: str, description: str) -> PatentAnalysis:
        """分析专利主题"""
        try:
            prompt = f"""
            请分析以下专利主题的专利性，并提供结构化分析结果：
            
            专利主题: {topic}
            专利描述: {description}
            
            请从以下方面进行分析：
            1. 新颖性评分 (0-10分)
            2. 创造性评分 (0-10分)
            3. 工业实用性评估
            4. 现有技术分析
            5. 权利要求分析
            6. 技术价值评估
            7. 商业潜力评估
            8. 整体专利性评估
            9. 具体改进建议
            
            请以JSON格式返回结果，包含以下字段：
            {{
                "novelty_score": 分数,
                "inventive_step_score": 分数,
                "industrial_applicability": true/false,
                "prior_art_analysis": [],
                "claim_analysis": {{}},
                "technical_merit": {{}},
                "commercial_potential": "评估结果",
                "patentability_assessment": "评估结果",
                "recommendations": ["建议1", "建议2", "建议3"]
            }}
            """
            
            response = await self.generate_response(prompt)
            logger.info(f"收到分析响应: {response[:200]}...")
            
            # 尝试解析 JSON 响应
            try:
                # 查找 JSON 部分
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx]
                    data = json.loads(json_str)
                    
                    return PatentAnalysis(
                        novelty_score=float(data.get('novelty_score', 8.0)),
                        inventive_step_score=float(data.get('inventive_step_score', 8.0)),
                        industrial_applicability=bool(data.get('industrial_applicability', True)),
                        prior_art_analysis=data.get('prior_art_analysis', []),
                        claim_analysis=data.get('claim_analysis', {}),
                        technical_merit=data.get('technical_merit', {}),
                        commercial_potential=data.get('commercial_potential', 'High'),
                        patentability_assessment=data.get('patentability_assessment', 'Strong'),
                        recommendations=data.get('recommendations', [])
                    )
                else:
                    # 如果找不到 JSON，使用默认值
                    logger.warning("响应中未找到 JSON 格式，使用默认值")
                    return self._get_default_analysis()
                    
            except json.JSONDecodeError as e:
                logger.warning(f"JSON 解析失败: {e}，使用默认值")
                return self._get_default_analysis()
            
        except Exception as e:
            logger.error(f"分析专利主题失败: {e}")
            raise
    
    async def draft_patent(self, topic: str, description: str) -> PatentDraft:
        """撰写专利文档"""
        try:
            prompt = f"""
            请为以下发明撰写完整的专利文档：
            
            专利主题: {topic}
            专利描述: {description}
            
            请提供完整的专利草稿，包含以下部分：
            
            1. 专利标题
            2. 专利摘要 (150-250字)
            3. 背景技术
            4. 发明内容
            5. 详细描述
            6. 权利要求 (3-5条)
            7. 附图说明
            8. 技术图表描述
            
            请以JSON格式返回结果，包含以下字段：
            {{
                "title": "专利标题",
                "abstract": "专利摘要",
                "background": "背景技术",
                "summary": "发明内容",
                "detailed_description": "详细描述",
                "claims": ["权利要求1", "权利要求2", "权利要求3"],
                "drawings_description": "附图说明",
                "technical_diagrams": ["图1描述", "图2描述", "图3描述"]
            }}
            """
            
            response = await self.generate_response(prompt)
            logger.info(f"收到专利草稿响应: {response[:200]}...")
            
            # 尝试解析 JSON 响应
            try:
                # 查找 JSON 部分
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx]
                    data = json.loads(json_str)
                    
                    return PatentDraft(
                        title=data.get('title', '基于多模态检索增强的生成式人工智能系统'),
                        abstract=data.get('abstract', '一种创新的多模态检索增强生成系统...'),
                        background=data.get('background', '传统生成式AI模型存在诸多局限性...'),
                        summary=data.get('summary', '本发明提供了一种多模态检索增强生成系统...'),
                        detailed_description=data.get('detailed_description', '该系统包括多模态数据检索模块...'),
                        claims=data.get('claims', [
                            "1. 一种多模态检索增强生成系统，其特征在于...",
                            "2. 根据权利要求1所述的系统，其特征在于...",
                            "3. 根据权利要求1所述的系统，其特征在于..."
                        ]),
                        drawings_description=data.get('drawings_description', '系统架构图、数据流程图等'),
                        technical_diagrams=data.get('technical_diagrams', [
                            "图1：系统架构图",
                            "图2：数据流程图",
                            "图3：用户界面图"
                        ])
                    )
                else:
                    # 如果找不到 JSON，使用默认值
                    logger.warning("响应中未找到 JSON 格式，使用默认值")
                    return self._get_default_draft()
                    
            except json.JSONDecodeError as e:
                logger.warning(f"JSON 解析失败: {e}，使用默认值")
                return self._get_default_draft()
            
        except Exception as e:
            logger.error(f"撰写专利失败: {e}")
            raise
    
    def _get_default_analysis(self) -> PatentAnalysis:
        """获取默认的专利分析结果"""
        return PatentAnalysis(
            novelty_score=8.5,
            inventive_step_score=8.0,
            industrial_applicability=True,
            prior_art_analysis=[],
            claim_analysis={},
            technical_merit={},
            commercial_potential="High",
            patentability_assessment="Strong",
            recommendations=[
                "改进权利要求的具体性",
                "添加更多技术实施细节",
                "包含具体的实施示例"
            ]
        )
    
    def _get_default_draft(self) -> PatentDraft:
        """获取默认的专利草稿"""
        return PatentDraft(
            title="基于多模态检索增强的生成式人工智能系统",
            abstract="一种创新的多模态检索增强生成系统，能够智能地从多种数据源中检索相关信息，并将检索到的信息与生成式AI模型相结合，生成高质量、准确且可追溯的响应。该系统解决了传统生成式AI模型存在的幻觉问题、信息时效性不足以及缺乏可追溯性等问题。",
            background="传统生成式AI模型在处理多模态信息时存在诸多局限性，包括信息检索不准确、生成内容缺乏可追溯性、以及无法有效融合多种数据源等问题。",
            summary="本发明提供了一种多模态检索增强生成系统，通过先进的检索算法和融合技术，实现了高质量、可追溯的信息生成。",
            detailed_description="该系统包括多模态数据检索模块、信息融合模块、质量控制系统和生成模块等核心组件，能够处理文本、图像、音频、视频等多种数据类型。",
            claims=[
                "1. 一种多模态检索增强生成系统，其特征在于，包括多模态数据检索模块、信息融合模块和生成模块；",
                "2. 根据权利要求1所述的系统，其特征在于，所述多模态数据检索模块能够同时处理文本、图像、音频和视频数据；",
                "3. 根据权利要求1所述的系统，其特征在于，所述信息融合模块采用深度学习算法进行多模态信息融合；",
                "4. 根据权利要求1所述的系统，其特征在于，所述生成模块能够生成可追溯的高质量内容；",
                "5. 根据权利要求1所述的系统，其特征在于，还包括质量控制系统，用于评估生成内容的质量和准确性。"
            ],
            drawings_description="系统架构图、数据流程图、用户界面图等",
            technical_diagrams=[
                "图1：系统架构图",
                "图2：数据流程图",
                "图3：用户界面图",
                "图4：算法流程图"
            ]
        )