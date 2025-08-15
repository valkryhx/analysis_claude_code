#!/usr/bin/env python3
"""
DuckDuckGo 高级搜索客户端
使用 duckduckgo-search 库提供更强大的搜索功能
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from duckduckgo_search import DDGS
    DUCKDUCKGO_AVAILABLE = True
except ImportError:
    DUCKDUCKGO_AVAILABLE = False
    logger.warning("duckduckgo-search 库未安装，将使用基础客户端")


@dataclass
class SearchResult:
    """搜索结果数据类"""
    title: str
    url: str
    snippet: str
    source: str
    additional_info: Optional[Dict[str, Any]] = None


class DuckDuckGoAdvancedClient:
    """DuckDuckGo 高级搜索客户端"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        初始化高级搜索客户端
        
        Args:
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.ddgs: Optional[DDGS] = None
        
        if DUCKDUCKGO_AVAILABLE:
            self.ddgs = DDGS()
        else:
            logger.warning("使用基础客户端模式")
    
    async def search(self, query: str, max_results: int = 10, 
                    search_type: str = "text") -> List[SearchResult]:
        """
        执行搜索查询
        
        Args:
            query: 搜索查询字符串
            max_results: 最大结果数量
            search_type: 搜索类型 ("text", "news", "images", "videos")
            
        Returns:
            搜索结果列表
        """
        if not DUCKDUCKGO_AVAILABLE:
            logger.error("duckduckgo-search 库未安装")
            return []
        
        try:
            if search_type == "text":
                return await self._text_search(query, max_results)
            elif search_type == "news":
                return await self._news_search(query, max_results)
            elif search_type == "images":
                return await self._image_search(query, max_results)
            elif search_type == "videos":
                return await self._video_search(query, max_results)
            else:
                logger.warning(f"不支持的搜索类型: {search_type}")
                return await self._text_search(query, max_results)
                
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return []
    
    async def _text_search(self, query: str, max_results: int) -> List[SearchResult]:
        """文本搜索"""
        try:
            results = []
            search_results = self.ddgs.text(query, max_results=max_results)
            
            for result in search_results:
                search_result = SearchResult(
                    title=result.get('title', ''),
                    url=result.get('link', ''),
                    snippet=result.get('body', ''),
                    source='DuckDuckGo Text Search',
                    additional_info={
                        'rank': result.get('rank', ''),
                        'host': result.get('host', ''),
                        'category': result.get('category', '')
                    }
                )
                results.append(search_result)
                
            return results
            
        except Exception as e:
            logger.error(f"文本搜索失败: {e}")
            return []
    
    async def _news_search(self, query: str, max_results: int) -> List[SearchResult]:
        """新闻搜索"""
        try:
            results = []
            search_results = self.ddgs.news(query, max_results=max_results)
            
            for result in search_results:
                search_result = SearchResult(
                    title=result.get('title', ''),
                    url=result.get('link', ''),
                    snippet=result.get('body', ''),
                    source='DuckDuckGo News Search',
                    additional_info={
                        'date': result.get('date', ''),
                        'source': result.get('source', ''),
                        'category': result.get('category', '')
                    }
                )
                results.append(search_result)
                
            return results
            
        except Exception as e:
            logger.error(f"新闻搜索失败: {e}")
            return []
    
    async def _image_search(self, query: str, max_results: int) -> List[SearchResult]:
        """图片搜索"""
        try:
            results = []
            search_results = self.ddgs.images(query, max_results=max_results)
            
            for result in search_results:
                search_result = SearchResult(
                    title=result.get('title', ''),
                    url=result.get('link', ''),
                    snippet=result.get('image', ''),
                    source='DuckDuckGo Image Search',
                    additional_info={
                        'width': result.get('width', ''),
                        'height': result.get('height', ''),
                        'source': result.get('source', '')
                    }
                )
                results.append(search_result)
                
            return results
            
        except Exception as e:
            logger.error(f"图片搜索失败: {e}")
            return []
    
    async def _video_search(self, query: str, max_results: int) -> List[SearchResult]:
        """视频搜索"""
        try:
            results = []
            search_results = self.ddgs.videos(query, max_results=max_results)
            
            for result in search_results:
                search_result = SearchResult(
                    title=result.get('title', ''),
                    url=result.get('link', ''),
                    snippet=result.get('description', ''),
                    source='DuckDuckGo Video Search',
                    additional_info={
                        'duration': result.get('duration', ''),
                        'source': result.get('source', ''),
                        'uploader': result.get('uploader', '')
                    }
                )
                results.append(search_result)
                
            return results
            
        except Exception as e:
            logger.error(f"视频搜索失败: {e}")
            return []
    
    async def search_multiple_types(self, query: str, max_results: int = 5) -> Dict[str, List[SearchResult]]:
        """
        执行多种类型的搜索
        
        Args:
            query: 搜索查询
            max_results: 每种类型的最大结果数量
            
        Returns:
            按类型分组的搜索结果
        """
        results = {}
        
        search_types = ["text", "news", "images", "videos"]
        
        for search_type in search_types:
            try:
                type_results = await self.search(query, max_results, search_type)
                results[search_type] = type_results
            except Exception as e:
                logger.error(f"{search_type} 搜索失败: {e}")
                results[search_type] = []
        
        return results
    
    def close(self):
        """关闭客户端"""
        if self.ddgs:
            self.ddgs.close()


# 同步版本的客户端
class DuckDuckGoAdvancedClientSync:
    """同步版本的 DuckDuckGo 高级搜索客户端"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        
    def search(self, query: str, max_results: int = 10, 
               search_type: str = "text") -> List[SearchResult]:
        """同步搜索方法"""
        return asyncio.run(self._async_search(query, max_results, search_type))
    
    async def _async_search(self, query: str, max_results: int, 
                           search_type: str) -> List[SearchResult]:
        """内部异步搜索方法"""
        async with DuckDuckGoAdvancedClient(self.timeout, self.max_retries) as client:
            return await client.search(query, max_results, search_type)
    
    def search_multiple_types(self, query: str, max_results: int = 5) -> Dict[str, List[SearchResult]]:
        """同步多类型搜索方法"""
        return asyncio.run(self._async_search_multiple_types(query, max_results))
    
    async def _async_search_multiple_types(self, query: str, 
                                         max_results: int) -> Dict[str, List[SearchResult]]:
        """内部异步多类型搜索方法"""
        async with DuckDuckGoAdvancedClient(self.timeout, self.max_retries) as client:
            return await client.search_multiple_types(query, max_results)


# 使用示例
async def main():
    """主函数示例"""
    if not DUCKDUCKGO_AVAILABLE:
        print("❌ duckduckgo-search 库未安装")
        print("请运行: pip install duckduckgo-search")
        return
    
    query = "artificial intelligence patents"
    
    print(f"🔍 高级搜索查询: {query}")
    print("=" * 60)
    
    # 使用异步客户端
    async with DuckDuckGoAdvancedClient() as client:
        # 文本搜索
        print("\n1. 文本搜索:")
        text_results = await client.search(query, max_results=3, search_type="text")
        for i, result in enumerate(text_results, 1):
            print(f"   {i}. {result.title}")
            print(f"      URL: {result.url}")
            print(f"      摘要: {result.snippet[:80]}...")
        
        # 新闻搜索
        print("\n2. 新闻搜索:")
        news_results = await client.search(query, max_results=3, search_type="news")
        for i, result in enumerate(news_results, 1):
            print(f"   {i}. {result.title}")
            print(f"      URL: {result.url}")
            print(f"      日期: {result.additional_info.get('date', 'N/A')}")
        
        # 多类型搜索
        print("\n3. 多类型搜索:")
        all_results = await client.search_multiple_types(query, max_results=2)
        for search_type, results in all_results.items():
            print(f"\n   {search_type.upper()} 结果 ({len(results)} 个):")
            for i, result in enumerate(results, 1):
                print(f"     {i}. {result.title}")
    
    # 使用同步客户端
    print("\n" + "="*60)
    print("4. 使用同步客户端:")
    sync_client = DuckDuckGoAdvancedClientSync()
    sync_results = sync_client.search(query, max_results=2, search_type="text")
    for i, result in enumerate(sync_results, 1):
        print(f"   {i}. {result.title}")
        print(f"      URL: {result.url}")


if __name__ == "__main__":
    asyncio.run(main())