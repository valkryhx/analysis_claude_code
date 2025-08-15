#!/usr/bin/env python3
"""
测试 DuckDuckGo 搜索客户端
"""

import asyncio
from duckduckgo_search_client import DuckDuckGoSearchClient, DuckDuckGoSearchClientSync


async def test_async_search():
    """测试异步搜索"""
    print("🔍 测试异步搜索...")
    
    async with DuckDuckGoSearchClient() as client:
        # 测试基本搜索
        query = "Python machine learning"
        print(f"搜索查询: {query}")
        
        results = await client.search(query, max_results=3)
        print(f"找到 {len(results)} 个结果:")
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   摘要: {result['snippet'][:80]}...")
            print(f"   来源: {result['source']}")
        
        # 测试即时答案API
        print("\n" + "="*50)
        print("🔍 测试即时答案API...")
        
        instant_results = await client.search_simple(query)
        print(f"即时答案结果: {len(instant_results)} 个")
        
        for i, result in enumerate(instant_results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   摘要: {result['snippet'][:80]}...")
            print(f"   来源: {result['source']}")


def test_sync_search():
    """测试同步搜索"""
    print("\n" + "="*50)
    print("🔍 测试同步搜索...")
    
    client = DuckDuckGoSearchClientSync()
    query = "DuckDuckGo search engine"
    
    print(f"搜索查询: {query}")
    
    results = client.search(query, max_results=2)
    print(f"找到 {len(results)} 个结果:")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   摘要: {result['snippet'][:80]}...")
        print(f"   来源: {result['source']}")


async def test_patent_search():
    """测试专利相关搜索"""
    print("\n" + "="*50)
    print("🔍 测试专利相关搜索...")
    
    async with DuckDuckGoSearchClient() as client:
        queries = [
            "patent filing process",
            "intellectual property rights",
            "patent search database"
        ]
        
        for query in queries:
            print(f"\n搜索: {query}")
            results = await client.search(query, max_results=2)
            
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']}")
                print(f"     URL: {result['url']}")


async def main():
    """主测试函数"""
    print("🚀 开始测试 DuckDuckGo 搜索客户端")
    print("="*60)
    
    try:
        # 测试异步搜索
        await test_async_search()
        
        # 测试同步搜索
        test_sync_search()
        
        # 测试专利相关搜索
        await test_patent_search()
        
        print("\n✅ 所有测试完成!")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())