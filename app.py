
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(page_title="艺术品投资评估原型", layout="wide")
st.title("🎨 艺术品投资评估原型系统")

tabs = st.tabs(["📊 综合评分", "💰 财务预测", "📉 敏感性分析"])

with tabs[0]:
    st.sidebar.header("输入艺术家评分 (1-5 分)")

    categories = [
        "历史维度", "学术维度", "市场维度",
        "稀缺性系数", "代际传承溢价", "年龄-产量曲线",
        "合约结构", "价值释放路径", "道德风险防范",
        "收入潜力", "成本控制", "审美折旧率"
    ]

    scores = [st.sidebar.slider(category, 1, 5, 3) for category in categories]

    st.subheader("📋 打分总览")
    data = pd.DataFrame({"维度": categories, "评分": scores})
    st.dataframe(data, use_container_width=True)

    st.subheader("📈 视觉化评估雷达图")
    labels = categories + [categories[0]]
    scores_plot = scores + [scores[0]]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, scores_plot, linewidth=2)
    ax.fill(angles, scores_plot, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels[:-1], fontsize=10)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}"))
    ax.set_title("艺术家综合评分雷达图", fontsize=14, pad=20)
    st.pyplot(fig)

    avg_score = np.mean(scores)
    if avg_score >= 4.5:
        rating = "A+ (核心推荐)"
    elif avg_score >= 4.0:
        rating = "A (优质项目)"
    elif avg_score >= 3.0:
        rating = "B (稳健项目)"
    else:
        rating = "C (谨慎评估)"
    st.success(f"🎯 综合评分：{avg_score:.2f} → 投资评级：{rating}")

with tabs[1]:
    st.subheader("💰 财务预测模型（单位：万元）")

base_price = 30  # 万元
annual_growth = 0.12  # 12%
penetration = 0.6     # 60%
years = 5             # 5年预测期
fixed_costs = 10      # 万元
variable_cost_ratio = 0.4  # 40%
aesthetic_depreciation = -0.03  # -3%

    revenue = [(base_price * ((1 + annual_growth) ** y)) * penetration for y in range(1, years + 1)]
    costs = [(base_price * variable_cost_ratio + fixed_costs) for _ in range(years)]
    depreciated_revenue = [r * ((1 + aesthetic_depreciation) ** y) for y, r in enumerate(revenue)]
    net_profits = [r - c for r, c in zip(depreciated_revenue, costs)]

    df_finance = pd.DataFrame({
        "年份": [f"第{y}年" for y in range(1, years + 1)],
        "收入": depreciated_revenue,
        "成本": costs,
        "净收益": net_profits
    })
    st.dataframe(df_finance, use_container_width=True)

    st.subheader("📊 现金流图")
    fig2, ax2 = plt.subplots()
    ax2.bar(df_finance["年份"], df_finance["净收益"], color='green')
    ax2.axhline(0, color='gray', linestyle='--')
    ax2.set_ylabel("净收益（万元）")
    st.pyplot(fig2)

    cumulative_cashflow = np.cumsum(net_profits)
    payback_year = next((i + 1 for i, total in enumerate(cumulative_cashflow) if total >= 0), "无法回本")
    st.info(f"💡 投资回收期：{payback_year} 年")

with tabs[2]:
    st.subheader("📉 敏感性分析：年涨幅变动对收益影响")

    def simulate_growth_change(change_pct):
        return [(base_price * ((1 + annual_growth + change_pct) ** y)) * penetration for y in range(1, years + 1)]

    scenarios = {
        "+5%": simulate_growth_change(0.05),
        "基准": simulate_growth_change(0.0),
        "-5%": simulate_growth_change(-0.05),
    }

    fig3, ax3 = plt.subplots()
    for label, values in scenarios.items():
        ax3.plot(range(1, years + 1), values, label=label)
    ax3.set_xlabel("年份")
    ax3.set_ylabel("预测收入（万元）")
    ax3.set_title("不同涨幅情境下的收入预测")
    ax3.legend()
    st.pyplot(fig3)
