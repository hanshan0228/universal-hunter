# Niche Configuration Template

> 复制此模板到 `niches/<your_niche_name>/config.md` 即可快速装载新项目。

```yaml
niche_id: "your_niche_id"
name: "Your Project Name"
target_site: "https://your-landing-page.com"
site_brand: "YourBrand"

# 路由模式: bio_routing (推荐) | direct_link
routing_mode: "bio_routing"

# 物理 DOM 查重签名列表:
dom_exclusion_signatures:
  - "your-landing-page.com"
  - "YourBrand"

# Profile 置顶帖文案建议:
profile_pinned_post:
  title: "Your Value Guide Title"
  body: "Short description with link: https://your-landing-page.com | VIP Support: https://t.me/your_concierge"

# 回帖结尾自然埋钩短语库 (Bio-Routing 与 逆向 Inbound DM 邀请):
profile_hooks:
  - "pinned the complete breakdown on my profile if helpful."
  - "left the direct checklist in my bio."
  - "feel free to shoot me a DM if you want me to share the raw comparison sheet."
  - "left the notes on my profile, or drop me a note if you run into setup errors."

# 目标版块池:
target_subreddits:
  - "subreddit_1"
  - "subreddit_2"

# 关键词矩阵:
keywords:
  tier_1_hot_intent:
    - "buy [keyword]"
    - "recommend [keyword]"
    - "best [keyword] tool"
  tier_2_pain_comparison:
    - "[competitor] alternative"
    - "why is [competitor] so bad"
  tier_3_setup_advice:
    - "how to setup [keyword]"
    - "[keyword] tips for 2026"
```
