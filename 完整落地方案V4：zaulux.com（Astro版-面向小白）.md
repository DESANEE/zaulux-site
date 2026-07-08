# 完整落地方案V4.1：zaulux.com（Astro +阿里云域名+Vercel+Cloudflare+搬瓦工+本地Hermes运维）

> **版本说明**：V4.1 在 V4 基础上修正了 astro.config 图片配置写法、补全 vercel.json 构建指令、新增产品列表页实现方案、清理 MDX 示例中的冗余 import。V4 核心架构不变——Astro 静态编译 + Cloudflare 全球加速 + Vercel 托管 + 搬瓦工后台 + Hermes 运维中枢。**面向对象：网络小白**——每步有解释，每行命令有说明。

---

## 先搞清楚几个核心概念（小白专区）

在往下看之前，先花 2 分钟理解几个关键名词，后面全部会用到：

| 名词 | 一句话解释 | 相当于... |
|------|-----------|----------|
| **域名** | 你的网站地址，比如 `zaulux.com` | 你家的门牌号 |
| **DNS** | 把域名翻译成服务器 IP 的系统 | 电话本，查"老张"→找到号码 |
| **CDN** | 全球各地缓存你网站内容的服务器网络 | 全国连锁便利店，就近取货 |
| **Vercel** | 免费托管前端网页的服务 | 免费帮你把网页挂上网 |
| **Cloudflare** | 全球网络加速 + 安全防护 | 你家门口的保安 + 快递驿站 |
| **Astro** | 一种做网站的工具，输出纯 HTML | 把原料加工成成品，送出去就不管了 |
| **搬瓦工** | 一台在美国的远程电脑（VPS） | 你在美国租的一台电脑 |
| **Hermes** | 运行在你电脑上的 AI 管家 | 你的 24 小时在线助理 |
| **Git** | 代码版本管理工具 | Word 的"修订记录"，但更强大 |
| **SSH** | 安全远程登录服务器的方式 | 加密的对讲机，只有你能用 |

---

## 整体架构：一张图看懂

```
                        zaulux.com 完整架构
 ┌──────────────────────────────────────────────────────────────┐
 │                                                              │
 │  ① 阿里云              ② Cloudflare              ③ Vercel   │
 │  ┌──────────┐   托管   ┌──────────────┐   托管   ┌────────┐ │
 │  │ 域名注册  │────────→│ DNS + CDN    │────────→│ Astro   │ │
 │  │ 续费/实名 │        │ + 安全防护   │         │ 静态网站 │ │
 │  └──────────┘        └──────────────┘        └────────┘ │
 │                              │                              │
 │                    全球 300+ 边缘节点                        │
 │                    北美客户秒开访问                           │
 │                                                              │
 │  ④ 搬瓦工 VPS（可选·后期再加）   ⑤ 本地电脑                  │
 │  ┌──────────────┐               ┌──────────────┐            │
 │  │ AI 后台算力  │←──SSH 低延迟──│ Hermes Agent │            │
 │  │ 图片批量处理 │     (可选)     │ 全站管理中控 │            │
 │  └──────────────┘               └──────────────┘            │
 │                                                              │
 └──────────────────────────────────────────────────────────────┘

  数据流向：
  🌐 客户访问 → Cloudflare 就近节点 → Vercel 返回 HTML → 秒开
  🔧 运维管理 → Hermes → 搬瓦工/Cloudflare/Vercel → 全自动
  📦 素材流转 → 搬瓦工处理 → Cloudflare R2 存储 → CDN 分发
```

**关键设计原则——三个"不"：**

1. **北美客户不碰搬瓦工**：所有网页和图片走 Cloudflare + Vercel 北美节点
2. **网站没有后台可攻击**：Astro 编译成纯 HTML，没有 PHP，没有数据库，没有登录页
3. **你不需要懂技术**：Hermes AI 管家帮你搞定一切，你只负责告诉它要做什么

---

## 为什么选 Astro 而不是 WordPress/Joomla/Next.js？

### 安全性对比——这是选 Astro 最核心的原因

| 网站类型 | 攻击面 | 举例 |
|----------|--------|------|
| **WordPress / Joomla** | PHP 运行时 + 数据库 + 插件 + 后台登录页 | 你刚经历过的：uploadCustomIcon 漏洞、后台爆破 |
| **Next.js** | API Routes + Serverless 函数 + Node.js 运行时 | API 接口被打、SSR 服务被刷 |
| **Astro** | **无** | 构建完只剩 .html 文件，没有可攻击的东西 |

```
Joomla/WordPress:   攻击者 → PHP漏洞 → 数据库 → 网站沦陷
Next.js:            攻击者 → API接口 → Serverless → 数据泄露
Astro:              攻击者 → index.html → ？→ 放弃（没什么可攻击的）
```

### 你的 B2B 焊接设备站为什么适合 Astro

你的网站内容是什么？产品参数、设备图片、公司介绍、联系表单。这些东西：

- **不需要 PHP 运行时**——产品参数不会每秒变化
- **不需要数据库**——焊接设备型号不会实时更新
- **不需要后台登录**——你可以直接让 AI 帮你改内容

Astro 在**构建时**就把所有页面编译成 HTML 文件，就像把一本书提前印好。客户访问时直接拿到成品，不需要现场"烹饪"。快、安全、省心。

---

## 第一阶段：准备工作（需要你做的，大约 30 分钟）

### 1.1 注册需要的账号

你需要注册以下三个账号（都免费）：

| 平台 | 用途 | 注册地址 | 需要什么 |
|------|------|----------|----------|
| **GitHub** | 存放网站代码 | github.com | 邮箱即可 |
| **Vercel** | 免费托管网站 | vercel.com | 用 GitHub 账号直接登录 |
| **Cloudflare** | DNS + CDN + 安全 | cloudflare.com | 邮箱即可 |

> 💡 **小白提示**：Vercel 和 Cloudflare 都有免费套餐，完全够一个外贸 B2B 站使用。Vercel 免费版每月 100GB 流量，Cloudflare CDN 免费无限流量。

### 1.2 阿里云域名准备

你已经有 `zaulux.com` 域名在阿里云，接下来只需要改一个设置——**把 DNS 解析权交给 Cloudflare**。

为什么要交给 Cloudflare？因为：
- Cloudflare 有全球 300+ 节点，北美客户秒开
- 免费防 DDoS 攻击
- 自动 SSL 证书（https 那个小锁）

具体操作（后面阶段会详细讲）：
1. 登录 Cloudflare，添加 `zaulux.com`
2. Cloudflare 会给你 2 个 NS 地址
3. 去阿里云域名控制台，把 DNS 服务器改成这 2 个 NS 地址
4. 等 1-24 小时生效

### 1.3 本地电脑安装工具（一次性，我来帮你）

你的 Hermes Agent 已经装好了，还需要装两个命令行工具：

```bash
# 安装 Git（版本管理工具）
# 下载地址：https://git-scm.com/download/win
# 一路点"下一步"即可

# 安装 Node.js（Astro 运行环境）
# 下载地址：https://nodejs.org（选 LTS 版本）
# 一路点"下一步"即可
```

---

## 第二阶段：创建 Astro 网站项目（我来帮你做）

### 2.1 什么是 Astro 项目

Astro 项目的文件夹结构就像这样：

```
zaulux-site/                  ← 项目根目录
├── src/
│   ├── pages/                ← 每个文件 = 网站上一个页面
│   │   ├── index.astro       ← 首页
│   │   ├── products/         ← 产品页面
│   │   │   └── [slug].astro  ← 产品详情（动态路由）
│   │   ├── about.astro       ← 关于我们
│   │   └── contact.astro     ← 联系我们
│   ├── components/           ← 可复用的"零件"
│   │   ├── Header.astro      ← 导航栏
│   │   ├── Footer.astro      ← 页脚
│   │   └── ProductCard.astro ← 产品卡片
│   ├── content/              ← AI 可以直接写的内容（MDX）
│   │   └── products/         ← 每篇 .mdx 文件 = 一篇产品介绍
│   └── styles/               ← 样式文件
├── public/                   ← 图片、PDF、字体等静态文件
│   ├── images/
│   └── favicon.ico
├── astro.config.mjs          ← Astro 配置文件
├── package.json              ← 项目依赖列表
└── tsconfig.json             ← TypeScript 配置
```

> 💡 **小白理解**：`src/pages/` 里的每个 `.astro` 文件，最终会变成网站上的一个 `.html` 页面。比如 `src/pages/about.astro` → 编译后 → `https://zaulux.com/about/`

### 2.2 AI 内容管理——Astro 最大的优势

这是 V4 相比 V3 最大的升级。你的产品内容可以放在 `src/content/products/` 目录下，用 **MDX** 格式写：

```markdown
---
# 这是"元数据"区（AI 和搜索引擎会读）
title: "Welding Positioner WP1"
category: "焊接变位机"
capacity: "1 Ton"
tiltingAngle: "0-90°"
image: "/images/products/wp1-main.jpg"
date: 2026-07-07
---

# Welding Positioner WP1

## 产品概述
WP1 型焊接变位机适用于管道和罐体焊接...

## 技术参数
| 参数 | 数值 |
|------|------|
| 承载能力 | 1 吨 |
| 翻转角度 | 0-90° |
| 旋转速度 | 0.1-2 rpm |

## 产品图片
![WP1 正面](https://cdn.zaulux.com/images/wp1-front.jpg)
![WP1 工作场景](https://cdn.zaulux.com/images/wp1-working.jpg)
```

> 💡 **小白提示**：注意 MDX 文件里直接写 `<img>` 或 `![alt](url)` 就行，不需要 import 任何东西——Astro 的 MDX 原生支持 Markdown 和 HTML 混写。

**这个格式的好处：**
- 🤖 **AI 可以直接写**：你告诉 AI "写一篇 WP1 变位机的产品介绍"，AI 直接生成这个文件
- 🔍 **搜索引擎友好**：元数据区的内容自动变成页面的 SEO 标签
- 📱 **自动生成页面**：Astro 读取这个文件，自动生成产品详情页 HTML
- ✏️ **修改超简单**：改文字、改参数、加图片，改完 git push，自动上线

### 2.4 产品列表页——所有产品的"目录"

你已经有 64 篇 MDX 在 `src/content/products/` 里，还需要一个**总览页面**让客户浏览所有产品。Astro 用 `Astro.glob()` 一行代码搞定：

**创建 `src/pages/products/index.astro`**：

```astro
---
// 读取 content/products/ 下所有 .mdx 文件
const products = await Astro.glob('../content/products/*.mdx');

// 按分类分组
const categories = {};
for (const p of products) {
  const cat = p.frontmatter.category || 'Other';
  if (!categories[cat]) categories[cat] = [];
  categories[cat].push(p);
}
---

<Layout title="Products - ZAULUX">
  <h1>Welding Equipment Products</h1>

  <!-- 按分类展示 -->
  {Object.entries(categories).map(([cat, items]) => (
    <section>
      <h2>{cat}</h2>
      <div class="product-grid">
        {items.map((p) => (
          <a href={`/products/${p.frontmatter.slug || ''}`} class="product-card">
            {p.frontmatter.images?.[0] && (
              <img
                src={p.frontmatter.images[0].url}
                alt={p.frontmatter.images[0].alt}
                loading="lazy"
              />
            )}
            <h3>{p.frontmatter.title}</h3>
            <p>{p.frontmatter.description?.slice(0, 80)}...</p>
          </a>
        ))}
      </div>
    </section>
  ))}
</Layout>
```

> 💡 **效果**：访问 `https://zaulux.com/products/`，自动展示所有 64 个产品，按分类（positioner、turning rolls、robot...）分组，每个产品显示第一张图和简介。

**产品详情页 `src/pages/products/[slug].astro`**：

```astro
---
// 根据 URL 中的 slug 找到对应的 MDX
export async function getStaticPaths() {
  const products = await Astro.glob('../content/products/*.mdx');
  return products.map((p) => ({
    params: { slug: p.frontmatter.slug },
    props: { product: p },
  }));
}

const { product } = Astro.props;
const { frontmatter } = product;
---

<Layout title={`${frontmatter.title} - ZAULUX`}>
  <article>
    <h1>{frontmatter.title}</h1>
    <p class="meta">
      Category: {frontmatter.category} | Published: {frontmatter.publishDate}
    </p>

    <!-- 图库 -->
    <div class="gallery">
      {frontmatter.images?.map((img) => (
        <figure>
          <img src={img.url} alt={img.alt} loading="lazy" />
          <figcaption>{img.alt}</figcaption>
        </figure>
      ))}
    </div>

    <!-- MDX 正文 -->
    <product.Content />
  </article>
</Layout>
```

> 💡 **两条路由就搞定了**：
> - `src/pages/products/index.astro` → 产品列表页（自动读取所有 MDX）
> - `src/pages/products/[slug].astro` → 产品详情页（根据 URL 匹配对应 MDX）
> 
> 新增一个产品：往 `content/products/` 丢一个 `.mdx` 文件 → 自动出现在列表页 + 自动有独立详情页。**零数据库、零配置。**

### 2.5 联系表单——唯一的"动态"功能

你的网站只有联系表单需要"动态"——访客填完信息，需要发给你。Astro 的做法：

```
访客填表 → 前端 JS 收集数据 → 发送到第三方表单服务 → 你收到邮件
```

不需要自己写后端！用免费服务：
- **Web3Forms**（免费 250 次/月）——最简单
- **Formspree**（免费 50 次/月）
- **Google Forms**（完全免费，无限次）

```html
<!-- 在 Astro 页面中，几行代码搞定 -->
<form action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="你的密钥">
  <input type="text" name="name" placeholder="Your Name" required>
  <input type="email" name="email" placeholder="Your Email" required>
  <textarea name="message" placeholder="Your Message"></textarea>
  <button type="submit">Send Inquiry</button>
</form>
```

> ⚠️ **防垃圾邮件必做**：企业站表单是垃圾邮件的重灾区。如果不用验证码，你的邮箱一天能收几百条博彩、色情广告。

**最简单的防护——加一个隐形"蜜罐"字段**（机器人会自动填，真人看不见）：

```html
<form action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="你的密钥">

  <!-- 🤖 蜜罐：机器人会填这个，真人看不到 -->
  <input type="text" name="bot-field" style="display:none" tabindex="-1" autocomplete="off">

  <input type="text" name="name" placeholder="Your Name" required>
  <input type="email" name="email" placeholder="Your Email" required>
  <textarea name="message" placeholder="Your Message"></textarea>
  <button type="submit">Send Inquiry</button>
</form>
```

**更强的防护——加 Cloudflare Turnstile**（免费，不需要点"我不是机器人"，自动判断）：

1. 登录 Cloudflare → Turnstile → 添加站点
2. 获取 site key 和 secret key
3. 表单里加几行：

```html
<!-- 放在 <form> 里面，提交按钮前面 -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<div class="cf-turnstile" data-sitekey="你的site-key"></div>
```

> 💡 **小白提示**：先上蜜罐就够了（0 成本，1 行代码）。垃圾邮件实在多了再加 Turnstile。

### 2.6 图片管理——Astro 没有"媒体库"，换图需要重新部署

> ⚠️ **实际痛点**：WordPress/Joomla 有后台媒体库，上传替换图片，网站自动更新。Astro 是纯静态——换图需要改文件 → Git 提交 → Vercel 重新构建（约 1 分钟）。虽然不算慢，但习惯 CMS 的人需要适应。

**三种方案，从简单到高级：**

| 方案 | 适合谁 | 操作方式 |
|------|--------|----------|
| **A：Git 直接管图片**（推荐新手） | 图片不频繁变 | 把新图放 `public/images/`，`git push`，自动部署 |
| **B：Cloudflare R2 + CDN**（推荐中期） | 图片较多，偶尔更新 | 图片上传 R2 存储桶，网站通过 CDN 链接引用，换图不用重新部署 |
| **C：Cloudinary / Contentful**（给钱省心） | 图片超多，天天换 | 专业"无头 CMS"管图片，Astro 只调取链接，有免费套餐 |

> 💡 **起步建议**：先用方案 A，图片和新图片改名不同（`wp1-v1.jpg` → `wp1-v2.jpg`），MDX 里改引用路径。2 分钟搞定。等图片超过 300 张再考虑方案 B。

---

## 第三阶段：完整部署流程（从 0 到上线）

### 3.1 步骤一：Cloudflare 接管域名解析

**目标**：让 Cloudflare 管理你的域名 DNS

1. 登录 [Cloudflare](https://dash.cloudflare.com)，点「添加站点」
2. 输入 `zaulux.com`，选 Free 套餐
3. Cloudflare 会扫描你现有的 DNS 记录，自动导入
4. 完成后，Cloudflare 给你 2 个**域名服务器（NS）地址**，类似：
   ```
   elsa.ns.cloudflare.com
   guy.ns.cloudflare.com
   ```
5. 登录阿里云 → 域名控制台 → 找到 `zaulux.com` → DNS 修改 → 把上面的 2 个地址填进去

> 💡 **小白提示**：这一步改完后，全世界的 DNS 服务器需要 1-24 小时才能全部更新。期间网站访问不受影响（Cloudflare 会自动同步你原来的解析记录）。

### 3.2 步骤二：Cloudflare DNS 记录配置

等 NS 生效后（Cloudflare 面板显示 Active），添加以下记录：

| 类型 | 名称 | 目标 | 代理状态 |
|------|------|------|----------|
| CNAME | `www` | `zaulux.vercel.app` | 🟠 橙色（开启代理） |
| CNAME | `@` | `zaulux.vercel.app` | 🟠 橙色（开启代理） |
| CNAME | `cdn` | `你的R2存储桶域名` | 🟠 橙色 |

> 💡 **小白提示**：橙色代理 = Cloudflare 帮你隐藏真实服务器地址 + 开启 CDN 加速。**一定要橙色！** 灰色等于裸奔。

### 3.3 步骤三：GitHub 创建代码仓库

```bash
# 在你的电脑上（我来帮你执行）
mkdir D:/AI/zaulux-astro-site
cd D:/AI/zaulux-astro-site

# 初始化 Git
git init
git branch -M main

# 创建 .gitignore（告诉 Git 哪些文件不上传）
echo "node_modules/
.env
dist/
.astro/" > .gitignore
```

然后在 GitHub 网站创建新仓库 `zaulux-site`，关联本地：

```bash
git remote add origin https://github.com/你的用户名/zaulux-site.git
```

### 3.4 步骤四：创建 Astro 项目并配置

```bash
# 创建 Astro 项目（选默认模板即可）
# 在 zaulux-astro-site 目录下执行
npm create astro@latest . -- --template basics

# 安装必要的依赖
npm install @astrojs/mdx @astrojs/sitemap

# 安装 Tailwind CSS（现代化样式框架）
npx astro add tailwind
```

**修改 `astro.config.mjs`**：

```javascript
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.zaulux.com',
  integrations: [
    mdx(),
    tailwind(),
    sitemap({
      // 自动生成 sitemap.xml
      changefreq: 'weekly',
      priority: 0.7,
    }),
  ],
  // 图片优化（自动转 WebP/AVIF）
  image: {
    service: { entrypoint: 'astro/assets/services/sharp' },
  },
  // 国际化和 SEO
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh', 'es'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
});
```

### 3.5 步骤五：Vercel 连接并部署

1. 登录 [Vercel](https://vercel.com)，点「New Project」
2. 选择你的 GitHub 仓库 `zaulux-site`
3. Vercel 自动识别这是 Astro 项目，无需手动配置
4. 在 Build Settings 确认：
   - Framework Preset: **Astro**
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. 点 Deploy，等待 1-2 分钟

部署完成后，Vercel 会给你一个临时域名，比如 `zaulux-site-abc123.vercel.app`。

### 3.6 步骤六：绑定自定义域名

1. Vercel 项目 → Settings → Domains
2. 添加 `www.zaulux.com`
3. Vercel 会提示你去 Cloudflare 添加 DNS 记录
4. 回到 Cloudflare，确认之前添加的 CNAME 记录指向 Vercel 给的地址
5. 等待 SSL 证书自动签发（约 1-2 分钟）

现在访问 `https://www.zaulux.com`，你的 Astro 网站就上线了！

### 3.7 步骤七：配置安全响应头

在项目根目录创建 `vercel.json`：

```json
{
  "buildCommand": "astro build",
  "outputDirectory": "dist",
  "framework": "astro",
  "installCommand": "npm install",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Permissions-Policy",
          "value": "camera=(), microphone=(), geolocation=()"
        },
        {
          "key": "Strict-Transport-Security",
          "value": "max-age=31536000; includeSubDomains; preload"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/admin",
      "destination": "/404",
      "permanent": false
    },
    {
      "source": "/administrator",
      "destination": "/404",
      "permanent": false
    },
    {
      "source": "/wp-admin",
      "destination": "/404",
      "permanent": false
    },
    {
      "source": "/phpmyadmin",
      "destination": "/404",
      "permanent": false
    },
    {
      "source": "/.env",
      "destination": "/404",
      "permanent": false
    },
    {
      "source": "/.git",
      "destination": "/404",
      "permanent": false
    },
    {
      "source": "/xmlrpc.php",
      "destination": "/404",
      "permanent": false
    }
  ]
}
```

> 💡 **小白提示**：这些配置干什么？
> - **安全头**：告诉浏览器不要执行奇怪的操作（防 XSS 攻击）
> - **重定向**：把 `/admin`、`/wp-admin` 等常见攻击路径导向 404 页面。因为这些路径在 Astro 中根本不存在——但攻击者不知道，他们会疯狂扫描这些路径。直接返回 404，让他们扫个寂寞。

### 3.8 步骤八：Cloudflare 安全开满

在 Cloudflare 面板做以下设置：

**SSL/TLS 设置：**
- SSL/TLS 加密模式：**Full (Strict)**← 一定要 Strict
- 开启「Always Use HTTPS」
- 开启「Automatic HTTPS Rewrites」

**安全设置：**
- 安全级别：**Medium**
- Challenge Passage：**30 分钟**
- Browser Integrity Check：**开启**

**防火墙规则（WAF）：**添加一条规则：
```
字段：URI Path   运算符：包含   值：/wp-admin
字段：URI Path   运算符：包含   值：/administrator
字段：URI Path   运算符：包含   值：/phpmyadmin
动作：阻止
```

> 💡 **小白提示**：就算 Astro 没有这些路径，提前在 Cloudflare 层面拦截，相当于在大门口就把小偷拦住，根本不让他走到你店门口。

---

## 第四阶段：搬瓦工 VPS 配置（可选 —— 前期可以先不部署）

> ⚠️ **重要提醒**：搬瓦工 VPS 在 V4 架构中属于**锦上添花，不是必需品**。
> 
> **为什么可以先跳过？**
> - Astro 在构建时已经用 sharp 自动压缩图片，不需要服务器再压一次
> - GitHub 免费保存所有代码历史版本，是最好的备份
> - Hermes 在你本地电脑可以直接 `curl` 监控网站可用性
> - 多一台 VPS = 多一个需要维护的系统 = 多一个潜在故障点
> 
> **什么时候才需要？** 等你网站做大了，需要 24 小时从海外 IP 检测访问速度、或者批量跑 AI 任务不想占用自己电脑的时候再加。
> 
> **如果你决定部署，以下是配置指南。否则直接跳到第五阶段。**

### 4.1 买什么配置

搬瓦工 DC6 CN2 GIA-E 套餐，**仅用于你国内电脑远程操控**，北美客户不会访问它。

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| CPU | 2 核 | 够图片批处理 |
| 内存 | 2 GB | 够跑脚本 |
| 硬盘 | 40 GB SSD | 存放原始素材 + 备份 |
| 带宽 | 1 Gbps | CN2 GIA 回国专线 |
| 流量 | 1000 GB/月 | 完全够用 |

### 4.2 初始化设置（一次性）

```bash
# ====== 搬瓦工 VPS 初始设置 ======
# （这些命令由 Hermes 通过 SSH 远程执行）

# 1. 更新系统
yum update -y

# 2. 安装必要工具
yum install -y imagemagick webp-tools git curl wget

# 3. 创建素材目录
mkdir -p /www/zaulux-assets/{images,backup,logs}

# 4. 安装 rclone（用于备份到 Cloudflare R2）
curl https://rclone.org/install.sh | bash

# 5. 配置 SSH 安全
# 禁用密码登录，只允许密钥
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart sshd

# 6. 安装 fail2ban（防暴力破解）
yum install -y epel-release fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

### 4.3 日常任务配置

搬瓦工负责三件事：

**① 每日图片批处理（Cron 每日 02:00）**
```bash
#!/bin/bash
# 功能：压缩原图 + 转 WebP
IMAGE_DIR="/www/zaulux-assets/images"
BAK_DIR="/www/zaulux-assets/backup/$(date +%Y%m%d)"

mkdir -p "$BAK_DIR"

# 备份原图
cp -r "$IMAGE_DIR"/* "$BAK_DIR/"

# 图片压缩（保留画质 85%）
find "$IMAGE_DIR" -name "*.jpg" -o -name "*.png" | while read f; do
  convert "$f" -quality 85 -strip "$f"
done

# 转换 WebP 格式
find "$IMAGE_DIR" -name "*.jpg" -o -name "*.png" | while read f; do
  cwebp -q 85 "$f" -o "${f%.*}.webp"
done

# 清理 30 天前备份
find /www/zaulux-assets/backup/ -type d -mtime +30 -exec rm -rf {} +

echo "✅ $(date): 素材处理完成"
```

**② 每日冷备同步到 R2（Cron 每日 04:00）**
```bash
#!/bin/bash
# 功能：备份同步到 Cloudflare R2
rclone sync /www/zaulux-assets/backup/ r2-cold:zaulux-cold-backup \
  --progress --transfers 8 --log-file=/www/zaulux-assets/logs/rclone.log

# 清理 R2 上 90 天前的文件
rclone delete r2-cold:zaulux-cold-backup --min-age 90d
```

**③ 健康自检（Cron 每 5 分钟）**
```bash
#!/bin/bash
# 检查 CPU/内存/磁盘，超标告警
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d. -f1)
MEM=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
DISK=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

if [ "$CPU" -gt 80 ] || [ "$MEM" -gt 90 ] || [ "$DISK" -gt 85 ]; then
  # 发送告警
  curl -X POST "$ALERT_WEBHOOK" -d "{\"text\":\"⚠️ VPS资源告警: CPU=${CPU}% MEM=${MEM}% DISK=${DISK}%\"}"
fi
```

---

## 第五阶段：本地 Hermes 统一管理中枢

### 5.1 Hermes 管什么

```
本地 Hermes Agent
├── 🌐 前端管理：Git 提交 + Vercel 部署 + Cloudflare 缓存刷新
├── 🔧 后台运维：SSH 远程搬瓦工 → 图片处理/备份/巡检
├── 🤖 AI 内容：修改 MDX 文件 → Git 推送 → 自动上线
├── 📊 监控告警：三分钟全网巡检 → 异常自动修复 → Telegram 通知
└── 🔑 安全管理：密钥轮换提醒 + 季度安全审计
```

### 5.2 Hermes 日常工作流

**场景一：新增一个产品页面**

你：「Hermes，帮我创建一个新的产品页面，焊接操作机 WM12，参数是...」

Hermes：
1. 在 `src/content/products/wm12.mdx` 创建 MDX 文件
2. 填充产品参数、描述、图片引用
3. Git 提交 + 推送
4. Vercel 自动部署（约 1 分钟）
5. Cloudflare 缓存自动刷新
6. 报告：「✅ WM12 产品页上线，地址：https://www.zaulux.com/products/wm12」

**场景二：修改产品价格**

你：「把 WP1 变位机的价格改成 $2,500」

Hermes：
1. 找到 `src/content/products/wp1.mdx`
2. 修改价格字段
3. Git 提交推送
4. 自动部署上线

**场景三：网站挂了**

Hermes 每 5 分钟自检，发现 `www.zaulux.com` 返回非 200：
1. 立即 Telegram 通知你
2. 检查 Vercel 部署状态
3. 如果是部署问题 → 自动回退上一个版本
4. 报告：「🚨 站点异常已自动修复，回退至部署 #1234」

---

## 第六阶段：安全体系（V4 专属）

### 6.1 Astro 的"零攻击面"架构

```
传统 CMS 攻击链：
  攻击者 → 扫后台路径 → 爆破密码 → 上传木马 → 控制服务器 → 窃取数据

Astro 攻击链：
  攻击者 → 扫后台路径 → 404（根本没有后台！）
  攻击者 → 尝试 SQL 注入 → 没有数据库可注入
  攻击者 → 尝试 PHP 漏洞 → 没有 PHP 运行时
  攻击者 → 扫描插件漏洞 → 没有插件系统
  攻击者 → ... → 放弃
```

### 6.2 多层防护体系

| 层级 | 防护手段 | 作用 |
|------|----------|------|
| 第一层：Cloudflare | DDoS 防护 + WAF + 隐藏源站 IP | 攻击流量还没到你网站就被拦截 |
| 第二层：Vercel | 自动 HTTPS + 安全响应头 | 浏览器级安全防护 |
| 第三层：Astro | 纯静态 HTML，无运行时 | 没有任何可攻击的代码 |
| 第四层：Git 版本控制 | 每次修改有记录，可随时回退 | 被篡改也能一键恢复 |
| 第五层：Hermes | 实时监控 + 自动修复 | 出问题 2 分钟内自动修复 |

### 6.3 备份策略（3-2-1，无需 VPS）

```
3 份数据副本
├── ① 本地电脑 `D:\AI\output\`（原始素材）
├── ② GitHub 代码仓库（所有 MDX + 配置 + 代码历史）
└── ③ Cloudflare R2 冷备（可选，等部署搬瓦工后再加）

2 种存储介质
├── 本地硬盘（快速恢复）
└── Git 云端（免费无限版本历史）

1 份异地备份
└── GitHub 服务器在全球多个数据中心
```

> 💡 **不部署搬瓦工也完全够用**：GitHub 保存你的每行代码、每张图片、每次修改记录，随时可以回退到任意历史版本。这比你原来 Joomla 服务器上的备份更可靠。

### 6.4 安全巡检清单

Hermes 每季度自动执行的检查项：

| 检查项 | 频率 | 不正常怎么办 |
|--------|------|-------------|
| SSL 证书到期 | 每日 | 到期前 30 天开始提醒 |
| 域名续费 | 每月 | 到期前 60 天提醒 |
| API 密钥轮换 | 90 天 | 提前 14 天提醒创建新密钥 |
| 备份完整性 | 每日 | 不一致立即告警 |
| 依赖漏洞 | 每月 | `npm audit` 自动检查 |
| 网站可用性 | 每 5 分钟 | 异常自动回退 |

---

## 第七阶段：SEO 优化清单

### 7.1 Astro 自动处理的 SEO

- ✅ **sitemap.xml** 自动生成（`@astrojs/sitemap`）
- ✅ **图片自动优化**（WebP/AVIF 自动转换）
- ✅ **纯 HTML 输出**（搜索引擎最爱，100% 可索引）
- ✅ **零 JavaScript 首屏**（Google 排名加分）

### 7.2 robots.txt —— 告诉搜索引擎什么能抓

在 `public/robots.txt` 创建（Astro 项目根目录的 public 文件夹）：

```txt
User-agent: *
Allow: /
Disallow: /cdn-cgi/

Sitemap: https://www.zaulux.com/sitemap-index.xml
```

> 💡 **小白提示**：`robots.txt` 是搜索引擎来看网站时第一个读的文件，相当于你家的"导览手册"。`Allow: /` 表示"随便看"，`Disallow` 列出不让看的（比如 Cloudflare 内部路径）。

### 7.3 404 页面——客户迷路时的"救命稻草"

Astro 自带 404 页面但很简陋。在 `src/pages/404.astro` 写一个友好的：

```astro
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="Page Not Found - ZAULUX">
  <main style="text-align:center;padding:80px 20px">
    <h1 style="font-size:4em;color:#1976d2;margin:0">404</h1>
    <p style="font-size:1.3em;color:#666;margin:20px 0">
      Sorry, this page doesn't exist.
    </p>
    <p style="color:#999">
      The page may have been moved or the URL is incorrect.
    </p>
    <a href="/"
       style="display:inline-block;margin-top:30px;padding:12px 32px;
              background:#1976d2;color:white;text-decoration:none;
              border-radius:6px;font-size:1.1em">
      ← Back to Home
    </a>
  </main>
</Layout>
```

> 💡 **效果**：客户输入错误的 URL → 看到一个友好页面 + 大大的"返回首页"按钮，而不是白屏报错。

### 7.4 SEO 元数据模板（给 AI 用的提示词）

以后让 AI 帮你写产品 MDX 时，直接把这段话粘贴给 AI：

```
请帮我写一篇关于 [产品名] 的产品介绍，格式必须是 Astro MDX。

Frontmatter 区域必须包含以下字段：
- title: 产品标题（英文，包含品牌+型号+核心参数，60字以内）
- description: 产品描述（英文，用于 Google 搜索结果摘要，150字以内）
- category: 产品分类（英文，从 positioner/turning rolls/robot/h beam/automation/boom&column/welding manipulator/beveling 中选择）
- publishDate: 发布日期（格式 YYYY-MM-DD）
- slug: URL 友好名称（英文，小写，用连字符分隔）
- images: 图片列表，每张包含 url 和 alt
- keywords: 关键词数组，5-8 个

正文部分使用 Markdown 语法，结构如下：
1. 产品概述（一段话）
2. 技术参数（用表格）
3. 产品特点（用无序列表）
4. 应用场景
5. 可选配件

图片用 ![alt](url) 格式引用，url 以 /images/ 开头。
```

完成后再补充这几个词：`robots.txt`, `404`, `提示词模板`。

### 7.5 你需要手动做的

每个产品 MDX 文件的元数据区，确保填写完整：

```markdown
---
title: "Welding Positioner WP1 - 1 Ton Pipe Welding Positioner"
description: "Professional 1-ton welding positioner for pipe and tank welding. 0-90° tilting angle, CE certified. Factory direct price."
image: "https://cdn.zaulux.com/images/wp1-og.jpg"
publishDate: 2026-07-07
keywords:
  - welding positioner
  - pipe welding positioner
  - 1 ton positioner
---
```

> 💡 **小白提示**：`title` 和 `description` 是 Google 搜索结果里显示的内容，写得好坏直接影响点击率。

---

## 第八阶段：成本估算（全部加起来多少钱）

| 项目 | 服务商 | 费用 | 说明 |
|------|--------|------|------|
| 域名 | 阿里云 | ~¥60/年 | zaulux.com 续费 |
| 网站托管 | Vercel | **免费** | 100GB 流量/月，B2B 站够用 |
| CDN + DNS + 安全 | Cloudflare | **免费** | 无限流量，DDoS 防护 |
| 后台 VPS | 搬瓦工 | ~$49/年 | **可选**，等做大了再部署 |
| 代码托管 | GitHub | **免费** | 无限私有仓库 |
| 表单服务 | Web3Forms | **免费** | 250 次/月 |
| AI 运维 | Hermes + Claude | ~$20/月 | AI 管家 + 代码助手 |
| **总计（不含 VPS）** | | **约 ¥300/年** | 每天不到 1 元 |
| **总计（含 VPS）** | | **约 ¥500/年** | 每天不到 1.5 元 |

> 对比：原来的 Joomla 服务器一个月要几百块，还天天被攻击。新方案一年不到 500，还不用担心安全问题。

---

## V4 相对 V3 的核心改进总结

| 改进点 | V3（Next.js） | V4（Astro） | 效果 |
|--------|-------------|------------|------|
| 🔒 攻击面 | 有 API Routes / Serverless | **零运行时**，纯 HTML | 安全等级从 C → A+ |
| ⚡ 页面速度 | React 运行时 ~40KB JS | **0 KB JS 默认** | 首屏加载快 3-5 倍 |
| 🤖 AI 写内容 | JSX 组件，门槛高 | **MDX 文件**，AI 直接生成 | 内容更新效率 10x |
| 🧩 复杂度 | SSR/CSR/ISR 多模式 | **只有 SSG**，一种模式 | 出问题概率降 90% |
| 📦 打包体积 | ~200KB+ React 运行时 | **~5KB**（仅必要 CSS） | 移动端体验大幅提升 |
| 💰 成本 | 一样 | 一样 | 没变化 |
| 🏗️ 架构 | CF + Vercel + BW + Hermes | **完全一致** | 沿用 V3 全部架构 |

---

> **文档版本**：V4.1
> **变更记录**：
> - V4.1：搬瓦工标记为可选、新增图片管理方案、表单防垃圾（蜜罐+Turnstile）、robots.txt+404 页面、AI 提示词模板、成本分两档
> - V4.0：基于 V3 架构，Next.js → Astro 全面重构，新增 AI MDX 内容工作流  
> **面向对象**：网络小白  
> **前置知识要求**：会用浏览器、知道什么是域名  
> **预计总部署时间**：2-3 小时（含等待 DNS 生效）  
> **维护时间**：零（全自动）  
> **安全等级**：A+（无运行时 = 无攻击面）  

---

## 附：V4 快速启动清单

- [ ] 注册 GitHub 账号
- [ ] 注册 Vercel 账号（用 GitHub 登录）
- [ ] 注册 Cloudflare 账号
- [ ] 阿里云域名 NS 改为 Cloudflare
- [ ] Cloudflare DNS 配好 CNAME 指向 Vercel
- [ ] 创建 Astro 项目
- [ ] 配置 astro.config.mjs
- [ ] 编写首页 + 产品 MDX 文件
- [ ] Git 推送 → Vercel 自动部署
- [ ] Cloudflare 安全设置（SSL Strict + WAF 规则）
- [ ] 搬瓦工 VPS 初始化（可选，不着急）
- [ ] Hermes 配置监控脚本
- [ ] 域名绑定，正式上线 🎉
