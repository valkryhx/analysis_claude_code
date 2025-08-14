#!/usr/bin/env python3
"""
配置文件 - 包含所有必要的 API keys 和配置参数
"""

import os
from typing import Optional

class Config:
    """配置类"""
    
    # GLM API 配置
    GLM_API_KEY = "f80163335a3749509ae1ecfa79f3f343.cNIEBuoFBDhkDpqZ"
    
    # 如果环境变量中有设置，则使用环境变量
    @classmethod
    def get_glm_api_key(cls) -> str:
        """获取 GLM API key"""
        return os.getenv("GLM_API_KEY", cls.GLM_API_KEY)
    
    # DuckDuckGo 搜索配置
    DUCKDUCKGO_TIMEOUT = 30
    DUCKDUCKGO_MAX_RETRIES = 3
    
    # 专利系统配置
    PATENT_SYSTEM_MAX_AGENTS = 10
    PATENT_SYSTEM_TIMEOUT = 300
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 模型配置
    GLM_MODEL = "glm-4.5-flash"
    GLM_MAX_TOKENS = 4000
    GLM_TEMPERATURE = 0.7
    
    # 搜索配置
    SEARCH_MAX_RESULTS = 10
    SEARCH_TIMEOUT = 30
    
    @classmethod
    def validate_config(cls) -> bool:
        """验证配置是否有效"""
        if not cls.get_glm_api_key():
            print("❌ GLM API key 未设置")
            return False
        
        print("✅ 配置验证通过")
        return True


# 创建全局配置实例
config = Config()