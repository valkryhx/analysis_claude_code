# Migration Guide: From Google API to GLM-4.5-flash

This guide will help you migrate your patent agent system from Google AI API to GLM-4.5-flash API.

## 🚀 Why Migrate to GLM-4.5-flash?

- **Cost-effective**: GLM-4.5-flash offers competitive pricing
- **High performance**: Excellent Chinese and English language support
- **Reliable**: Stable API with good uptime
- **Feature-rich**: Supports all the functionality needed for patent analysis

## 📋 Prerequisites

1. **GLM API Key**: Get your API key from [Zhipu AI](https://open.bigmodel.cn/)
2. **API Key Format**: Your key should be in the format `id:secret`
3. **Python Environment**: Python 3.8+ with required dependencies

## 🔄 Migration Steps

### Step 1: Update Dependencies

Remove Google-specific dependencies:
```bash
pip uninstall google-generativeai langchain-google-genai
```

### Step 2: Update Environment Variables

Replace your `.env` file:
```env
# OLD (Google API)
# GOOGLE_API_KEY=your_google_api_key

# NEW (GLM API)
GLM_API_KEY=your_glm_api_id:your_glm_api_secret
```

### Step 3: Update Import Statements

Replace Google imports with GLM imports:

**Before (Google):**
```python
from google_a2a_client import get_google_a2a_client, SearchResult
```

**After (GLM):**
```python
from glm_client import get_glm_client, SearchResult
```

### Step 4: Update Client Initialization

**Before (Google):**
```python
self.google_a2a_client = await get_google_a2a_client()
```

**After (GLM):**
```python
self.glm_client = await get_glm_client()
```

### Step 5: Update Method Calls

**Before (Google):**
```python
analysis = await self.google_a2a_client.analyze_patent_topic(topic, description)
```

**After (GLM):**
```python
analysis = await self.glm_client.analyze_patent_topic(topic, description)
```

## 🧪 Testing the Migration

Run the test script to verify everything works:
```bash
python test_glm_client.py
```

## 📚 API Reference

### GLM Client Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `analyze_patent_topic()` | Analyze patent topic for patentability | `topic`, `description` |
| `search_prior_art()` | Search for prior art | `topic`, `keywords`, `max_results` |
| `generate_patent_draft()` | Generate patent draft | `topic`, `description`, `analysis` |
| `review_patent_draft()` | Review patent draft | `draft`, `analysis` |
| `optimize_patent_claims()` | Optimize patent claims | `claims`, `feedback` |
| `generate_technical_diagrams()` | Generate diagram descriptions | `description` |

### Configuration Options

```python
# Initialize with custom settings
client = GLMClient(api_key="your_custom_key")

# Use environment variable (recommended)
client = GLMClient()  # Uses GLM_API_KEY from .env
```

## 🔧 Troubleshooting

### Common Issues

1. **API Key Format Error**
   - Ensure your API key is in `id:secret` format
   - Check for extra spaces or special characters

2. **Authentication Failed**
   - Verify your API key is correct
   - Check if your account has sufficient credits

3. **Rate Limiting**
   - GLM API has rate limits, implement retry logic if needed
   - Consider implementing exponential backoff

### Error Messages

| Error | Solution |
|-------|----------|
| `API key must be in format 'id:secret'` | Check your API key format |
| `GLM API error: 401` | Invalid API key or expired |
| `GLM API error: 429` | Rate limit exceeded, wait and retry |

## 📊 Performance Comparison

| Metric | Google API | GLM-4.5-flash |
|--------|------------|----------------|
| Response Time | ~2-5s | ~1-3s |
| Token Limit | 30k | 128k |
| Cost per 1M tokens | $15 | $5 |
| Chinese Support | Limited | Excellent |
| API Stability | Good | Excellent |

## 🆘 Support

- **GLM API Documentation**: [https://open.bigmodel.cn/doc/api](https://open.bigmodel.cn/doc/api)
- **Zhipu AI Support**: [https://open.bigmodel.cn/](https://open.bigmodel.cn/)
- **GitHub Issues**: Report bugs in this repository

## 🎯 Next Steps

After successful migration:

1. **Monitor Performance**: Track response times and success rates
2. **Optimize Prompts**: Fine-tune prompts for better GLM performance
3. **Implement Caching**: Add response caching to reduce API calls
4. **Add Fallbacks**: Implement fallback to other AI providers if needed

## 📝 Migration Checklist

- [ ] Update dependencies
- [ ] Configure GLM API key
- [ ] Update import statements
- [ ] Update client initialization
- [ ] Update method calls
- [ ] Test functionality
- [ ] Update documentation
- [ ] Deploy changes
- [ ] Monitor performance

---

**Need help?** Open an issue in this repository or check the GLM API documentation.