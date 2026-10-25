# Niche Configuration: TikTok Agency Accounts & Spend Match (Adgrowth-Lab)

> 专为 TikTok 海外买量、企业代理户开户、返佣与消耗满赠打造的特种作战配置。
> 采用 Bio-Routing 两段式隐形穿透打法，确保回帖 100% 存活，高意向流量回流至个人主页。

---

## 🎯 业务与承接定义 (Niche & Routing)

```yaml
niche_id: "tiktok_agency"
name: "TikTok Agency Accounts & Spend Match"
target_site: "https://adgrowth-lab.github.io/"
site_brand: "Adgrowth-Lab"

# 承接路由模式: 
#   - direct_link (崔晃晃直接留链接模式：直出落地页链接，适用求链接贴或宽松版块)
#   - bio_routing (主页置顶穿透模式：公域0外链，主页置顶帖承接，适用高风控商业版块)
#   - inbound_dm (逆向私信模式：公域抛出资产邀请私信，私域1v1 3轮攻坚收割，高客单首选)
#   - brand_search (品牌搜索模式：0外链0主页，引导搜索品牌词，防降权且反哺Google SEO)
#   - adaptive (智能自适应：根据帖子求助意图与版块风控自动选择最佳模式)
routing_mode: "adaptive"

# 物理 DOM 查重签名: 页面一旦出现以下任何字符串，立即撤离放弃回复
dom_exclusion_signatures:
  - "adgrowth-lab.github.io"
  - "adgrowth-lab"
  - "getstartedtiktok.partnerlinks.io"

# 模式专属回帖模版库 (Mode Specific Response Templates):

# 1. direct_link 模式话术 (直接带链接 · FTC规范披露):
direct_link_templates:
  - "been running 5 figures on tiktok ads. Personal accounts will always get hard-capped at $50/day during Q4. We switched to direct agency whitelist accounts with verified balance deposits. Here is the official partner portal with the tiered credit match up to $6,000: https://adgrowth-lab.github.io/ (disclosure: official partner route)."
  - "virtual cards get flagged constantly on new BMs right now. Official agency partner lines let you fund your Ads Manager balance directly with zero markup: https://adgrowth-lab.github.io/"

# 2. bio_routing 模式话术 (公域0外链 · 自然引导看主页):
profile_hooks:
  - "pinned a breakdown of verified agency tiers and spend match requirements on my profile if you need the checklist."
  - "left the notes on how we get direct agency accounts in my bio."
  - "details on the tiered spend match ($200 to $6,000 credit) are pinned on my profile if helpful."
  - "broke down the agency threshold requirements vs personal accounts on my profile."
  - "pinned our agency line onboarding checklist on my profile if you want to avoid account limits."

# 3. inbound_dm 模式话术 (资产缺口 · 邀请主动发私信):
inbound_dm_hooks:
  - "I benchmarked the agency pricing tiers and spend match requirements on a spreadsheet. Feel free to shoot me a DM and I'll send it over."
  - "put together a quick 1-page checklist on how to bypass the $50 spend hold without getting banned. Drop me a DM if you want me to share the doc."
  - "we mapped out the official spend match verification process vs secondary brokers. Shoot me a message if you want the breakdown spreadsheet."

# 4. brand_search 模式话术 (0外链0主页 · 搜索心智占坑 · 𝕏防降权):
brand_search_templates:
  - "We ended up checking our numbers on AdGrowth Lab's spend match calculator — turned out our monthly volume qualified for a 50% credit match directly in Ads Manager."
  - "Best practice is looking up the AdGrowth Lab TikTok agency tier matrix on Google. Explains the difference between self-serve $50 limits and whitelisted lines."

# Profile 置顶帖文案建议 (账号主页设置此内容即可完成转化闭环):
profile_pinned_post:
  title: "Official TikTok Agency Ad Accounts & Spend Match Tier Guide (Up to $6,000 Match)"
  body: "Complete breakdown of agency account tiers, whitelist status, no daily spend limits, and official TikTok Ads Manager balance deposits: https://adgrowth-lab.github.io/ | Enterprise VIP Telegram: https://t.me/adgrowth_lab"
```

---

## 👥 目标受众核心痛点 (Pain Points)

```yaml
pain_points:
  - id: "daily_limit"
    title: "新手个人户 $50/天消耗限额，爆品起量直接被卡死"
    symptom: "TikTok personal accounts capped at $50/day spend limit during learning phase"
    solution: "Agency accounts come with no daily spend limit from day 1."

  - id: "random_ban"
    title: "个人户跑几百刀就被误封，申诉无门，现金被吞"
    symptom: "Sudden account suspension/ban after spending $300-$500 with unhelpful bot support"
    solution: "Agency accounts run on whitelisted agency credit lines with dedicated rep support."

  - id: "pixel_loss"
    title: "封号导致 Pixel 连带报废，历史累计转化数据清零"
    symptom: "BM suspension wiping out pixel events and machine learning optimization"
    solution: "Agency accounts allow multi-pixel binding and cross-account asset sharing."

  - id: "card_declined"
    title: "虚拟卡/外币卡频繁拒付，触发支付高危风控"
    symptom: "TikTok Ads Manager payment failed / card declined loop"
    solution: "Agency direct balance top-up with monthly invoicing or wire/crypto support."

  - id: "spend_match"
    title: "高昂投放成本，寻找官方返佣和消耗补贴 (Spend Match)"
    symptom: "Looking for TikTok ad credits, rebates, promo codes, or cash back"
    solution: "Official tiered ad credits up to $6,000 matched directly into Ads Manager balance."
```

---

## 🔑 关键词矩阵 (3-Tier Keyword Matrix)

```yaml
target_subreddits:
  - "tiktokads"              # 核心阵地 (严格执行 Karma >= 50 门禁)
  - "dropship"               # 痛点聚集地 (个人户限额重灾区)
  - "dropshipping"
  - "shopify"                # 真实独立站卖家，有预算但缺户
  - "Affiliate_Marketing"    # 买量老手，极度看重返佣与抗封
  - "adops"                  # 关注代理账期与返点
  - "ecommerce"
  - "ppc"

keywords:
  tier_1_hot_intent:         # 显性需求：拿着钱找开户/返佣
    - "tiktok agency account"
    - "tiktok agency ad account"
    - "recommend tiktok agency"
    - "need tiktok agency"
    - "buy tiktok ad account"
    - "agency accounts for tiktok"
    - "tiktok ad credit"
    - "tiktok ad spend match"
    - "tiktok match spend"
    - "tiktok ad rebate"
    - "tiktok ad cashback"
    - "tiktok threshold account"
    - "tiktok agency partner"
    - "tiktok agency whitelist"

  tier_2_pain_comparison:    # 竞品与痛点：抱怨封号、限额、支付失败
    - "tiktok account suspended"
    - "tiktok account banned"
    - "tiktok ads daily limit"
    - "spend limit tiktok ads"
    - "tiktok ads daily limit 50"
    - "tiktok ads payment failed"
    - "tiktok ads card declined"
    - "tiktok agency account vs personal"
    - "scale tiktok ads budget"
    - "tiktok ads learning phase stuck"

  tier_3_setup_advice:       # 基础交流：新号投放、像素配置、起量经验 (纯干货树立人设)
    - "first tiktok ad campaign"
    - "running tiktok ads dropshipping"
    - "tiktok events api setup"
    - "tiktok pixel deduplication"
    - "try tiktok ads 2026"
    - "run ads on tiktok"
```

---

## 🎭 角色与人设原则 (Persona & Voice)

```yaml
persona:
  identity: "Senior Media Buyer / E-commerce Growth Operator"
  tone: "Cold, professional, highly technical, slightly cynical about ad platforms, direct, no fluff"
  length: "35-65 words"
  rules:
    - "绝对不加任何 Emoji (不当热情客服)"
    - "绝对不出现 'Let me know if you need help' 或 'I can help with that' (严防 Solicitation 判定)"
    - "首字母概率小写，适当使用 media buying 圈内术语 (CBO, learning phase, agency line, BM, pixel fallback)"
    - "正文严禁出现任何外部 http/https 链接"
```
