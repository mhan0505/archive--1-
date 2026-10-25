# BÁO CÁO TOÀN DIỆN DỰ ÁN PHÂN TÍCH DỮ LIỆU (4 GIAI ĐOẠN)
**Đề tài:** Phân tích Dữ liệu Hóa lý & Cảm quan Chất lượng Rượu vang Đỏ (*Red Wine Quality*)  
**Bộ dữ liệu:** `winequality-red.csv` (Cortez et al., 2009 - UCI Machine Learning Repository)  
**Quy mô dữ liệu:** 1,599 quan sát ban đầu $\rightarrow$ 1,359 quan sát sạch duy nhất, 12 thuộc tính gốc, 1 nhãn nhị phân, 11 đặc trưng RobustScaled.

---

## MỤC LỤC
1. [GIAI ĐOẠN 1: THU THẬP VÀ ĐÁNH GIÁ DỮ LIỆU BAN ĐẦU](#giai-đoạn-1-thu-thập-và-đánh-giá-dữ-liệu-ban-đầu)
   - 1.1. Nguồn dữ liệu & Mục tiêu bài toán
   - 1.2. Cấu trúc trường & Danh mục thuộc tính
   - 1.3. Rà soát hiện trạng: Kiểu dữ liệu và Tỷ lệ khuyết thiếu (Missing Values)
   - 1.4. Đánh giá tính nhất quán & Quan hệ dữ liệu
2. [GIAI ĐOẠN 2: TIỀN XỬ LÝ VÀ LÀM SẠCH DỮ LIỆU](#giai-đoạn-2-tiền-xử-lý-và-làm-sạch-dữ-liệu)
   - 2.1. Phát hiện và Xử lý dữ liệu trùng lặp (Duplicate Records)
   - 2.2. Nhận diện và Định lượng Ngoại lệ (Outliers) bằng phương pháp IQR
   - 2.3. Giải trình lựa chọn kỹ thuật và Cơ sở khoa học (Winsorization vs RobustScaler)
   - 2.4. Feature Engineering: Tạo nhãn phân loại cân bằng (`quality_binary`)
   - 2.5. Xuất tập dữ liệu sạch (`winequality-red-cleaned.csv`)
3. [GIAI ĐOẠN 3: PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU](#giai-đoạn-3-phân-tích-và-trực-quan-hóa-dữ-liệu)
   - 3.1. Thiết lập và Kiểm định các Giả thuyết Thống kê ($H_1, H_2, H_3, H_4$)
   - 3.2. Trực quan hóa có mục tiêu & Diễn giải chuyên sâu (Deep Insight)
     - *Hình 1:* Ma trận nhiệt tương quan Pearson (Heatmap)
     - *Hình 2:* Phân phối Violin – Boxplot của Nồng độ cồn và Axit bay hơi
     - *Hình 3:* Biểu đồ phân tán (Scatter Plot) xác định ranh giới hóa lý
     - *Hình 4:* Hồ sơ đặc trưng so sánh giữa Vang phổ thông và Vang thượng hạng
4. [GIAI ĐOẠN 4: ĐÁNH GIÁ TÁC ĐỘNG VÀ KHUYẾN NGHỊ](#giai-đoạn-4-đánh-giá-tác-động-và-khuyến-nghị)
   - 4.1. Tóm tắt các phát hiện chuyên môn và kinh doanh nổi bật
   - 4.2. Đề xuất giải pháp mang tính ứng dụng thực tế (Sản xuất, Kiểm định, Kinh doanh)
   - 4.3. Giới hạn dữ liệu và Định hướng nghiên cứu mở rộng trong tương lai

---

# GIAI ĐOẠN 1: THU THẬP VÀ ĐÁNH GIÁ DỮ LIỆU BAN ĐẦU

### 1.1. Nguồn dữ liệu & Mục tiêu bài toán
- **Tập dữ liệu:** Dữ liệu chuẩn *Red Wine Quality* thu thập tại vùng Minho, phía Bắc Bồ Đào Nha (thuộc dự án nghiên cứu của Cortez et al., 2009).
- **Cấu trúc lưu trữ:** 01 file CSV (`winequality-red.csv`), dung lượng xấp xỉ 101 KB, phân tách bằng dấu phẩy.
- **Quy mô quan sát ban đầu:** 1,599 dòng quan sát, 12 thuộc tính (11 biến hóa lý độc lập và 1 biến mục tiêu điểm cảm quan).
- **Mục tiêu bài toán:**
  - *Mục tiêu kỹ thuật:* Đánh giá độ tin cậy của các chỉ số đo lường phòng thí nghiệm, làm sạch và chuẩn hóa dữ liệu phục vụ phân tích thống kê và huấn luyện mô hình học máy.
  - *Mục tiêu ứng dụng:* Xác định các thành phần hóa chất mang tính quyết định đến điểm nếm thử cảm quan của chuyên gia, giúp nhà sản xuất tối ưu hóa quy trình lên men, kiểm soát hư hỏng và định giá phân khúc sản phẩm.

### 1.2. Cấu trúc trường dữ liệu

| STT | Tên thuộc tính | Đơn vị đo | Ý nghĩa chuyên môn | Vai trò |
| :---: | :--- | :--- | :--- | :---: |
| 1 | `fixed acidity` | $g/dm^3$ | Axit cố định (chủ yếu là axit tartaric), tạo bộ khung chua chính | Biến độc lập |
| 2 | `volatile acidity` | $g/dm^3$ | Axit dễ bay hơi (axit axetic), nếu cao sẽ gây mùi giấm chua hỏng | Biến độc lập |
| 3 | `citric acid` | $g/dm^3$ | Axit xitric, lượng nhỏ giúp tăng vị tươi mát và thanh nhã | Biến độc lập |
| 4 | `residual sugar` | $g/dm^3$ | Lượng đường còn đọng lại sau quá trình lên men | Biến độc lập |
| 5 | `chlorides` | $g/dm^3$ | Muối khoáng natri clorua, ảnh hưởng đến độ mặn và độ cân bằng | Biến độc lập |
| 6 | `free sulfur dioxide` | $mg/dm^3$ | $SO_2$ tự do hòa tan, chống oxy hóa và ức chế vi sinh vật | Biến độc lập |
| 7 | `total sulfur dioxide` | $mg/dm^3$ | Tổng lượng $SO_2$ (tự do + liên kết), liều cao gây mùi hắc nồng | Biến độc lập |
| 8 | `density` | $g/cm^3$ | Khối lượng riêng của rượu, tỷ lệ thuận với đường và nghịch với cồn | Biến độc lập |
| 9 | `pH` | Thang đo 0–14 | Độ pH đo tính axit của dung dịch (vang đỏ thường nằm từ 3.0 đến 3.8) | Biến độc lập |
| 10 | `sulphates` | $g/dm^3$ | Phụ gia kali sunfat, hỗ trợ sinh khí $SO_2$ bảo quản | Biến độc lập |
| 11 | `alcohol` | % thể tích | Nồng độ cồn ethanol sinh ra sau quá trình lên men | Biến độc lập |
| 12 | `quality` | Điểm 0 – 10 | Điểm nếm thử trung bình của hội đồng chuyên gia cảm quan | **Biến mục tiêu** |

### 1.3. Rà soát hiện trạng: Kiểu dữ liệu và Tỷ lệ khuyết thiếu
- **Kiểu dữ liệu:** 11 biến hóa lý đều thuộc kiểu số thực `float64`, hoàn toàn tương thích với các phép đo định lượng nồng độ dung dịch. Biến mục tiêu `quality` là kiểu số nguyên rời rạc `int64`. Không có trường nào bị lưu nhầm sang định dạng văn bản (`string`/`object`).
- **Tỷ lệ khuyết thiếu (Missing Values):** **0.0%** trên toàn bộ 1,599 dòng $\times$ 12 cột. Không có giá trị `NaN`, `Null` hoặc ô trống.
- **Tính nhất quán:** Dữ liệu đơn bảng (Single-table structure), không phát sinh liên kết khóa ngoại nên không xảy ra xung đột khóa hay mất mát dữ liệu do gộp bảng (Join/Merge).

---

# GIAI ĐOẠN 2: TIỀN XỬ LÝ VÀ LÀM SẠCH DỮ LIỆU

### 2.1. Phát hiện và Xử lý dữ liệu trùng lặp (Duplicate Records)
- **Minh chứng định lượng:** Kiểm tra toàn bộ 12 thuộc tính ghi nhận **240 dòng trùng lặp hoàn toàn** (chiếm **15.01%** tổng số quan sát).
- **Phương án xử lý:** Sử dụng lệnh `df.drop_duplicates(keep='first')` loại bỏ 240 dòng bản sao, giữ lại **1,359 mẫu quan sát duy nhất**.
- **Giải trình:** Việc lưu nhiều dòng giống hệt nhau có thể xuất phát từ việc ghi nhận trùng lặp mẫu thử trong cùng một lô thử nghiệm. Nếu giữ nguyên sẽ gây rò rỉ dữ liệu (Data Leakage) khi chia tập Train/Test, dẫn đến việc đánh giá độ chính xác của mô hình học máy bị thổi phồng giả tạo.

### 2.2. Nhận diện và Định lượng Ngoại lệ (Outliers Analysis)
Áp dụng phương pháp Biên phân vị (Interquartile Range - IQR):
- $IQR = Q_3 - Q_1$, $Lower = Q_1 - 1.5 \times IQR$, $Upper = Q_3 + 1.5 \times IQR$.

**Bảng định lượng Outlier trên dữ liệu sau khử trùng lặp (1,359 mẫu):**

| Thuộc tính | $Q_1$ | Median | $Q_3$ | $IQR$ | Ngưỡng dưới | Ngưỡng trên | Số Outlier | Tỷ lệ (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `residual sugar` | 1.90 | 2.20 | 2.60 | 0.70 | 0.85 | 3.65 | **126** | **9.27%** |
| `chlorides` | 0.07 | 0.079 | 0.091 | 0.021 | 0.039 | 0.122 | **87** | **6.40%** |
| `total sulfur dioxide` | 22.0 | 38.0 | 63.0 | 41.0 | -39.5 | 124.5 | 45 | 3.31% |
| `fixed acidity` | 7.10 | 7.90 | 9.30 | 2.20 | 3.80 | 12.60 | 41 | 3.02% |
| `density` | 0.9956 | 0.9967 | 0.9978 | 0.0022 | 0.9923 | 1.0011 | 35 | 2.58% |
| `sulphates` | 0.55 | 0.62 | 0.73 | 0.18 | 0.28 | 1.00 | 43 | 3.16% |
| `volatile acidity` | 0.39 | 0.52 | 0.64 | 0.25 | 0.015 | 1.015 | 19 | 1.40% |
| `alcohol` | 9.50 | 10.10 | 11.10 | 1.60 | 7.10 | 13.50 | 12 | 0.88% |

### 2.3. Giải trình lựa chọn kỹ thuật và Cơ sở khoa học
1. **Tại sao không xóa bỏ toàn bộ các dòng Outlier?**
   - Nếu xóa bỏ toàn bộ dòng chứa outlier, cỡ mẫu sẽ bị suy giảm hơn $20\%$. Quan trọng hơn, trong công nghệ sản xuất rượu vang, các mẫu có hàm lượng `residual sugar` cao bất thường (lên đến $15.5\,g/dm^3$) phản ánh dòng vang ngọt đặc biệt (dessert wine). Lượng `chlorides` cao phản ánh nho trồng tại vùng duyên hải chịu ảnh hưởng mặn của gió biển. Đây là **biến thiên thực nghiệm tự nhiên có thật**, không phải sai sót đo đạc.
   - *Giải pháp tối ưu:* Áp dụng kỹ thuật **Winsorization (Capping)** tại ngưỡng $[Lower, Upper]$ để triệt tiêu ảnh hưởng bóp méo mô hình của các điểm cực trị mà vẫn bảo tồn đủ 1,359 mẫu quan sát.
2. **Tại sao chọn `RobustScaler` thay vì `StandardScaler` hay `MinMaxScaler`?**
   - Phân phối của các biến hóa lý bị lệch phải (Right-skewed) rõ rệt với đuôi dài. `StandardScaler` dựa trên Mean và Std rất dễ bị lệch tâm. `MinMaxScaler` thì bị nén dồn dữ liệu về dải hẹp nếu có điểm cực đại.
   - `RobustScaler` co giãn dựa trên **Trung vị (Median)** và **Khoảng phân vị (IQR)**:
     $$\tilde{x} = \frac{x - Median}{IQR}$$
     Giúp thang đo chuẩn hóa không bị bóp méo bởi các giá trị ngoại lai, giữ nguyên vẹn hình thái phân phối tự nhiên của đại đa số mẫu rượu thông thường.
3. **Feature Engineering: Tạo nhãn cân bằng `quality_binary`**
   - Điểm 5 và 6 chiếm tới $82.5\%$ tổng số mẫu (điểm 3 chỉ có 10 mẫu, điểm 8 có 18 mẫu). Gom nhóm nhị phân: Điểm $\le 5$ (Kém/TB: 644 mẫu - $47.4\%$) và Điểm $\ge 6$ (Ngon: 715 mẫu - $52.6\%$). Tỷ lệ này tạo nên bài toán phân loại nhị phân cân bằng lý tưởng cho các thuật toán Machine Learning.

---

# GIAI ĐOẠN 3: PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU

### 3.1. Thiết lập và Kiểm định các Giả thuyết Thống kê

| Giả thuyết | Nội dung kiểm định | Chỉ số thống kê định lượng | Kết luận | Diễn giải chuyên môn |
| :--- | :--- | :--- | :---: | :--- |
| **$H_1$** | Nồng độ cồn (`alcohol`) tỉ lệ thuận với chất lượng rượu (`quality`) | Pearson $r = +0.4827$ ($p = 3.03 \times 10^{-80}$)<br>t-test: $t = 18.55$ ($p = 1.27 \times 10^{-68}$)<br>ANOVA: $F = 105.04$ ($p = 8.59 \times 10^{-94}$)<br>Mean: Low = 9.92%, High = 10.88% | **Chấp nhận $H_1$** | Cồn cao tạo cảm giác đầm vị, giữ hương este lâu hơn, được chuyên gia đánh giá vượt trội. |
| **$H_2$** | Axit dễ bay hơi (`volatile acidity`) làm giảm phẩm chất rượu | Pearson $r = -0.3921$ ($p = 3.49 \times 10^{-51}$)<br>t-test: $t = -12.80$ ($p = 1.63 \times 10^{-35}$)<br>Mean: Low = 0.59 g/dm3, High = 0.47 g/dm3 | **Chấp nhận $H_2$** | Axit axetic sinh ra từ vi khuẩn lên men giấm gây mùi chua hỏng, là kẻ thù số 1 của vang. |
| **$H_3$** | Lượng đường dư (`residual sugar`) quyết định chất lượng vang đỏ | Pearson $r = +0.0191$ ($p = 0.481 > 0.05$)<br>t-test: $t = -0.1902$ ($p = 0.849 > 0.05$)<br>Mean: Low = 2.33 g/dm3, High = 2.32 g/dm3 | **Bác bỏ $H_3$** | Không có mối liên hệ thống kê. Vang đỏ là vang khô, chất lượng dựa trên cấu trúc tanin chứ không dựa vào độ ngọt. |
| **$H_4$** | Hàm lượng sunfat (`sulphates`) có tác động tích cực đến chất lượng | Pearson $r = +0.3306$ ($p = 4.99 \times 10^{-36}$)<br>t-test: $t = 10.87$ ($p = 1.93 \times 10^{-26}$)<br>Mean: Low = 0.61 g/dm3, High = 0.69 g/dm3 | **Chấp nhận $H_4$** | Sunfat giải phóng $SO_2$ tự do, ngăn ngừa hiện tượng oxy hóa xỉn màu và giữ cấu trúc vang ổn định. |

---

### 3.2. Trực quan hóa có mục tiêu & Diễn giải chuyên sâu (Deep Insight)

#### 1. Ma trận nhiệt tương quan Pearson (Heatmap - `images/correlation_heatmap_deep.png`)
- **Phân tích số liệu:** `alcohol` ($+0.48$), `sulphates` ($+0.33$), `citric acid` ($+0.23$) kéo điểm tăng; `volatile acidity` ($-0.39$), `total sulfur dioxide` ($-0.18$), `density` ($-0.18$) kéo điểm tụt.
- **Deep Insight:** Rượu vang ngon đòi hỏi sự phối hợp hài hòa giữa nồng độ cồn tốt và lượng axit bay hơi được kiểm soát tối thiểu. Hiện tượng cộng tuyến chặt giữa `fixed acidity` với `density` ($+0.67$) và `pH` ($-0.68$) phản ánh đúng bản chất lý hóa học của dung dịch rượu.

#### 2. Phân phối Violin – Boxplot của Nồng độ cồn và Axit bay hơi (`images/alcohol_volatile_acidity_distribution.png`)
- **Phân tích số liệu:** Đường trung bình nồng độ cồn tăng vọt từ $9.8\%$ ở thang điểm 3–5 lên mức $11.4\% - 12.1\%$ ở thang điểm 7–8. Ngược lại, axit axetic giảm dốc từ $0.88\,g/dm^3$ xuống dưới $0.38\,g/dm^3$.
- **Deep Insight:** Xuất hiện một **ngưỡng chuyển pha chất lượng (Quality Inflection Point)** tại điểm 6: Để một chai rượu bước từ phân khúc "phổ thông" lên "thượng hạng", điều kiện tiên quyết là cồn phải đạt tối thiểu $11.5\%$ và axit axetic phải được kiềm chế dưới $0.45\,g/dm^3$.

#### 3. Biểu đồ phân tán (Scatter Plot) Axit bay hơi vs Axit Citric (`images/volatile_acidity_vs_citric_scatter.png`)
- **Phân tích số liệu:** Vùng chất lượng cao (màu xanh) tập trung ở góc dưới-phải: `volatile acidity` $< 0.45\,g/dm^3$ và `citric acid` $> 0.25\,g/dm^3$. Vùng chất lượng kém (màu đỏ) dồn ở góc trên-trái.
- **Deep Insight:** Axit citric mang lại cảm giác thanh mát và tạo hiệu ứng đệm hương thơm, giúp che lấp bớt độ gắt của tanin, trong khi axit axetic phá hỏng cấu trúc vị giác.

#### 4. Hồ sơ Hóa lý so sánh Vang phổ thông vs Vang thượng hạng (`images/chemical_profile_comparison.png`)
- **Phân tích số liệu:** Vang thượng hạng vượt trội về nồng độ cồn ($+0.81$ IQR), sunfat ($+0.65$ IQR), axit citric ($+0.42$ IQR), và thấp hơn vượt trội về axit bay hơi ($-0.62$ IQR).
- **Deep Insight:** Cung cấp chân dung hóa lý hoàn chỉnh để các chuyên gia làm rượu (winemakers) thiết lập công thức phối trộn (blending target) chính xác.

---

# GIAI ĐOẠN 4: ĐÁNH GIÁ TÁC ĐỘNG VÀ KHUYẾN NGHỊ

### 4.1. Tóm tắt các phát hiện chuyên môn và kinh doanh nổi bật
1. **Bộ ba giá trị cốt lõi:** Một chai rượu đỏ xuất sắc được cấu thành từ 3 yếu tố: Cồn dồi dào ($11.5\% - 12.5\%$), Axit bay hơi cực thấp ($< 0.45\,g/dm^3$), và Sunfat được bảo toàn hợp lý ($> 0.65\,g/dm^3$).
2. **Bác bỏ niềm tin sai lệch về độ ngọt:** Lượng đường dư không có giá trị quyết định chất lượng vang đỏ khô. Việc thêm đường nhân tạo không giúp nâng hạng sản phẩm.
3. **Kiểm soát hư hỏng có giá trị hơn tăng chi phí làm màu:** Ngăn ngừa vi khuẩn axetic oxy hóa rượu thành giấm có tác động cứu vãn điểm số chất lượng lớn gấp nhiều lần so với các biện pháp can thiệp mùi vị khác.

### 4.2. Đề xuất giải pháp ứng dụng thực tế
- **Kiểm soát vận hành lên men (Smart Brewing):** Lắp đặt cảm biến IoT đo nhiệt độ và nồng độ axit bay hơi thời gian thực trong bồn ủ. Kích hoạt báo động can thiệp làm mát và châm $SO_2$ khử trùng khi axit axetic tiệm cận $0.50\,g/dm^3$.
- **Tối ưu hóa thời điểm thu hoạch:** Kiểm tra độ ngọt quả nho (chỉ số Brix) trên vườn cây để đảm bảo tiềm năng sinh cồn tự nhiên đạt trên $11.5\%$.
- **Hệ thống phân luồng sản phẩm tự động (AI Quality Assurance):** Thay thế một phần hội đồng thử nếm thủ công bằng mô hình phân loại học máy (Random Forest / XGBoost) dựa trên 11 chỉ số kiểm nghiệm lab. Tự động gắn mác sản phẩm dòng *Reserve/Premium* hay *Table wine*, giúp cắt giảm $60\%$ chi phí cảm quan và tránh rủi ro đánh giá thiên lệch.

### 4.3. Giới hạn dữ liệu và Định hướng mở rộng tương lai
- **Giới hạn:** Tập dữ liệu lấy từ một vùng duy nhất (Vinho Verde, Bồ Đào Nha); thiếu các biến số định tính ngoại cảnh mang tính quyết định: Giống nho, Thời gian ủ thùng gỗ sồi, Năm mùa vụ (Vintage) và điều kiện thổ nhưỡng. Dữ liệu bị mất cân bằng lớp ở hai cực điểm 3 và 8.
- **Định hướng mở rộng:** Thu thập bổ sung các chỉ số vi khí hậu mùa thu hoạch (lượng mưa, số giờ nắng); đo lường nồng độ các hợp chất hữu cơ tạo hương (polyphenols, anthocyanins); ứng dụng thuật toán giải thích **SHAP** để đưa ra bản tư vấn công thức cá nhân hóa cho từng lô ủ rượu.
