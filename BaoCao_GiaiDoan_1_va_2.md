# BÁO CÁO CHI TIẾT: GIAI ĐOẠN 1 & GIAI ĐOẠN 2
**Đề tài:** Phân tích Dữ liệu Hóa lý & Chất lượng Rượu vang Đỏ (*Red Wine Quality*)  
**Tập dữ liệu:** `winequality-red.csv` (Cortez et al., 2009 - UCI Machine Learning Repository)

---

## MỤC LỤC
1. [GIAI ĐOẠN 1: THU THẬP VÀ ĐÁNH GIÁ DỮ LIỆU BAN ĐẦU](#giai-đoạn-1-thu-thập-và-đánh-giá-dữ-liệu-ban-đầu)
   - 1.1. Nguồn dữ liệu và Mục tiêu bài toán
   - 1.2. Cấu trúc tập dữ liệu và Định nghĩa thuộc tính
   - 1.3. Rà soát hiện trạng: Kiểu dữ liệu và Giá trị khuyết thiếu
   - 1.4. Đánh giá tính nhất quán và Tính toàn vẹn
2. [GIAI ĐOẠN 2: TIỀN XỬ LÝ VÀ LÀM SẠCH DỮ LIỆU](#giai-đoạn-2-tiền-xử-lý-và-làm-sạch-dữ-liệu)
   - 2.1. Phát hiện và Xử lý dữ liệu trùng lặp (Duplicate Records)
   - 2.2. Nhận diện và Định lượng Ngoại lệ (Outliers Analysis)
   - 2.3. Giải trình lựa chọn kỹ thuật và Cơ sở khoa học
   - 2.4. Quy trình xử lý ngoại lệ và Chuẩn hóa dữ liệu (Scaling)
   - 2.5. Tạo lập dữ liệu sạch xuất xưởng (`winequality-red-cleaned.csv`)

---

# GIAI ĐOẠN 1: THU THẬP VÀ ĐÁNH GIÁ DỮ LIỆU BAN ĐẦU

### 1.1. Nguồn dữ liệu và Mục tiêu bài toán
- **Tập dữ liệu lựa chọn:** Red Wine Quality Dataset từ Viện Nghiên cứu Rượu vang Minho, Bồ Đào Nha (công bố bởi P. Cortez, A. Cerdeira, F. Almeida, T. Matos và J. Reis, 2009).
- **Cấu trúc lưu trữ:** 01 file định dạng Comma-Separated Values (`winequality-red.csv`), dung lượng xấp xỉ 101 KB.
- **Quy mô quan sát:** 
  - Tổng số dòng quan sát (samples): **1,599** mẫu rượu vang đỏ.
  - Tổng số cột (features): **12** cột (gồm 11 biến hóa lý đầu vào và 1 biến chất lượng đầu ra).
- **Mục tiêu bài toán:**
  - *Mục tiêu kỹ thuật:* Kiểm tra chất lượng dữ liệu đo đạc trong phòng thí nghiệm, làm sạch và chuẩn bị dữ liệu chuẩn xác cho các mô hình hồi quy (Regression) hoặc phân loại (Classification).
  - *Mục tiêu ứng dụng:* Xác định các thành phần hóa chất mang tính quyết định đến phẩm chất cảm quan của rượu, giúp các xưởng ủ rượu chủ động kiểm soát quy trình lên men và phân hạng sản phẩm.

---

### 1.2. Cấu trúc tập dữ liệu và Danh mục thuộc tính

| STT | Tên thuộc tính | Đơn vị đo | Ý nghĩa hóa lý / Chuyên môn | Vai trò |
| :---: | :--- | :--- | :--- | :---: |
| 1 | `fixed acidity` | $g(tartaric\ acid)/dm^3$ | Axit cố định (chủ yếu là axit tartaric), tạo độ chua chính và giữ cấu trúc rượu | Biến độc lập |
| 2 | `volatile acidity` | $g(acetic\ acid)/dm^3$ | Axit dễ bay hơi (axit axetic), nếu quá cao gây mùi giấm hỏng khó chịu | Biến độc lập |
| 3 | `citric acid` | $g/dm^3$ | Axit xitric, lượng nhỏ giúp tăng độ tươi mát và thanh lịch của rượu | Biến độc lập |
| 4 | `residual sugar` | $g/dm^3$ | Lượng đường còn sót lại sau khi quá trình lên men dừng lại | Biến độc lập |
| 5 | `chlorides` | $g(sodium\ chloride)/dm^3$ | Lượng muối khoáng trong rượu, ảnh hưởng đến độ mặn và độ cân bằng | Biến độc lập |
| 6 | `free sulfur dioxide` | $mg/dm^3$ | Dạng khí $SO_2$ tự do hòa tan, chống oxy hóa và ức chế vi sinh vật gây hại | Biến độc lập |
| 7 | `total sulfur dioxide` | $mg/dm^3$ | Tổng lượng $SO_2$ (tự do + liên kết), nếu quá cao sẽ gây mùi hắc | Biến độc lập |
| 8 | `density` | $g/cm^3$ | Khối lượng riêng của rượu, phụ thuộc vào nồng độ cồn và lượng đường dư | Biến độc lập |
| 9 | `pH` | Thang đo 0–14 | Độ pH đo tính axit của rượu (phần lớn rượu vang nằm từ 3.0 đến 3.8) | Biến độc lập |
| 10 | `sulphates` | $g(potassium\ sulphate)/dm^3$ | Chất phụ gia sunfat, hỗ trợ sinh khí $SO_2$ bảo quản rượu | Biến độc lập |
| 11 | `alcohol` | % thể tích ($% vol$) | Nồng độ cồn ethanol sinh ra sau quá trình lên men đường | Biến độc lập |
| 12 | `quality` | Điểm số (0 – 10) | Điểm cảm quan trung bình do ít nhất 3 chuyên gia thẩm định nếm thử | **Biến mục tiêu** |

---

### 1.3. Rà soát hiện trạng: Kiểu dữ liệu và Tỷ lệ khuyết thiếu

Thực hiện kiểm tra bằng code Python:
```python
import pandas as pd
df = pd.read_csv('winequality-red.csv')
print(df.info())
print(df.isnull().sum())
```

**Bảng tổng hợp kiểm tra thuộc tính và giá trị thiếu:**

| Thuộc tính | Kiểu dữ liệu (`Dtype`) | Số lượng bản ghi hợp lệ (`Non-Null`) | Số lượng thiếu (`Null Count`) | Tỷ lệ thiếu (`%`) |
| :--- | :---: | :---: | :---: | :---: |
| `fixed acidity` | `float64` | 1,599 | 0 | 0.0% |
| `volatile acidity` | `float64` | 1,599 | 0 | 0.0% |
| `citric acid` | `float64` | 1,599 | 0 | 0.0% |
| `residual sugar` | `float64` | 1,599 | 0 | 0.0% |
| `chlorides` | `float64` | 1,599 | 0 | 0.0% |
| `free sulfur dioxide` | `float64` | 1,599 | 0 | 0.0% |
| `total sulfur dioxide` | `float64` | 1,599 | 0 | 0.0% |
| `density` | `float64` | 1,599 | 0 | 0.0% |
| `pH` | `float64` | 1,599 | 0 | 0.0% |
| `sulphates` | `float64` | 1,599 | 0 | 0.0% |
| `alcohol` | `float64` | 1,599 | 0 | 0.0% |
| `quality` | `int64` | 1,599 | 0 | 0.0% |

**Nhận xét hiện trạng:**
1. **Kiểu dữ liệu:** 11 chỉ số hóa lý được lưu trữ ở định dạng số thực liên tục `float64`, hoàn toàn chính xác với bản chất của phép đo phân tích hóa học. Biến mục tiêu `quality` là số nguyên rời rạc `int64`. Không có cột nào bị lỗi lưu nhầm dạng văn bản (`string`/`object`).
2. **Giá trị khuyết thiếu (Missing values):** Tỷ lệ thiếu là **0.0%** trên toàn bộ 1,599 quan sát. Đây là tập dữ liệu đo đạc chuẩn hóa trong môi trường kiểm nghiệm nghiêm ngặt.

---

### 1.4. Đánh giá tính nhất quán và Tính toàn vẹn
- **Cấu trúc bảng:** Dữ liệu được tổ chức dưới dạng một bảng phẳng duy nhất (single table), không có liên kết khóa ngoại ($Foreign\ Key$) với bảng ngoài. Do đó không xảy ra xung đột khóa hoặc mất mát dữ liệu do gộp bảng (Merge/Join).
- **Phạm vi giá trị hợp lệ (Domain Range Validity):**
  - $pH$: Nằm trong khoảng $2.74$ đến $4.01$, hoàn toàn phù hợp với tính axit sinh hóa của vang đỏ.
  - $density$: Dao động từ $0.99007$ đến $1.00369\,g/cm^3$ (xung quanh tỷ trọng của nước $1.0000$), phản ánh đúng đặc tính tỷ trọng rượu.
  - $quality$: Dao động từ mức $3$ đến mức $8$ (không có mẫu nào chạm đáy $0-2$ hoặc đạt tuyệt đối $9-10$).

---

# GIAI ĐOẠN 2: TIỀN XỬ LÝ VÀ LÀM SẠCH DỮ LIỆU

### 2.1. Phát hiện và Xử lý dữ liệu trùng lặp (Duplicate Records)

- **Minh chứng định lượng:**
  Thực hiện kiểm tra các bản ghi trùng lặp trên toàn bộ 12 thuộc tính:
  ```python
  duplicates_count = df.duplicated().sum()
  # Kết quả: 240 dòng
  ```
  Tập dữ liệu chứa **240 dòng trùng lặp hoàn toàn** (chiếm **15.01%** trên tổng số 1,599 quan sát ban đầu).
- **Phương án xử lý:**
  Loại bỏ toàn bộ 240 dòng bản sao, chỉ giữ lại một bản ghi đầu tiên đại diện:
  ```python
  df_cleaned = df.drop_duplicates(keep='first').copy()
  ```
  Sau khi loại bỏ, tập dữ liệu còn lại **1,359 mẫu quan sát duy nhất**.
- **Giải trình kỹ thuật:**
  Mặc dù trong sản xuất có thể có nhiều chai rượu cùng một mẻ, nhưng khi xây dựng mô hình dự báo học máy hoặc kiểm định thống kê, sự trùng lặp 15% các hàng giống hệt nhau sẽ gây hiện tượng **Data Leakage** (rò rỉ dữ liệu giữa tập train/test) và phóng đại giả tạo độ chính xác của mô hình.

---

### 2.2. Nhận diện và Định lượng Ngoại lệ (Outliers Analysis)

Sử dụng phương pháp **Biên phân vị (Interquartile Range - IQR)**:
- Phân vị 25% ($Q_1$), Phân vị 75% ($Q_3$), Khoảng phân vị $IQR = Q_3 - Q_1$.
- Ngưỡng dưới: $Lower = Q_1 - 1.5 \times IQR$
- Ngưỡng trên: $Upper = Q_3 + 1.5 \times IQR$

**Bảng thống kê định lượng Outlier trên tập dữ liệu 1,599 mẫu ban đầu:**

| Thuộc tính | $Q_1$ | Median ($Q_2$) | $Q_3$ | $IQR$ | Ngưỡng dưới | Ngưỡng trên | Min - Max | Số Outlier | Tỷ lệ (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `fixed acidity` | 7.10 | 7.90 | 9.20 | 2.10 | 3.95 | 12.35 | 4.60 - 15.90 | 49 | 3.06% |
| `volatile acidity` | 0.39 | 0.52 | 0.64 | 0.25 | 0.015 | 1.015 | 0.12 - 1.58 | 19 | 1.19% |
| `citric acid` | 0.09 | 0.26 | 0.42 | 0.33 | -0.405 | 0.915 | 0.00 - 1.00 | 1 | 0.06% |
| `residual sugar` | 1.90 | 2.20 | 2.60 | 0.70 | 0.85 | 3.65 | 0.90 - 15.50 | **155** | **9.69%** |
| `chlorides` | 0.07 | 0.079 | 0.09 | 0.02 | 0.040 | 0.120 | 0.012 - 0.611 | **112** | **7.00%** |
| `free sulfur dioxide` | 7.00 | 14.00 | 21.00 | 14.00 | -14.00 | 42.00 | 1.00 - 72.00 | 30 | 1.88% |
| `total sulfur dioxide` | 22.00 | 38.00 | 62.00 | 40.00 | -38.00 | 122.00 | 6.00 - 289.00 | 55 | 3.44% |
| `density` | 0.9956 | 0.9967 | 0.9978 | 0.0022 | 0.9923 | 1.0011 | 0.9901 - 1.0037 | 45 | 2.81% |
| `pH` | 3.21 | 3.31 | 3.40 | 0.19 | 2.925 | 3.685 | 2.74 - 4.01 | 35 | 2.19% |
| `sulphates` | 0.55 | 0.62 | 0.73 | 0.18 | 0.280 | 1.000 | 0.33 - 2.00 | 59 | 3.69% |
| `alcohol` | 9.50 | 10.20 | 11.10 | 1.60 | 7.10 | 13.50 | 8.40 - 14.90 | 13 | 0.81% |
| `quality` | 5.00 | 6.00 | 6.00 | 1.00 | 3.50 | 7.50 | 3.00 - 8.00 | 28 | 1.75% |

---

### 2.3. Giải trình lựa chọn kỹ thuật và Cơ sở khoa học

#### 1. Tại sao KHÔNG xóa bỏ hoàn toàn tất cả các dòng Outlier?
- **Nguy cơ mất thông tin:** Nếu loại bỏ toàn bộ các dòng chứa ít nhất một thuộc tính ngoại lệ, ta sẽ mất tới hơn $25\%$ tập dữ liệu.
- **Bản chất thực nghiệm:** Trong ngành sản xuất rượu vang, các mẫu có `residual sugar` cao bất thường (lên đến $15.5\,g/dm^3$) là các dòng vang ngọt đặc biệt (Sweet / Dessert wine). Tương tự, lượng muối `chlorides` cao phản ánh nho được trồng ở các vùng thổ nhưỡng duyên hải có độ mặn tự nhiên. Đây là biến thiên thực tế của tự nhiên, không phải sai số đo đạc.
- **Giải pháp áp dụng:** 
  - Kỹ thuật **Winsorization (Capping)** tại bách phân vị thứ 1% và 99% (hoặc $1.5 \times IQR$ capping) để kiềm chế tác động cực đoan của các giá trị ngoại lai mà vẫn bảo toàn số lượng mẫu quan sát.

#### 2. Lựa chọn phương pháp Chuẩn hóa (Feature Scaling)
- **So sánh các phương pháp:**
  - *MinMaxScaler:* Ánh xạ dữ liệu về $[0, 1]$. Phương pháp này cực kỳ nhạy cảm với ngoại lệ; nếu có một giá trị cực đại lớn (như sugar = 15.5), phần lớn các điểm dữ liệu còn lại sẽ bị nén nghẽn lại ở khoảng $[0, 0.15]$.
  - *StandardScaler (Z-Score):* Chuẩn hóa về $\mu = 0, \sigma = 1$. Dù phổ biến, công thức này phụ thuộc trực tiếp vào Trung bình ($Mean$) và Độ lệch chuẩn ($Std$) – hai chỉ số bị bóp méo nặng khi phân phối bị lệch phải.
  - **Lựa chọn tối ưu: `RobustScaler`**
    $$\tilde{x} = \frac{x - Q_2(x)}{IQR(x)} = \frac{x - Median(x)}{Q_3(x) - Q_1(x)}$$
    - **Lý do lựa chọn:** `RobustScaler` sử dụng Trung vị và Khoảng phân vị IQR làm thước đo vị trí và độ phân tán. Hai đại lượng này có tính kháng ngoại lệ rất cao (robust to outliers), đảm bảo các đặc trưng hóa học sau chuẩn hóa phản ánh đúng cấu trúc phân phối của đại đa số mẫu rượu thông thường.

#### 3. Chuyển đổi bài toán (Feature Engineering & Label Encoding)
- **Đặc điểm biến mục tiêu `quality`:**
  - Điểm 3: 10 mẫu ($0.6\%$)
  - Điểm 4: 53 mẫu ($3.3\%$)
  - Điểm 5: 681 mẫu ($42.6\%$)
  - Điểm 6: 638 mẫu ($39.9\%$)
  - Điểm 7: 199 mẫu ($12.4\%$)
  - Điểm 8: 18 mẫu ($1.1\%$)
- **Giải trình:** Phân phối điểm số tập trung cực lớn vào hai mức 5 và 6 (chiếm $82.5\%$), trong khi các điểm cực biên rất thưa thớt. Nếu huấn luyện mô hình đa lớp 6 mức độ mà không xử lý sẽ dẫn đến dự đoán thiên vị hoàn toàn về lớp 5 và 6.
- **Giải pháp:** 
  - Tạo thêm biến phân lớp nhị phân `quality_binary`:
    - `0` (Rượu bình thường / Kém): Điểm $quality \le 5$ (744 mẫu).
    - `1` (Rượu ngon / Thượng hạng): Điểm $quality \ge 6$ (855 mẫu).
  - Tỷ lệ giữa hai nhóm sau phân loại nhị phân là xấp xỉ **46.5% vs 53.5%** — tạo ra một tập dữ liệu cân bằng lý tưởng cho các thuật toán phân lớp.

---

### 2.4. Quy trình thực thi Code Tiền xử lý

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler

# 1. Nạp dữ liệu gốc
df = pd.read_csv('winequality-red.csv')

# 2. Xử lý trùng lặp
df_clean = df.drop_duplicates().copy()

# 3. Kỹ thuật Winsorization (Capping tại 1.5 x IQR)
features = [col for col in df_clean.columns if col != 'quality']
for col in features:
    q1 = df_clean[col].quantile(0.25)
    q3 = df_clean[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df_clean[col] = np.clip(df_clean[col], lower_bound, upper_bound)

# 4. Feature Engineering: Tạo nhãn chất lượng nhị phân
df_clean['quality_binary'] = (df_clean['quality'] >= 6).astype(int)

# 5. Chuẩn hóa đặc trưng bằng RobustScaler
scaler = RobustScaler()
scaled_features = scaler.fit_transform(df_clean[features])
df_scaled = pd.DataFrame(scaled_features, columns=[f'{c}_scaled' for c in features], index=df_clean.index)

# Ghép bảng dữ liệu sạch hoàn chỉnh
df_final = pd.concat([df_clean, df_scaled], axis=1)
df_final.to_csv('winequality-red-cleaned.csv', index=False)
```

---

### 2.5. Kết quả dữ liệu sạch xuất xưởng (`winequality-red-cleaned.csv`)
1. **Số lượng bản ghi:** 1,359 dòng quan sát duy nhất, 0 bản ghi trùng lặp, 0 giá trị khuyết thiếu.
2. **Cấu trúc trường dữ liệu:**
   - 11 biến hóa lý gốc đã được Capping giới hạn biên bất thường.
   - 1 biến `quality` nguyên bản (thang đo 3–8).
   - 1 biến phân loại `quality_binary` cân bằng nhãn ($0$ và $1$).
   - 11 biến hóa lý chuẩn hóa `*_scaled` sẵn sàng đưa vào mô hình máy học (Logistic Regression, SVM, KNN, Random Forest,...).
3. **Mức độ hoàn thiện:** Toàn bộ dữ liệu sạch đã được lưu trữ sẵn sàng tại đường dẫn file: `winequality-red-cleaned.csv`.
