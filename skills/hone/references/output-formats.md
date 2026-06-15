# Output Formats

Use concise Chinese by default. Lead with the recommendation and next action.

## Discover Short List

```md
## Hone Discover
范围：过去 7 天
来源：GitHub Trending / HN / Reddit / linux.do / Product Hunt

### 建议 shape
1. <title>
   来源：<source> · <tier>/<confidence>
   链接：<url>
   为什么重要：<one sentence>
   推荐动作：shape

### 建议 deep read
...
```

## Signal Candidate

Use this schema for saved scout reports or deep output:

```json
{
  "title": "string",
  "source": "github_trending | hacker_news | reddit | linux_do | product_hunt | official",
  "sourceUrl": "string",
  "publishedAt": "string | null",
  "fetchedAt": "string",
  "sourceTier": "official | maintainer | community",
  "confidence": "confirmed | maintainer_claimed | community_reported | unverified",
  "topicTags": ["skill", "mcp", "workflow"],
  "heat": {
    "stars": 0,
    "comments": 0,
    "upvotes": 0,
    "rank": 0
  },
  "whatHappened": "发生了什么",
  "whyItMatters": "为什么对本地 agent harness 有影响",
  "localPracticeHypothesis": "可能沉淀成什么本地实践",
  "recommendedAction": "ignore | watch | deep_read | shape",
  "reasoning": "为什么给这个动作"
}
```

## Apply Result

```md
已生成/写入：<path>
验证：pass | warn | skipped
试用：<prompt or command>
剩余风险：<0-2 bullets>
```

## Check Finding

```md
- [type/severity] <title>
  位置：<paths>
  证据：<short evidence>
  建议：<draft fix / needs decision / watch>
```
