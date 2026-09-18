# Reflection — Đinh Trường An

## 1. Phần việc đã làm

Mình phụ trách kiểm tra và cải thiện evaluator cho hệ thống phát hiện văn phong AI/dịch máy trong kịch bản tiếng Việt. Mình đã đọc lại `test-log.md`, kiểm tra các commit và sửa phần chấm span để không tính sai finding rỗng hoặc span bao trùm cả câu. Mình cũng tham gia thêm rule layer để bắt các tín hiệu có thể kiểm chứng như page reference, markdown, acronym, code-switch, số liệu và repetition.

Kết quả tốt nhất đạt được là recall strict 20/20 (100%), false positive trên tập sạch bằng 0 và Evidence Gate Drops bằng 0. Đồng thời, mình kiểm tra regression no-flag và ghi nhận rằng no-flag mới đạt 2/7, nên không dùng riêng con số recall 100% để kết luận hệ thống đã hoàn thiện.

Ngoài ra, mình chuẩn bị prompt và một bộ 20 testcase recall mới, bao phủ translationese, repetition, code-switch, claim số liệu, tham chiếu trang/hình, nguyên câu tiếng Anh và thuật ngữ kỹ thuật.

## 2. Quyết định nhóm mình không đồng ý nhưng vẫn theo

Mình không đồng ý với việc chỉ dùng recall 100% làm chỉ số chính để đánh giá chất lượng, vì rule layer có thể làm tăng false positive trên các câu nói tự nhiên. Tuy vậy, mình vẫn theo hướng giữ recall cao vì đây là yêu cầu quan trọng của bài toán và đã ghi rõ no-flag là regression bắt buộc phải xử lý tiếp.

Mình cũng không muốn nới lỏng luật chấm span để giữ số đẹp. Nhóm thống nhất dùng evidence gate và ratio guard nghiêm ngặt, dù kết quả recall có thể thấp hơn các lượt chạy cũ.

## 3. Nếu làm lại từ đầu

Mình sẽ thiết kế golden set gồm cả positive case và no-flag case ngay từ đầu, đồng thời tách rõ các lỗi chắc chắn có thể bắt bằng rule khỏi các lỗi cần LLM đánh giá ngữ nghĩa. Mỗi lần thay đổi prompt hoặc rule sẽ chạy đủ recall, false positive, no-flag và các case hành vi thay vì chỉ chạy một chỉ số.

Mình cũng sẽ chuẩn bị môi trường chạy và kiểm tra kết nối API trước khi bắt đầu benchmark, đồng thời lưu riêng report của từng lượt để việc so sánh giữa các commit minh bạch hơn.
