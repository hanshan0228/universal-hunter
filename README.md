# Universal Hunter 🛡️

> **Multi-Niche Stealth Traffic Hunter & High-Conversion Community Growth Sniper**  
> 专为高风控对抗平台（Reddit、𝕏、垂直论坛）设计的特战级社媒截流与流量增长框架。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)
[![Anti-Ban: Bio-Routing](https://img.shields.io/badge/Anti--Ban-Bio--Routing-purple.svg)](#)

---

## 🌟 核心理念 (Core Philosophy)

传统的批量群发脚本在 2026 年的高对抗平台早已失效。`Universal Hunter` 采用**真人级伪装与特种作战打法**：

1. **80% 侦查 (Scout) + 20% 狙击 (Sniper)**：
   - 80% 的时间在真实滚动、阅读、随机点赞，积累正常用户的行为指纹与 Trust Score。
   - 20% 的时间针对高意向求助帖发起精准打击。
2. **两段式隐形穿透 (Bio-Routing)**：
   - 公开回帖 **100% 纯干货、0 外链、0 商业工具词、0 机械招揽**。
   - 结尾通过自然的 Profile Hook 引导至个人主页置顶帖完成转化闭环，根除 AutoMod 删帖与 Shadowban。
3. **物理 DOM 现场排查 (Physical DOM Scan)**：
   - 打开页面后自动检查自己账号是否已在评论区、同类竞争对手或目标链接是否已露出，见缝插针，绝不盲目撞车。
4. **代码级 Jaccard 反聚类查重**：
   - 发帖前自动计算与最近 30 条回复的 Token 相似度，超过 50% 强制重写，彻底杜绝平台 SimHash 算法聚类打包封号。
5. **多项目原生隔离 (Multi-Niche Architecture)**：
   - 每个项目（Niche）拥有独立的配置文件、3-Tier 词库、每日配额与历史查重记录，互不干扰。

---

## 📂 项目结构

```
universal-hunter/
├── SKILL.md                          # 核心工作流与特种兵行动准则 (Agent Skill)
├── scripts/
│   └── db.py                         # 多项目 SQLite、Jaccard 去重、Karma 门禁引擎
├── niches/                           # 独立项目配置空间
│   ├── tiktok_agency/                # TikTok 海外代理户与 Spend Match 项目
│   │   └── config.md
│   ├── fairway_fort/                 # 高尔夫球车 LSV 合规与 VIN 查号项目
│   │   └── config.md
│   └── justmysocks/                  # 高速 CN2 GIA 网络节点服务项目
│       └── config.md
├── references/
│   ├── anti_ban_rules.md             # 2026 最新平台反作弊机制与避坑指引
│   ├── warmup_guide.md               # 养号与 Karma 爬坡阶段操作手册
│   └── templates/
│       └── config_template.md        # 新项目一键创建模板
└── data/
    └── .gitkeep                      # 运行时 SQLite 数据库目录 (history.db)
```

---

## 🚀 快速上手

### 1. 命令行直接调用 (CLI)

```bash
# 查看指定 Niche 今日配额与回复统计
python3 scripts/db.py stats tiktok_agency

# 检查关键词在过去 24 小时内是否使用过
python3 scripts/db.py check_keyword "tiktok agency account" tiktok_agency

# 记录选定关键词
python3 scripts/db.py log_keyword "tiktok agency account" tiktok_agency

# 检查回复内容是否与历史内容相似度过高 (>50% 触发反聚类保护)
python3 scripts/db.py check_similarity "Your proposed reply text..." tiktok_agency

# 检查账号 Karma 是否达到目标版块安全门禁
python3 scripts/db.py check_karma 65 tiktokads
```

### 2. 作为 Agent Skill 使用

在支持 OpenCode / Claude Code / Codex 的环境中，直接唤起：
> *"使用 `$universal-hunter`，执行一轮 TikTok 代理户获客任务"*

系统将自动加载 `niches/tiktok_agency/config.md`，执行 80% 闲逛、DOM 查重、Jaccard 校验、以及 Bio-Routing 精准跟帖。

---

## 🎯 预置 Niche 示例：TikTok 代理户与返佣

* **目标受众**：面临个人户 $50/天限额、频繁被误封、虚拟卡拒付、寻找官方返佣（Spend Match）的跨境卖家与 Media Buyer。
* **承接策略**：回帖纯粹拆解企业户白名单机制，引导查看主页置顶：`https://adgrowth-lab.github.io/`。
* **词库规模**：64 个自然长尾词，分级覆盖 Tier 1 (显性找户)、Tier 2 (封号痛点)、Tier 3 (投放起量)。

---

## 📄 License

MIT License.
