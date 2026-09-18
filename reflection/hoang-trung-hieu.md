# Reflection — Hoàng Trung Hiếu (2A202602945)

## Vai trò & phân công

Đội trưởng, phụ trách "Spec + điều phối" theo `spec.md` §8: §1 problem statement, §2 bảng impact, §4 lát cắt & non-goals, nộp form cả 5 mốc, dựng `demo-slides.pdf`, mở đầu thuyết trình CP6.

## Việc mình thực sự đã làm

Đúng phần được phân công (§1/§2/§4, canvas, nộp mốc), nhưng thực tế lấn sâu hơn hẳn vào phần "prompt + eval" của An — vì đó là chỗ tắc nghẽn nhất của cả nhóm trong 2 ngày qua. Cụ thể mình đứng tên commit (kèm Claude hỗ trợ) cho toàn bộ chuỗi Lượt 3 đến Lượt 16 của `eval/run_eval.py`: từ lần đầu chạy đủ 39 case (Lượt 3, recall 45%), vá `SYSTEM_PROMPT` liên tiếp (Lượt 4-7, đẩy recall lên 80-95%), phát hiện và tự tay sửa 2 lỗi chấm điểm nghiêm trọng làm thổi phồng recall suốt Lượt 3-7 (Lượt 8, sau khi Duy phát hiện), sửa quy trình test S1/S2 (Lượt 8-9), và cả buổi sáng nay (18/9, ngày CP5) đọc lại đúng tài liệu đề gốc (`mau-kich-ban.md`, `track-c-lesson-studio.md`) để tìm ý tưởng sửa prompt, thêm `temperature=0` sau khi phát hiện số liệu dao động ngẫu nhiên, và dựng 2 file mẫu validation cho Thái/Sơn. Cũng là người vá 1 bug hạ tầng (`912bdf2` — key OpenAI bị route nhầm sang OpenRouter làm mọi lượt eval fail 401).

## AI hỗ trợ thế nào

Gần như mọi commit eval của mình đều làm cùng Claude — không phải kiểu "AI viết hộ code rồi mình dán vào", mà theo quy trình: mình mô tả hiện tượng/số liệu quan sát được → Claude đọc code/log để tìm nguyên nhân → cả hai cùng quyết định sửa gì → chạy thử → đọc kết quả cùng nhau trước khi ghi vào spec. Việc quan trọng nhất Claude giúp là **giữ kỷ luật đo lường**: mỗi lần mình muốn tin ngay vào một con số đẹp (vd Lượt 12 báo A3 "PASS lần đầu tiên"), Claude luôn nhắc lại phải test lặp lại trước khi ghi vào spec — và đúng là lần đó hoá ra chỉ là may mắn của `temperature` ngẫu nhiên, phải đính chính lại ở Lượt 13. Quyết định nội dung, đánh giá "có nên tin số này không", và quyết định thời điểm dừng thử nghiệm để chốt (Lượt 16) vẫn là mình quyết, dựa trên trade-off đo được chứ không phải Claude tự quyết định.

## Quyết định mình không hoàn toàn đồng tình nhưng vẫn theo

Sáng nay (18/9), gần hạn CP5 13:00, mình dành phần lớn thời gian để tiếp tục vá `SYSTEM_PROMPT`/đo lại recall thay vì dựng `demo-slides.pdf` và video dự phòng trước — hai thứ mà rubric coi là điều kiện cứng để có 5 điểm CP5, còn eval score dù có tăng cũng không đổi được kết quả pass/fail của mốc này. Lý do mình vẫn làm: tối qua An báo con số "Gemini 70%" nhưng dùng logic chấm cũ (thiếu ratio guard, đã biết là logic lỗi từ Lượt 8), nếu không chốt lại số liệu trung thực trước thì rất dễ đưa nhầm số sai lên slide — mà rubric phạt nặng việc "trình bày số đẹp mà giấu quality bar". Đây là đánh đổi có cân nhắc, không phải trì hoãn vô cớ, nhưng nhìn lại thì có thể đã nên khoá số liệu sớm hơn (ví dụ dừng ở Lượt 13) để dành thời gian chắc chắn có slide/video trước, không nên để sát nút.

## Bài học từ case fail của chính nhóm

Case rõ nhất: **2 lỗi trong chính công cụ chấm điểm** (`_valid_span`/`_is_hit` thiếu kiểm tra span rỗng và giới hạn tỉ lệ kích thước) đã làm cả nhóm tin rằng recall đạt 85-95% suốt từ Lượt 3 đến Lượt 7 — một con số hoàn toàn sai, chỉ được phát hiện tình cờ bởi Duy tối 17/9. Sau khi sửa, recall thật chỉ còn 45%. Bài học không chỉ là "kiểm tra code cẩn thận hơn", mà cụ thể hơn: **công cụ đo bản thân nó cũng là một phần cần eval, không được mặc định nó đúng chỉ vì nó chạy không lỗi**. Sáng nay việc phát hiện thêm rằng thiếu `temperature=0` cũng gây ra ảo giác tương tự (một lượt "PASS lần đầu" hoá ra chỉ là may mắn ngẫu nhiên) cho thấy đây không phải sự cố một lần — là một loại rủi ro lặp lại nếu không thành thói quen kiểm chứng.

## Nếu làm lại từ đầu

Set `temperature=0` ngay từ Lượt 3, và viết `_valid_span()`/ratio-guard đúng ngay từ bản đầu tiên của `run_eval.py` thay vì để 5 lượt đo trên logic sai. Cả hai đều là những dòng code rất ngắn, không tốn công thêm nếu làm từ đầu, nhưng thiếu chúng đã khiến nhóm mất gần một ngày làm việc trên những con số ảo và phải đính chính nhiều lần.
