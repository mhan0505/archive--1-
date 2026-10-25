import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import RobustScaler, StandardScaler
import nbformat as nbf

os.makedirs('images', exist_ok=True)
sns.set_theme(style='whitegrid')

# 1. Load Data
df = pd.read_csv('winequality-red.csv')

# 2. Outliers Summary Table
records = []
for col in df.columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers_cnt = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    pct = (outliers_cnt / len(df)) * 100
    records.append({
        'feature': col,
        'q1': round(q1, 4),
        'median': round(df[col].median(), 4),
        'q3': round(q3, 4),
        'iqr': round(iqr, 4),
        'lower_bound': round(lower_bound, 4),
        'upper_bound': round(upper_bound, 4),
        'min': round(df[col].min(), 4),
        'max': round(df[col].max(), 4),
        'outlier_count': outliers_cnt,
        'outlier_percentage': round(pct, 2)
    })

outlier_df = pd.DataFrame(records)
outlier_df.to_csv('outliers_summary.csv', index=False)
print("Saved outliers_summary.csv")

# 3. Create Plots
# Plot 1: Target Quality Distribution & Binary split
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.countplot(x='quality', data=df, palette='viridis', ax=axes[0])
axes[0].set_title('Phân phối thang điểm chất lượng gốc (3 - 8)', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Quality Score')
axes[0].set_ylabel('Số lượng mẫu')
for p in axes[0].patches:
    axes[0].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')

binary_quality = (df['quality'] >= 6).map({True: 'Ngon (>=6)', False: 'Trung bình/Kém (<6)'})
binary_quality.value_counts().plot.pie(autopct='%1.1f%%', colors=['#4CAF50', '#FF7043'], ax=axes[1], startangle=90, explode=(0.04, 0))
axes[1].set_title('Phân loại nhị phân (Binary Quality)', fontsize=13, fontweight='bold')
axes[1].set_ylabel('')
plt.tight_layout()
plt.savefig('images/target_quality_distribution.png', dpi=300)
plt.close()

# Plot 2: Boxplots of features before clipping (Demonstrating Outliers)
features_to_plot = ['residual sugar', 'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'sulphates', 'alcohol']
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()
for idx, col in enumerate(features_to_plot):
    sns.boxplot(y=df[col], ax=axes[idx], color='#42A5F5', flierprops=dict(marker='o', markersize=4, markerfacecolor='red', alpha=0.6))
    axes[idx].set_title(f'Biểu đồ hộp: {col}', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Giá trị đo')
plt.suptitle('Minh chứng các điểm ngoại lệ (Outliers màu đỏ) qua phương pháp IQR', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('images/outliers_boxplot_before.png', dpi=300)
plt.close()

# Plot 3: Scaling Comparison (Raw vs StandardScaler vs RobustScaler for Residual Sugar & Chlorides)
fig, axes = plt.subplots(2, 3, figsize=(16, 8))
raw_sugar = df['residual sugar']
std_sugar = StandardScaler().fit_transform(df[['residual sugar']])
rob_sugar = RobustScaler().fit_transform(df[['residual sugar']])

sns.histplot(raw_sugar, kde=True, ax=axes[0, 0], color='skyblue')
axes[0, 0].set_title('Residual Sugar: Dữ liệu thô (Lệch phải)', fontweight='bold')
sns.histplot(std_sugar, kde=True, ax=axes[0, 1], color='orange')
axes[0, 1].set_title('StandardScaler (Bị nén tâm do Mean lệch)', fontweight='bold')
sns.histplot(rob_sugar, kde=True, ax=axes[0, 2], color='green')
axes[0, 2].set_title('RobustScaler (Bảo toàn phân phối trung tâm)', fontweight='bold')

raw_chlor = df['chlorides']
std_chlor = StandardScaler().fit_transform(df[['chlorides']])
rob_chlor = RobustScaler().fit_transform(df[['chlorides']])

sns.histplot(raw_chlor, kde=True, ax=axes[1, 0], color='skyblue')
axes[1, 0].set_title('Chlorides: Dữ liệu thô (Ngoại lệ đuôi dài)', fontweight='bold')
sns.histplot(std_chlor, kde=True, ax=axes[1, 1], color='orange')
axes[1, 1].set_title('StandardScaler', fontweight='bold')
sns.histplot(rob_chlor, kde=True, ax=axes[1, 2], color='green')
axes[1, 2].set_title('RobustScaler (Kháng ngoại lệ tối ưu)', fontweight='bold')

plt.suptitle('So sánh tác động của các kỹ thuật Chuẩn hóa phân phối (Feature Scaling)', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('images/scaling_distribution_comparison.png', dpi=300)
plt.close()
print("Saved plots in images/")

# 4. Pipeline Execution & Save Cleaned Data
df_clean = df.drop_duplicates(keep='first').copy()
features = [c for c in df_clean.columns if c != 'quality']

# Winsorization clipping at 1.5 x IQR
for col in features:
    q1 = df_clean[col].quantile(0.25)
    q3 = df_clean[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df_clean[col] = np.clip(df_clean[col], lower_bound, upper_bound)

# Label encoding
df_clean['quality_binary'] = (df_clean['quality'] >= 6).astype(int)

# Robust scaling
scaler = RobustScaler()
scaled_features = scaler.fit_transform(df_clean[features])
df_scaled = pd.DataFrame(scaled_features, columns=[f'{c}_scaled' for c in features], index=df_clean.index)

df_final = pd.concat([df_clean, df_scaled], axis=1)
df_final.to_csv('winequality-red-cleaned.csv', index=False)
print("Saved winequality-red-cleaned.csv. Shape:", df_final.shape)

# 5. Build Jupyter Notebook hp.ipynb
nb = nbf.v4.new_notebook()

cells = []

# Title & Info
cells.append(nbf.v4.new_markdown_cell("""# BÁO CÁO THỰC THI DỮ LIỆU: GIAI ĐOẠN 1 & 2
## ĐỀ TÀI: PHÂN TÍCH CHẤT LƯỢNG RƯỢU VANG ĐỎ (RED WINE QUALITY)
**Tập dữ liệu:** `winequality-red.csv` (1,599 quan sát, 12 thuộc tính hóa lý & cảm quan)

---
### NỘI DUNG THỰC HIỆN:
- **Giai đoạn 1:** Thu thập, đọc cấu trúc, rà soát kiểu dữ liệu, kiểm tra giá trị khuyết thiếu (Missing values), đánh giá tính toàn vẹn.
- **Giai đoạn 2:** Phát hiện & xử lý trùng lặp (Duplicates), kiểm định ngoại lệ bằng phương pháp IQR (Outliers), giải trình lựa chọn kỹ thuật (Winsorization vs RobustScaler), gắn nhãn phân loại cân bằng và xuất dữ liệu sạch (`winequality-red-cleaned.csv`).
"""))

cells.append(nbf.v4.new_code_cell("""# 1. Cài đặt và nạp các thư viện phân tích dữ liệu cần thiết
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import RobustScaler, StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Thiết lập phong cách trực quan hóa
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
print("Thư viện đã được nạp thành công!")"""))

# Stage 1
cells.append(nbf.v4.new_markdown_cell("""---
## GIAI ĐOẠN 1: THU THẬP VÀ ĐÁNH GIÁ DỮ LIỆU BAN ĐẦU

### 1.1. Đọc dữ liệu và rà soát kích thước
Nguồn gốc: Tập dữ liệu Red Wine Quality từ UCI Machine Learning Repository (P. Cortez et al., 2009)."""))

cells.append(nbf.v4.new_code_cell("""# Đọc tập dữ liệu gốc
df = pd.read_csv('winequality-red.csv')

print(f"Kích thước tập dữ liệu gốc (Shape): {df.shape[0]} dòng, {df.shape[1]} cột")
print("-" * 60)
df.head()"""))

cells.append(nbf.v4.new_markdown_cell("""### 1.2. Rà soát cấu trúc, kiểu dữ liệu từng trường và giá trị khuyết thiếu (Missing Values)"""))

cells.append(nbf.v4.new_code_cell("""# Kiểm tra tổng quan kiểu dữ liệu và giá trị thiếu
audit_df = pd.DataFrame({
    'Kiểu Dtype': df.dtypes,
    'Số lượng hợp lệ': df.count(),
    'Số lượng thiếu (NaN)': df.isnull().sum(),
    'Tỷ lệ thiếu (%)': (df.isnull().sum() / len(df)) * 100,
    'Số giá trị duy nhất (Unique)': df.nunique()
})

audit_df"""))

cells.append(nbf.v4.new_markdown_cell("""**Nhận xét Giai đoạn 1:**
- Toàn bộ 11 biến hóa lý đều thuộc kiểu `float64`, hoàn toàn chính xác với bản chất của phép đo phân tích định lượng trong phòng thí nghiệm.
- Biến mục tiêu `quality` thuộc kiểu số nguyên `int64` (thang điểm đánh giá từ 3 đến 8).
- **Tỷ lệ thiếu (Missing values): 0.0%** trên toàn bộ các cột. Không có giá trị `NaN`/`Null`.
- Không phát sinh liên kết khóa ngoại/gộp bảng (Single-table structure), không có rủi ro bất đồng bộ khóa."""))

cells.append(nbf.v4.new_markdown_cell("""### 1.3. Thống kê mô tả tổng quan (Descriptive Statistics)"""))

cells.append(nbf.v4.new_code_cell("""# Bảng thống kê các chỉ số tập trung và độ phân tán
summary_stats = df.describe().T[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
summary_stats['IQR'] = summary_stats['75%'] - summary_stats['25%']
summary_stats"""))

# Stage 2
cells.append(nbf.v4.new_markdown_cell("""---
## GIAI ĐOẠN 2: TIỀN XỬ LÝ VÀ LÀM SẠCH DỮ LIỆU

### 2.1. Nhận diện và Xử lý dữ liệu trùng lặp (Duplicate Records)
- **Vấn đề phát hiện:** Tập dữ liệu có các dòng trùng lặp giống nhau 100% ở toàn bộ 12 thuộc tính.
- **Giải pháp:** Loại bỏ các dòng lặp để tránh rò rỉ dữ liệu (Data Leakage) khi huấn luyện mô hình sau này."""))

cells.append(nbf.v4.new_code_cell("""# Kiểm tra số lượng dòng trùng lặp
n_duplicates = df.duplicated().sum()
pct_duplicates = (n_duplicates / len(df)) * 100

print(f"Số lượng dòng trùng lặp: {n_duplicates} dòng ({pct_duplicates:.2f}% tổng dữ liệu)")

# Loại bỏ dòng trùng lặp, giữ lại quan sát đầu tiên
df_cleaned = df.drop_duplicates(keep='first').copy()
print(f"Kích thước sau khi loại bỏ trùng lặp: {df_cleaned.shape[0]} dòng, {df_cleaned.shape[1]} cột")"""))

cells.append(nbf.v4.new_markdown_cell("""### 2.2. Nhận diện và Định lượng Ngoại lệ (Outliers) bằng phương pháp IQR
Công thức xác định biên phân vị:
- $IQR = Q_3 - Q_1$
- $Ngưỡng\\ dưới (Lower\\ Bound) = Q_1 - 1.5 \\times IQR$
- $Ngưỡng\\ trên (Upper\\ Bound) = Q_3 + 1.5 \\times IQR$"""))

cells.append(nbf.v4.new_code_cell("""# Tính toán số lượng và tỷ lệ ngoại lệ cho từng thuộc tính
outlier_records = []
for col in df_cleaned.columns:
    q1 = df_cleaned[col].quantile(0.25)
    q3 = df_cleaned[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers_cnt = ((df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)).sum()
    pct = (outliers_cnt / len(df_cleaned)) * 100
    outlier_records.append({
        'Thuộc tính': col,
        'Q1': round(q1, 3),
        'Median': round(df_cleaned[col].median(), 3),
        'Q3': round(q3, 3),
        'IQR': round(iqr, 3),
        'Ngưỡng dưới': round(lower_bound, 3),
        'Ngưỡng trên': round(upper_bound, 3),
        'Số Outlier': outliers_cnt,
        'Tỷ lệ Outlier (%)': round(pct, 2)
    })

pd.DataFrame(outlier_records)"""))

cells.append(nbf.v4.new_code_cell("""# Trực quan hóa ngoại lệ thông qua Boxplots
features_inspect = ['residual sugar', 'chlorides', 'total sulfur dioxide', 'sulphates', 'alcohol', 'fixed acidity']

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for idx, col in enumerate(features_inspect):
    sns.boxplot(y=df_cleaned[col], ax=axes[idx], color='#64B5F6',
                flierprops=dict(marker='o', markersize=5, markerfacecolor='crimson', alpha=0.7))
    axes[idx].set_title(f'Phân bố & Outlier: {col}', fontweight='bold')
    axes[idx].set_ylabel('Giá trị')

plt.suptitle('Biểu đồ hộp (Boxplot) phát hiện giá trị ngoại lệ của các chỉ số hóa lý', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""### 2.3. Giải trình lựa chọn kỹ thuật và Cơ sở khoa học

#### A. Tại sao KHÔNG xóa bỏ hoàn toàn tất cả các dòng Outlier?
1. **Bảo toàn cỡ mẫu:** Nếu xóa tất cả các dòng có ít nhất một giá trị ngoại lệ theo chuẩn $1.5 \\times IQR$, ta sẽ mất hơn **20%** lượng quan sát thực nghiệm.
2. **Bản chất công nghệ thực phẩm:** Các chỉ số như `residual sugar` cao bất thường (lên đến $15.5\\,g/dm^3$) hay `chlorides` cao phản ánh đặc tính của các mẻ rượu đặc biệt (rượu ngọt dessert wine hoặc nho từ vùng đất duyên hải có độ mặn tự nhiên). Đây là **biến thiên có thật trong tự nhiên**, không phải lỗi nhập liệu.
3. **Giải pháp áp dụng:** Kỹ thuật **Winsorization (Capping)** tại ngưỡng $[Lower\\ Bound, Upper\\ Bound]$ để khử bỏ tác động bóp méo mô hình của các giá trị cực đoan mà vẫn bảo tồn đầy đủ 1,359 mẫu quan sát.

#### B. Tại sao lựa chọn `RobustScaler` thay vì `StandardScaler` hay `MinMaxScaler`?
- `MinMaxScaler`: Bị ảnh hưởng nặng nề bởi giá trị cực đại. Nếu có điểm cực trị, toàn bộ các điểm còn lại sẽ bị dồn nén về khoảng hẹp $[0, 0.2]$.
- `StandardScaler`: Dựa vào $Mean$ và $Std$, vốn là hai tham số rất nhạy cảm với phân phối lệch phải (Right-skewed) như đường dư hay muối khoáng.
- **`RobustScaler`**: Sử dụng công thức:
  $$\\tilde{x} = \\frac{x - \\text{Median}}{IQR}$$
  Trung vị (Median) và Khoảng phân vị (IQR) không bị kéo lệch bởi các giá trị ngoại lai cực lớn, giúp chuẩn hóa đặc trưng một cách khách quan nhất."""))

cells.append(nbf.v4.new_code_cell("""# 1. Áp dụng kỹ thuật Winsorization (Capping tại biên 1.5 x IQR)
features_to_scale = [col for col in df_cleaned.columns if col != 'quality']

for col in features_to_scale:
    q1 = df_cleaned[col].quantile(0.25)
    q3 = df_cleaned[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df_cleaned[col] = np.clip(df_cleaned[col], lower_bound, upper_bound)

print("Đã hoàn thành Capping ngoại lệ bằng phương pháp Winsorization!")"""))

cells.append(nbf.v4.new_code_cell("""# 2. So sánh phân phối trước và sau Chuẩn hóa (Minh chứng RobustScaler)
fig, axes = plt.subplots(1, 3, figsize=(16, 4))

raw_val = df['residual sugar']
std_val = StandardScaler().fit_transform(df[['residual sugar']])
rob_val = RobustScaler().fit_transform(df[['residual sugar']])

sns.histplot(raw_val, kde=True, ax=axes[0], color='cornflowerblue')
axes[0].set_title('Residual Sugar: Dữ liệu thô', fontweight='bold')

sns.histplot(std_val, kde=True, ax=axes[1], color='coral')
axes[1].set_title('StandardScaler (Mean = 0, Std = 1)', fontweight='bold')

sns.histplot(rob_val, kde=True, ax=axes[2], color='mediumseagreen')
axes[2].set_title('RobustScaler (Median = 0, IQR = 1)', fontweight='bold')

plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""### 2.4. Feature Engineering: Tạo nhãn phân loại cân bằng (`quality_binary`)"""))

cells.append(nbf.v4.new_code_cell("""# Khảo sát phân bố biến mục tiêu gốc
print("Phân phối thang điểm gốc:")
print(df_cleaned['quality'].value_counts().sort_index())

# Rời rạc hóa thành 2 nhóm chất lượng:
# 0: Trung bình / Kém (Quality <= 5)
# 1: Ngon / Cao cấp (Quality >= 6)
df_cleaned['quality_binary'] = (df_cleaned['quality'] >= 6).astype(int)

# Trực quan hóa mức độ cân bằng nhãn
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

sns.countplot(x='quality', data=df_cleaned, palette='Blues_r', ax=axes[0])
axes[0].set_title('Phân phối thang điểm 3 đến 8 (Mất cân bằng)', fontweight='bold')

df_cleaned['quality_binary'].value_counts().plot.pie(
    autopct='%1.1f%%', 
    labels=['Ngon (>=6)', 'Kém/TB (<6)'], 
    colors=['#66BB6A', '#FFA726'],
    startangle=90, 
    ax=axes[1]
)
axes[1].set_title('Tỷ lệ nhãn nhị phân sau xử lý (Lý tưởng cho Machine Learning)', fontweight='bold')
axes[1].set_ylabel('')

plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""### 2.5. Xuất tập dữ liệu sạch hoàn chỉnh (`winequality-red-cleaned.csv`)"""))

cells.append(nbf.v4.new_code_cell("""# Thực hiện RobustScaler trên toàn bộ 11 thuộc tính
scaler = RobustScaler()
scaled_matrix = scaler.fit_transform(df_cleaned[features_to_scale])
scaled_df = pd.DataFrame(
    scaled_matrix, 
    columns=[f'{col}_scaled' for col in features_to_scale], 
    index=df_cleaned.index
)

# Hợp nhất bảng dữ liệu cuối cùng
final_cleaned_df = pd.concat([df_cleaned, scaled_df], axis=1)

# Lưu trữ file sạch
final_cleaned_df.to_csv('winequality-red-cleaned.csv', index=False)
print(f"Đã lưu thành công dữ liệu sạch vào file: 'winequality-red-cleaned.csv'")
print(f"Kích thước file sạch: {final_cleaned_df.shape[0]} dòng, {final_cleaned_df.shape[1]} cột")
final_cleaned_df.head(3)"""))

nb.cells = cells

with open('hp.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Saved notebook hp.ipynb successfully!")
