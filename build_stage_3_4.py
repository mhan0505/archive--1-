import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import nbformat as nbf

os.makedirs('images', exist_ok=True)
sns.set_theme(style='whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

df = pd.read_csv('winequality-red-cleaned.csv')

# ----------------- PLOT 1: Heatmap tương quan toàn diện -----------------
raw_features = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
                'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
                'pH', 'sulphates', 'alcohol', 'quality']

corr_matrix = df[raw_features].corr()

plt.figure(figsize=(12, 9))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)

sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=0.7, vmin=-0.7, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .8}, annot=True, fmt='.2f', annot_kws={"size": 9})

plt.title('Ma trận tương quan Pearson giữa 11 chỉ số hóa lý và Chất lượng rượu', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('images/correlation_heatmap_deep.png', dpi=300)
plt.close()
print("Saved correlation_heatmap_deep.png")

# ----------------- PLOT 2: Violin & Boxplot cho Alcohol & Volatile Acidity -----------------
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Alcohol
sns.violinplot(x='quality', y='alcohol', data=df, palette='Blues', inner=None, ax=axes[0], cut=0)
sns.boxplot(x='quality', y='alcohol', data=df, width=0.25, ax=axes[0], color='white',
            boxprops=dict(alpha=0.8), showcaps=True)
alc_means = df.groupby('quality')['alcohol'].mean()
axes[0].plot(range(len(alc_means)), alc_means.values, marker='o', color='crimson', linewidth=2, label='Đường giá trị TB (Mean)')
axes[0].set_title('Phân phối Nồng độ cồn (Alcohol) theo Thang điểm Chất lượng', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Điểm chất lượng (Quality Score)', fontweight='bold')
axes[0].set_ylabel('Độ cồn (% vol)', fontweight='bold')
axes[0].legend(loc='upper left')

# Volatile Acidity
sns.violinplot(x='quality', y='volatile acidity', data=df, palette='Reds_r', inner=None, ax=axes[1], cut=0)
sns.boxplot(x='quality', y='volatile acidity', data=df, width=0.25, ax=axes[1], color='white',
            boxprops=dict(alpha=0.8), showcaps=True)
va_means = df.groupby('quality')['volatile acidity'].mean()
axes[1].plot(range(len(va_means)), va_means.values, marker='s', color='navy', linewidth=2, label='Đường giá trị TB (Mean)')
axes[1].set_title('Hàm lượng Axit dễ bay hơi (Volatile Acidity) theo Chất lượng', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Điểm chất lượng (Quality Score)', fontweight='bold')
axes[1].set_ylabel('Axit axetic (g/dm3)', fontweight='bold')
axes[1].legend(loc='upper right')

plt.tight_layout()
plt.savefig('images/alcohol_volatile_acidity_distribution.png', dpi=300)
plt.close()
print("Saved alcohol_volatile_acidity_distribution.png")

# ----------------- PLOT 3: Scatter Plot & Hexbin Volatile Acidity vs Citric Acid -----------------
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    x='volatile acidity', y='citric acid',
    hue='quality_binary', palette={0: '#E53935', 1: '#2E7D32'},
    style='quality_binary', markers=['X', 'o'],
    data=df, alpha=0.75, s=60
)
plt.axvline(x=0.5, color='gray', linestyle='--', alpha=0.7, label='Ngưỡng khuyến cáo Axit bay hơi (0.5 g/dm3)')
plt.axhline(y=0.25, color='blue', linestyle=':', alpha=0.7, label='Ngưỡng tươi mát Citric Acid (0.25 g/dm3)')
plt.title('Tương quan giữa Axit dễ bay hơi (Mùi giấm) và Axit Citric (Vị tươi mát)', fontsize=13, fontweight='bold')
plt.xlabel('Axit dễ bay hơi - Volatile Acidity (g/dm3)', fontweight='bold')
plt.ylabel('Axit Citric - Citric Acid (g/dm3)', fontweight='bold')
plt.legend(labels=['Rượu ngon (>=6)', 'Rượu kém/TB (<6)', 'Ngưỡng bay hơi tối đa', 'Ngưỡng citric tối thiểu'], loc='upper right')
plt.tight_layout()
plt.savefig('images/volatile_acidity_vs_citric_scatter.png', dpi=300)
plt.close()
print("Saved volatile_acidity_vs_citric_scatter.png")

# ----------------- PLOT 4: So sánh hồ sơ hóa lý (Radar/Bar Chart Profile) -----------------
compare_cols = ['alcohol', 'sulphates', 'citric acid', 'fixed acidity', 'volatile acidity', 'total sulfur dioxide']
low_profile = df[df['quality'] <= 5][[f'{c}_scaled' for c in compare_cols]].median()
high_profile = df[df['quality'] >= 7][[f'{c}_scaled' for c in compare_cols]].median()

comparison_df = pd.DataFrame({
    'Chỉ số': compare_cols,
    'Vang phổ thông (Điểm 3-5)': low_profile.values,
    'Vang thượng hạng (Điểm 7-8)': high_profile.values
})

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(compare_cols))
width = 0.35

rects1 = ax.bar(x - width/2, comparison_df['Vang phổ thông (Điểm 3-5)'], width, label='Vang phổ thông (Điểm 3-5)', color='#EF5350')
rects2 = ax.bar(x + width/2, comparison_df['Vang thượng hạng (Điểm 7-8)'], width, label='Vang thượng hạng (Điểm 7-8)', color='#43A047')

ax.set_ylabel('Giá trị vị trí chuẩn hóa (RobustScaled Score)', fontweight='bold')
ax.set_title('Hồ sơ đặc trưng hóa lý: So sánh nhóm Rượu phổ thông vs Rượu thượng hạng', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(compare_cols, fontweight='bold', fontsize=11)
ax.legend(fontsize=11)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')

plt.tight_layout()
plt.savefig('images/chemical_profile_comparison.png', dpi=300)
plt.close()
print("Saved chemical_profile_comparison.png")
