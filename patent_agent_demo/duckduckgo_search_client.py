#!/usr/bin/env python3
"""
DuckDuckGo Search Client
提供免费的搜索功能，替代 Google Search API
"""

import aiohttp
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DuckDuckGoSearchClient:
    """DuckDuckGo 搜索客户端"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        初始化搜索客户端
        
        Args:
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
            
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        执行搜索查询
        
        Args:
            query: 搜索查询字符串
            max_results: 最大结果数量
            
        Returns:
            搜索结果列表
        """
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
            
        # 构建搜索URL
        search_url = self._build_search_url(query, max_results)
        
        for attempt in range(self.max_retries):
            try:
                async with self.session.get(search_url) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        return self._parse_search_results(html_content, max_results)
                    else:
                        logger.warning(f"Search request failed with status {response.status}")
                        
            except Exception as e:
                logger.error(f"Search attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # 指数退避
                    
        logger.error("All search attempts failed")
        return []
    
    def _build_search_url(self, query: str, max_results: int) -> str:
        """
        构建搜索URL
        
        Args:
            query: 搜索查询
            max_results: 结果数量
            
        Returns:
            完整的搜索URL
        """
        base_url = "https://html.duckduckgo.com/html/"
        params = {
            'q': query,
            'kl': 'us-en',  # 语言和地区
            'kp': '1',      # 安全搜索级别
        }
        
        # 构建查询字符串
        query_string = '&'.join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
        return f"{base_url}?{query_string}"
    
    def _parse_search_results(self, html_content: str, max_results: int) -> List[Dict[str, Any]]:
        """
        解析HTML搜索结果
        
        Args:
            html_content: HTML内容
            max_results: 最大结果数量
            
        Returns:
            解析后的搜索结果列表
        """
        results = []
        
        try:
            # 简单的HTML解析，查找搜索结果
            # 这里使用基本的字符串搜索，实际项目中可能需要更复杂的HTML解析
            
            # 查找结果链接
            lines = html_content.split('\n')
            for line in lines:
                if 'class="result__title"' in line and len(results) < max_results:
                    # 提取标题和链接
                    title_start = line.find('>')
                    title_end = line.find('</a>')
                    if title_start != -1 and title_end != -1:
                        title = line[title_start + 1:title_end].strip()
                        
                        # 查找链接
                        href_start = line.find('href="')
                        if href_start != -1:
                            href_end = line.find('"', href_start + 6)
                            if href_end != -1:
                                url = line[href_start + 6:href_end]
                                
                                # 查找摘要
                                snippet = ""
                                for snippet_line in lines:
                                    if 'class="result__snippet"' in snippet_line:
                                        snippet_start = snippet_line.find('>')
                                        snippet_end = snippet_line.find('</p>')
                                        if snippet_start != -1 and snippet_end != -1:
                                            snippet = snippet_line[snippet_start + 1:snippet_end].strip()
                                            break
                                
                                results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': 'DuckDuckGo'
                                })
                                
        except Exception as e:
            logger.error(f"Error parsing search results: {e}")
            
        return results
    
    async def search_simple(self, query: str) -> List[Dict[str, Any]]:
        """
        使用DuckDuckGo Instant Answer API进行简单搜索
        
        Args:
            query: 搜索查询
            
        Returns:
            搜索结果
        """
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
            
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_instant_answer(data)
                else:
                    logger.warning(f"Instant answer request failed with status {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Instant answer search failed: {e}")
            return []
    
    def _parse_instant_answer(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        解析即时答案API的响应
        
        Args:
            data: API响应数据
            
        Returns:
            解析后的结果
        """
        results = []
        
        try:
            # 添加主题摘要
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', 'Summary'),
                    'url': data.get('AbstractURL', ''),
                    'snippet': data.get('Abstract', ''),
                    'source': 'DuckDuckGo Instant Answer'
                })
            
            # 添加相关主题
            for topic in data.get('RelatedTopics', [])[:5]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('Text', ''),
                        'url': topic.get('FirstURL', ''),
                        'snippet': topic.get('Text', ''),
                        'source': 'DuckDuckGo Related Topic'
                    })
                    
        except Exception as e:
            logger.error(f"Error parsing instant answer: {e}")
            
        return results


# 同步版本的客户端（用于非异步环境）
class DuckDuckGoSearchClientSync:
    """同步版本的DuckDuckGo搜索客户端"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        
    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        同步搜索方法
        
        Args:
            query: 搜索查询
            max_results: 最大结果数量
            
        Returns:
            搜索结果列表
        """
        return asyncio.run(self._async_search(query, max_results))
    
    async def _async_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """内部异步搜索方法"""
        async with DuckDuckGoSearchClient(self.timeout, self.max_retries) as client:
            return await client.search(query, max_results)
    
    def search_simple(self, query: str) -> List[Dict[str, Any]]:
        """
        同步简单搜索方法
        
        Args:
            query: 搜索查询
            
        Returns:
            搜索结果列表
        """
        return asyncio.run(self._async_search_simple(query))
    
    async def _async_search_simple(self, query: str) -> List[Dict[str, Any]]:
        """内部异步简单搜索方法"""
        async with DuckDuckGoSearchClient(self.timeout, self.max_retries) as client:
            return await client.search_simple(query)


# 使用示例
async def main():
    """主函数示例"""
    query = "Python programming tutorial"
    
    print(f"搜索查询: {query}")
    print("=" * 50)
    
    # 使用异步客户端
    async with DuckDuckGoSearchClient() as client:
        print("1. 使用HTML搜索:")
        results = await client.search(query, max_results=5)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   摘要: {result['snippet'][:100]}...")
            print()
        
        print("2. 使用Instant Answer API:")
        instant_results = await client.search_simple(query)
        for i, result in enumerate(instant_results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   摘要: {result['snippet'][:100]}...")
            print()
    
    # 使用同步客户端
    print("3. 使用同步客户端:")
    sync_client = DuckDuckGoSearchClientSync()
    sync_results = sync_client.search(query, max_results=3)
    for i, result in enumerate(sync_results, 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print()


if __name__ == "__main__":
    asyncio.run(main())