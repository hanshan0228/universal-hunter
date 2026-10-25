# Universal Hunter Anti-Ban & Countermeasures (2026 Edition)

## 🛡️ 平台风控对抗与生存指南

### 1. Reddit 2026 最新反作弊机制剖析
- **SimHash 聚类算法**: Reddit 不仅检测完全相同的文本，还会将同一账号发出的评论进行 SimHash / MinHash 降维聚类。如果一个账号最近发出的 10 条评论相似度超过 50%，会被打上 `heuristic_spammer` 标签，后续所有评论直接进 Shadow-remove。
- **AutoMod 正文正则**:
  - `domain: [any external url]` -> 绝大多数商业版块（如 r/tiktokads）直接静默移除。
  - `body: ["dm me", "let me know", "hit me up", "inbox me"]` -> 直接触发 Rule 6 (No Solicitation)。
- **Karma 权重过滤**:
  - `comment_karma < 10`: 在商业版块的发言会自动折叠或暂扣队列。
  - `comment_karma < 50`: 触发高敏感版块的自动拦截。

### 2. Bio-Routing（主页承接）的核心生存法则
- **为什么 Bio-Routing 能做到 100% 存活？**
  - 版块 AutoMod 只能审查帖子和评论的正文。如果正文只有纯技术干货和个人经验，完全不出现任何链接和推销词，AutoMod 规则命中率为 0。
  - 潜在客户点击用户名查看你的 Reddit 个人 Profile 是 Reddit 官方鼓励的平台行为。
  - 在 Profile 置顶帖中放置 `https://adgrowth-lab.github.io/` 受到 Reddit 全局 Terms 保护（在自己的 Profile 发帖不违反特定版块规则）。
- **Profile 置顶帖搭建要点**:
  - 标题必须是提供价值，而不是单纯打广告：
    - ✅ *"Verified TikTok Agency Accounts with Tiered Spend Match: What Media Buyers Need to Know"*
    - ❌ *"Buy TikTok Agency Accounts Now at 50% Off"*
  - 正文把主要优势写清楚（白名单户、免每日限额、官方后台直接充值），并附上清爽的链接。

### 3. Jaccard 相似度排重算法应用
`scripts/db.py check_similarity` 实现了基于词集合的 Jaccard 距离检查：
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
当相似度计算结果 $\ge 0.50$ 时，必须强制改换角度，例如：
- 第一条从“$50 限额算法原理”切入；
- 第二条从“虚拟卡支付风控”切入；
- 第三条从“多像素资产隔离”切入。
每个切入点用不同的词汇，确保文本指纹彻底离散。

---

### 4. 逆向 Inbound DM 邀请与防 Solicitation 规则 (Inbound Hook Protocol)
- **为什么“我已私信你 (I sent you a DM)”会被秒封？**
  - Reddit / 𝕏 等社区风控将未经请求的主动私信与公开“已发私信”声明直接归类为高危垃圾营销（Spam Solicitation），极易触发用户举报与 AutoMod 静默封号。
- **逆向 Inbound 邀请公式 (The Reverse Inbound Formula)**:
  - **80% 硬核公开解惑 + 20% 高价值结构化资产缺口**。
  - 公开评论解答用户的底层技术疑问后，将繁琐的原始数据、对照表或申诉模板作为“可选索取资产”开放：
    - ✅ *"I benchmarked the pricing tiers and feature limits on a spreadsheet. If you want the comparison doc, feel free to shoot me a DM and I'll share it."*
    - ✅ *"Left the setup checklist on my profile, or drop me a note if you get stuck on the billing gateway error."*
    - ❌ *"DM me now to buy an account"*
    - ❌ *"Check your inbox I sent you a message"*
- **双向确认的安全优势**:
  - 当潜在买家被你的专业度打动，**主动向你发起第一条私信**时，平台通信系统判定此对话为“受邀社交互动 (Consensual Chat)”，风控阈值直接降为 0。
  - 1v1 私信对话转化率高达 30%~50%，且支持针对高客单用户引入 Telegram VIP Concierge 做深度服务。
