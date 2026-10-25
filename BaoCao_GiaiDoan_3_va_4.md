# BÁO CÁO CHI TIẾT: GIAI ĐOẠN 3 & GIAI ĐOẠN 4
**Đề tài:** Phân tích Dữ liệu Hóa lý & Chất lượng Rượu vang Đỏ (*Red Wine Quality*)  
**Tập dữ liệu đã làm sạch:** `winequality-red-cleaned.csv` (1,359 mẫu quan sát duy nhất, 12 thuộc tính gốc + 1 nhãn nhị phân + 11 đặc trưng RobustScaled)

---

## MỤC LỤC
1. [GIAI ĐOẠN 3: PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU](#giai-đoạn-3-phân-tích-và-trực-quan-hóa-dữ-liệu)
   - 1.1. Thiết lập và Kiểm định các Giả thuyết Thống kê ($H_1, H_2, H_3, H_4$)
   - 1.2. Trực quan hóa có mục tiêu và Diễn giải chuyên sâu (Deep Insight)
     - *Biểu đồ 1:* Ma trận nhiệt tương quan Pearson đa biến
     - *Biểu đồ 2:* Phân phối kết hợp Violin – Boxplot của Nồng độ cồn và Axit bay hơi
     - *Biểu đồ 3:* Biểu đồ phân tán (Scatter Plot) xác định ranh giới hóa lý
     - *Biểu đồ 4:* Hồ sơ so sánh đa đặc trưng giữa Rượu phổ thông và Rượu thượng hạng
2. [GIAI ĐOẠN 4: ĐÁNH GIÁ TÁC ĐỘNG VÀ KHUYẾN NGHỊ](#giai-đoạn-4-đánh-giá-tác-động-và-khuyến-nghị)
   - 2.1. Tóm tắt các phát hiện chuyên môn và kinh doanh nổi bật
   - 2.2. Đề xuất giải pháp ứng dụng thực tế trong sản xuất và phân phối
   - 2.3. Nhận diện giới hạn dữ liệu và Định hướng mở rộng tương lai

---

# GIAI ĐOẠN 3: PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU

### 1.1. Thiết lập và Kiểm định các Giả thuyết Thống kê

Nhóm phân tích thiết lập 4 giả thuyết chính để đối chiếu giả định ban đầu với thực tế số liệu trên 1,359 mẫu rượu đã làm sạch:

#### Giả thuyết $H_1$: Nồng độ cồn (`alcohol`) tỉ lệ thuận với chất lượng rượu (`quality`)
- **Giả định ban đầu:** Rượu có độ cồn cao hơn tạo cảm giác dày dặn trong vòm miệng ("full-bodied"), giữ hương este thơm lâu hơn, do đó được chuyên gia đánh giá điểm cao hơn.
- **Thực hiện kiểm định:**
  - *Hệ số tương quan Pearson:* $r = +0.4827$, $p\text{-value} = 3.03 \times 10^{-80}$ ($p < 0.001$).
  - *Kiểm định Independent Two-sample t-test* giữa nhóm Rượu kém/trung bình (Quality $< 6$) và nhóm Rượu ngon (Quality $\ge 6$):
    - Trung bình nhóm $< 6$: $\mu_1 = 9.92\%$
    - Trung bình nhóm $\ge 6$: $\mu_2 = 10.88\%$
    - Giá trị thống kê $t = 18.55$, $p\text{-value} = 1.27 \times 10^{-68}$.
  - *Kiểm định Phân tích phương sai một yếu tố (One-way ANOVA)* trên cả 6 thang điểm (3, 4, 5, 6, 7, 8):
    - Giá trị kiểm định $F = 105.04$, $p\text{-value} = 8.59 \times 10^{-94}$.
- **Kết luận:** **Chấp nhận giả thuyết $H_1$**. Sự khác biệt về nồng độ cồn giữa các nhóm chất lượng mang ý nghĩa thống kê cực kỳ mạnh mẽ. Độ cồn là yếu tố đơn lẻ tác động tích cực lớn nhất đến điểm cảm quan.

---

#### Giả thuyết $H_2$: Axit dễ bay hơi (`volatile acidity`) làm suy giảm nghiêm trọng phẩm chất của rượu
- **Giả định ban đầu:** Axit dễ bay hơi chủ yếu là axit axetic sinh ra do vi khuẩn axetic oxy hóa rượu thành giấm chua hỏng. Mùi giấm chua hắc sẽ phá hỏng hương thơm tự nhiên của nho.
- **Thực hiện kiểm định:**
  - *Hệ số tương quan Pearson:* $r = -0.3921$, $p\text{-value} = 3.49 \times 10^{-51}$ ($p < 0.001$).
  - *Kiểm định Two-sample t-test:*
    - Trung bình nhóm Kém/TB ($<6$): $\mu_1 = 0.59\,g/dm^3$
    - Trung bình nhóm Ngon ($\ge 6$): $\mu_2 = 0.47\,g/dm^3$
    - Giá trị thống kê $t = -12.80$, $p\text{-value} = 1.63 \times 10^{-35}$.
- **Kết luận:** **Chấp nhận giả thuyết $H_2$**. Axit axetic là chỉ số tương quan âm mạnh nhất. Bất kỳ mẫu rượu nào có hàm lượng axit bay hơi vượt ngưỡng đều bị chuyên gia đánh tụt điểm.

---

#### Giả thuyết $H_3$: Lượng đường dư (`residual sugar`) quyết định mức độ thơm ngon của rượu vang đỏ
- **Giả định ban đầu:** Vang đỏ ngọt hơn (nhiều đường dư hơn) sẽ dễ uống và được người nếm thử ưa chuộng hơn.
- **Thực hiện kiểm định:**
  - *Hệ số tương quan Pearson:* $r = +0.0191$, $p\text{-value} = 0.481 > 0.05$.
  - *Kiểm định Two-sample t-test:*
    - Trung bình nhóm Kém/TB ($<6$): $\mu_1 = 2.33\,g/dm^3$
    - Trung bình nhóm Ngon ($\ge 6$): $\mu_2 = 2.32\,g/dm^3$
    - Giá trị thống kê $t = -0.1902$, $p\text{-value} = 0.849 > 0.05$.
- **Kết luận:** **Bác bỏ hoàn toàn giả thuyết $H_3$**. 
  - $p\text{-value} = 0.481$ vượt xa ngưỡng ý nghĩa $\alpha = 0.05$, chứng tỏ không có mối liên hệ tuyến tính nào giữa lượng đường dư và điểm chất lượng. 
  - Vang đỏ là dòng vang khô (Dry Red Wine), sự tinh tế nằm ở cấu trúc tanin và tính cân bằng axit - cồn, chứ không nằm ở vị ngọt đường.

---

#### Giả thuyết $H_4$: Hàm lượng Sunfat (`sulphates`) đóng vai trò bảo tồn hương vị và hỗ trợ nâng cao chất lượng
- **Giả định ban đầu:** Sunfat (kali sunfat) là phụ gia giúp giải phóng $SO_2$ tự do, ngăn chặn hiện tượng oxy hóa xỉn màu và chống nhiễm khuẩn mốc.
- **Thực hiện kiểm định:**
  - *Hệ số tương quan Pearson:* $r = +0.3306$, $p\text{-value} = 4.99 \times 10^{-36}$ ($p < 0.001$).
  - *Kiểm định Two-sample t-test:*
    - Trung bình nhóm Kém/TB: $\mu_1 = 0.61\,g/dm^3$
    - Trung bình nhóm Ngon: $\mu_2 = 0.69\,g/dm^3$
    - Giá trị thống kê $t = 10.87$, $p\text{-value} = 1.93 \times 10^{-26}$.
- **Kết luận:** **Chấp nhận giả thuyết $H_4$**. Việc duy trì mức sunfat ổn định giúp bảo quản tốt phẩm chất của rượu.

---

### 1.2. Trực quan hóa có mục tiêu & Diễn giải chuyên sâu (Deep Insight)

#### Biểu đồ 1: Ma trận nhiệt tương quan Pearson đa biến (`images/correlation_heatmap_deep.png`)
- **Loại biểu đồ:** Heatmap ma trận tam giác dưới, hiển thị hệ số tương quan màu phân cực (Diverging palette).
- **Phân tích số liệu:**
  1. *Nhóm tác động tích cực đến Quality:* `alcohol` ($+0.48$), `sulphates` ($+0.33$), `citric acid` ($+0.23$), `fixed acidity` ($+0.12$).
  2. *Nhóm tác động tiêu cực đến Quality:* `volatile acidity` ($-0.39$), `total sulfur dioxide` ($-0.18$), `density` ($-0.18$), `chlorides` ($-0.13$).
  3. *Tương quan cộng tuyến giữa các chỉ số độc lập:*
     - `fixed acidity` tương quan rất cao với `citric acid` ($r = +0.67$) và `density` ($r = +0.67$), nhưng tỉ lệ nghịch với `pH` ($r = -0.68$).
     - `free sulfur dioxide` và `total sulfur dioxide` đồng biến chặt chẽ ($r = +0.67$).
- **Deep Insight (Nhận định chuyên sâu):**
  - Rượu vang ngon đòi hỏi sự kết hợp đồng thời của **3 trụ cột hóa học**: Nồng độ cồn tốt ($> 11\%$), nồng độ axit bay hơi cực thấp ($< 0.5\,g/dm^3$), và được bảo vệ bởi lượng sunfat tối ưu ($> 0.65\,g/dm^3$).
  - Hiện tượng đa cộng tuyến giữa `fixed acidity`, `density` và `pH` phản ánh chuẩn xác các quy luật nhiệt động lực học và dung dịch đệm trong hóa học. Khi áp dụng mô hình hồi quy tuyến tính (Linear Regression), cần phải xem xét hiện tượng VIF (Variance Inflation Factor) hoặc ưu tiên các mô hình cây quyết định (Random Forest, XGBoost) vốn miễn nhiễm với đa cộng tuyến.

---

#### Biểu đồ 2: Phân phối Violin kết hợp Boxplot cho Alcohol & Volatile Acidity (`images/alcohol_volatile_acidity_distribution.png`)
- **Loại biểu đồ:** Violin plot thể hiện mật độ xác suất kết hợp lõi Boxplot và đường nối giá trị trung bình qua các thang điểm từ 3 đến 8.
- **Phân tích số liệu:**
  - *Với Alcohol:*
    - Điểm 3, 4, 5: Đường trung bình nằm ngang ở mức thấp ($9.8\% - 10.1\%$), phần "bụng" phình to của violin tập trung ở vùng $9.5\%$.
    - Điểm 6, 7, 8: Đường trung bình dốc đứng đi lên ($10.6\% \rightarrow 11.4\% \rightarrow 12.1\%$). Ở điểm 8, phân phối rượu có nồng độ cồn dồn toàn bộ lên vùng trên $11.5\%$.
  - *Với Volatile Acidity:*
    - Điểm 3 có trung bình axit axetic lên tới gần $0.9\,g/dm^3$.
    - Khi điểm chất lượng tăng lên 7 và 8, trung bình axit bay hơi giảm tuần tự xuống dưới $0.4\,g/dm^3$ và $0.38\,g/dm^3$.
- **Deep Insight (Nhận định chuyên sâu):**
  - Tồn tại một **ngưỡng chuyển giao chất lượng (Quality Inflection Point)** ở mức điểm 6. Rượu muốn vượt qua ngưỡng "bình dân" (điểm 5) để bước vào phân khúc "thượng hạng" (điểm 7, 8) bắt buộc phải đạt được bước nhảy vọt về nồng độ cồn ($\ge 11\%$) và kiểm soát axit axetic dưới $0.45\,g/dm^3$.

---

#### Biểu đồ 3: Phân tán (Scatter Plot) giữa Axit bay hơi và Axit Citric (`images/volatile_acidity_vs_citric_scatter.png`)
- **Loại biểu đồ:** Scatter Plot với hai màu đối lập phân loại chất lượng rượu và các đường giới hạn phân vùng kỹ thuật.
- **Phân tích số liệu:**
  - Vùng nguy hiểm (Góc trên - trái): `volatile acidity` $> 0.5\,g/dm^3$ và `citric acid` $< 0.1\,g/dm^3$ bị chiếm lĩnh áp đảo bởi các dấu 'X' màu đỏ (chất lượng kém/trung bình).
  - Vùng xuất sắc (Góc dưới - phải): `volatile acidity` $< 0.4\,g/dm^3$ và `citric acid` $> 0.25\,g/dm^3$ là nơi quần tụ của đại đa số các điểm tròn màu xanh (rượu chất lượng cao).
- **Deep Insight (Nhận định chuyên sâu):**
  - Axit citric đóng vai trò là "chất bù trừ vị giác". Sự xuất hiện của axit citric mang lại vị chua tươi mát của cam quýt, giúp nâng tầm trải nghiệm của người uống. Ngược lại, nếu thiếu vắng axit citric mà axit axetic lại cao, rượu sẽ mang mùi hăng nồng của giấm ăn pha loãng.

---

#### Biểu đồ 4: So sánh Hồ sơ Đặc trưng Hóa lý chuẩn hóa (`images/chemical_profile_comparison.png`)
- **Loại biểu đồ:** Grouped Bar Chart so sánh giá trị vị trí trung vị sau chuẩn hóa (`RobustScaled`) giữa nhóm Vang phổ thông (Điểm 3–5) và Vang thượng hạng (Điểm 7–8).
- **Phân tích số liệu:**
  - Điểm lệch vị trí giữa 2 phân khúc:
    - `alcohol`: Vang thượng hạng vượt trội $+0.81$ đơn vị IQR so với mức $-0.19$ của vang phổ thông.
    - `citric acid`: Vang thượng hạng đạt $+0.42$ đơn vị IQR, trong khi vang phổ thông là $-0.09$.
    - `sulphates`: Vang thượng hạng đạt $+0.65$ đơn vị IQR, trong khi vang phổ thông là $-0.22$.
    - `volatile acidity`: Vang thượng hạng giảm sâu xuống $-0.62$ đơn vị IQR, trong khi vang phổ thông ở mức $+0.24$.
- **Deep Insight (Nhận định chuyên sâu):**
  - Biểu đồ này cung cấp chính xác **chân dung kỹ thuật (Technical DNA Profile)** của một chai vang đỏ cao cấp: Được kích hoạt mạnh mẽ bởi bộ ba Cồn - Axit Citric - Sunfat, và triệt tiêu tối đa Axit axetic.

---

# GIAI ĐOẠN 4: ĐÁNH GIÁ TÁC ĐỘNG VÀ KHUYẾN NGHỊ

### 2.1. Tóm tắt các phát hiện chuyên môn và kinh doanh nổi bật

1. **Độ cồn không phải là "ngẫu nhiên", mà là thước đo của mùa vụ và quy trình lên men:** Nồng độ cồn cao trong vang đỏ phản ánh quả nho nguyên liệu thu hoạch đúng độ chín sinh học (tích tụ đủ đường tự nhiên) và chủng men hoạt động triệt để. Rượu có độ cồn cao hơn luôn chiếm ưu thế vượt trội trong cảm nhận của các chuyên gia.
2. **Kẻ thù số 1 là vi khuẩn axetic:** Axit dễ bay hơi (`volatile acidity`) là tác nhân hàng đầu phá hủy mẻ rượu. Điểm nếm thử giảm tuyến tính rất dốc khi chỉ số này tăng lên.
3. **Phá vỡ định kiến về "Độ ngọt":** Lượng đường dư (`residual sugar`) hoàn toàn không đóng góp vào việc nâng cao điểm đánh giá đối với vang đỏ khô. Việc cố tình giữ lại đường hoặc pha thêm ngọt nhân tạo không giúp sản phẩm bán được giá cao hơn ở phân khúc chuyên nghiệp.
4. **Hiệu ứng che chắn của Sunfat:** Hàm lượng sunfat đóng vai trò như chiếc "khiên bảo vệ", giúp vang không bị chua hóa trong thời gian ủ và đóng chai.

---

### 2.2. Đề xuất giải pháp mang tính ứng dụng thực tế

#### A. Tối ưu hóa trong quy trình sản xuất và chế biến (Operations & Brewing)
- **Lắp đặt cảm biến IoT giám sát liên tục (Real-time Fermentation Monitoring):**
  - Đo đạc tự động chỉ số axit dễ bay hơi và nhiệt độ thùng ủ.
  - Thiết lập hệ thống cảnh báo tự động: Khi `volatile acidity` chạm ngưỡng $0.50\,g/dm^3$, lập tức kích hoạt biện pháp giảm nhiệt độ làm chậm tốc độ vi sinh và bổ sung liều lượng $SO_2$ hợp chuẩn để triệt tiêu vi khuẩn lên men giấm.
- **Tiêu chuẩn hóa nguyên liệu đầu vào:**
  - Lựa chọn thời điểm hái nho có độ Brix (độ đường tự nhiên) đủ cao để đảm bảo tiềm năng sinh cồn đạt tối thiểu $11.5\% - 12.0\% vol$.
  - Cân nhắc phối trộn (blending) các mẻ vang có lượng axit citric dồi dào để nâng cao độ tươi và cải thiện điểm đánh giá tổng thể.

#### B. Chiến lược phân luồng sản phẩm và Tối ưu chi phí (Quality Assurance & Business)
- **Hệ thống phân hạng chất lượng tự động bằng Machine Learning (AI-powered QA):**
  - *Vấn đề hiện tại:* Thuê hội đồng chuyên gia sommelier nếm thử thủ công từng lô rượu rất tốn kém chi phí, mất thời gian và mang tính chủ quan.
  - *Giải pháp:* Huấn luyện mô hình phân loại (Random Forest hoặc XGBoost) trên tập 11 chỉ số xét nghiệm lab. Mô hình có thể dự báo với độ chính xác cao xác suất một mẻ rượu đạt chuẩn "Thượng hạng" (Quality $\ge 7$) hay "Phổ thông" (Quality $\le 5$).
  - *Ứng dụng thương mại:* Tự động định hướng phân luồng đóng chai, dán nhãn dòng Premium/Reserve hoặc dòng phổ thông (Table wine) ngay tại nhà máy, giúp doanh nghiệp tối đa hóa doanh thu trên từng mẻ ủ.

---

### 2.3. Nhận diện giới hạn dữ liệu và Định hướng mở rộng tương lai

#### A. Các giới hạn của tập dữ liệu hiện tại
1. **Thiếu biến số định tính quan trọng:** 
   - Dữ liệu hoàn toàn là các biến hóa lý trong phòng thí nghiệm; thiếu vắng các thông tin ngoại cảnh có ảnh hưởng quyết định đến giá trị vang như: **Giống nho** (Cabernet Sauvignon, Merlot, Pinot Noir), **Năm thu hoạch (Vintage)**, **Thời gian ủ trong thùng gỗ sồi (Oak Aging)**, và **Vùng thổ nhưỡng (Terroir)**.
2. **Thiên lệch địa lý (Geographical Bias):** 
   - Toàn bộ 1,599 mẫu được lấy từ vùng Minho (Bồ Đào Nha). Do đặc tính khí hậu địa phương, các phát hiện này chưa chắc đã khái quát hóa hoàn toàn cho các vùng khí hậu khác (như vùng khô nóng Bordeaux hay Nam Úc).
3. **Mất cân bằng nhãn (Class Imbalance):**
   - Hơn $82\%$ mẫu dữ liệu nằm ở điểm 5 và 6. Các mẫu đặc biệt dở (điểm 3: 10 mẫu) và cực kỳ xuất sắc (điểm 8: 18 mẫu) chiếm tỷ lệ quá nhỏ, gây khó khăn cho việc huấn luyện mô hình nhận diện các mẻ rượu kiệt xuất.

#### B. Định hướng nghiên cứu và Mở rộng trong tương lai
- **Làm giàu dữ liệu (Data Enrichment):**
  - Thu thập thêm biến số về khí hậu mùa vụ (lượng mưa trung bình, biên độ nhiệt ngày đêm, số giờ nắng trong năm thu hoạch).
  - Bổ sung thông số quang phổ huỳnh quang hoặc phân tích sắc ký khí (Gas Chromatography) để định lượng chính xác các hợp chất tạo mùi thơm phức tạp (terpenes, pyrazines, polyphenols).
- **Nâng cao năng lực mô hình học máy:**
  - Thử nghiệm các kiến trúc Ensemble Learning (CatBoost, LightGBM) kết hợp kỹ thuật cân bằng dữ liệu nâng cao (SMOTE-NC, Cost-Sensitive Learning).
  - Ứng dụng **SHAP (SHapley Additive exPlanations)** để giải thích độ đóng góp chi tiết của từng thuộc tính hóa học cho từng chai rượu cụ thể, cung cấp bản khuyến nghị cá nhân hóa cho từng mẻ ủ.
