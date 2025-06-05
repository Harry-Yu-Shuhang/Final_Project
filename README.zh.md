# QF623 ETF 投资组合管理项目

本项目实现了一个 ETF 策略，目标是在满足最小波动率约束的前提下，**最大化夏普比率（Sharpe Ratio）**，并使用 Yahoo Finance 数据进行回测与归因分析。

---

## 🎯 项目目标

- 构建 ETF 投资池（排除杠杆/反向 ETF）
- 利用 **趋势跟随策略** 生成 alpha 信号
- 构建组合（long-only 或 long-short），需满足：
  - 年化风险 ≥ 3%
  - 权重绝对值和 ≤ 1（即 ∑|w| ≤ 1）
- 模拟 **T+1 调仓执行**
- 输出指标并解释 **风险因子暴露**

---

## ⚙️ 原理说明

### 1. ETF Universe 构建
- 过滤关键词如 `3x`、`ultra`、`inverse`，排除杠杆产品
- 排除日均成交量过低的 ETF

### 2. Alpha 信号：趋势跟随
- 使用短期（20天）与长期（100天）移动平均差值作为信号
- 信号为正 → 表示趋势向上，应加仓

### 3. 投资组合优化
- 优化目标：最大化夏普比率
- 约束条件：
  - 年化波动率 ≥ 3%
  - 权重绝对值之和 ≤ 1
- 使用 SLSQP 优化器

### 4. T+1 调仓机制
- 在第 T 天收盘后生成信号
- 实际调仓发生在第 T+1 天收盘
- 收益从 T+1 到 T+2 测量

### 5. 表现归因分析
- 输出：
  - 年化收益、波动率、Sharpe 比率
  - Beta 回归（可选）
  - 对冲效果评估（可选）

---

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt
# 或者使用 poetry 安装
poetry install
```

```bash
# 执行主程序
python main.py
```

---

## 📈 策略结果图

**组合累计净值（T+1 执行）：**

![累计收益](./cumulative_returns.png)

---

## 📁 项目结构

```
QF623_Final_Project/
├── config/
├── data/
├── signals/
├── portfolio/
├── execution/
├── attribution/
├── utils/
├── main.py
└── cumulative_returns.png
```

---

## 📜 开源协议

MIT License
