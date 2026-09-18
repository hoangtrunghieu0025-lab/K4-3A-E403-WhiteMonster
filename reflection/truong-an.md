# Reflection — Đinh Trường An

## 1. Phần việc đã làm

Mình phụ trách kiểm tra và cải thiện evaluator cho hệ thống phát hiện văn phong AI/dịch máy trong kịch bản tiếng Việt. Mình đã đọc lại `test-log.md`, kiểm tra các commit và sửa phần chấm span để không tính sai finding rỗng hoặc span bao trùm cả câu. Mình cũng tham gia thêm rule layer để bắt các tín hiệu có thể kiểm chứng như page reference, markdown, acronym, code-switch, số liệu và repetition.

Kết quả tốt nhất đạt được là recall strict 20/20 (100%), false positive trên tập sạch bằng 0 và Evidence Gate Drops bằng 0. Đồng thời, mình kiểm tra regression no-flag và ghi nhận rằng no-flag mới đạt 2/7, nên không dùng riêng con số recall 100% để kết luận hệ thống đã hoàn thiện.

Ngoài ra, mình chuẩn bị prompt và một bộ 20 testcase recall mới, bao phủ translationese, repetition, code-switch, claim số liệu, tham chiếu trang/hình, nguyên câu tiếng Anh và thuật ngữ kỹ thuật.

Trong quá trình làm, mình cũng kiểm tra lại lịch sử commit và đối chiếu các kết quả trong `evaluation_report` với `test-log.md`. Việc này giúp phân biệt kết quả chạy thật với những lượt chạy dùng logic chấm cũ. Mình đặc biệt chú ý hai lỗi có thể làm recall bị thổi phồng: span rỗng vẫn được coi là hợp lệ và span trả về quá dài vẫn được tính là khớp. Sau khi thêm kiểm tra span không rỗng và ratio guard, kết quả được đánh giá nghiêm ngặt hơn.

Mình đã ghi nhận rõ trade-off của rule layer. Rule layer giúp bắt đủ các pattern dễ kiểm chứng và đưa recall strict lên 20/20, nhưng có nguy cơ gắn cờ oan cho câu nói tự nhiên. Vì vậy mình không chỉ báo cáo con số 100%, mà còn kiểm tra no-flag và ghi lại các case regression để nhóm có hướng sửa tiếp bằng verifier.

Về quy trình làm việc, mình đã chuẩn bị prompt test riêng thay vì chỉ dùng lại các testcase phổ biến. Bộ prompt mới cố tình bao phủ nhiều dạng lỗi và có thể dùng để kiểm tra khả năng tổng quát hóa của evaluator.

## 2. Quyết định nhóm mình không đồng ý nhưng vẫn theo

Mình không đồng ý với việc chỉ dùng recall 100% làm chỉ số chính để đánh giá chất lượng, vì rule layer có thể làm tăng false positive trên các câu nói tự nhiên. Tuy vậy, mình vẫn theo hướng giữ recall cao vì đây là yêu cầu quan trọng của bài toán và đã ghi rõ no-flag là regression bắt buộc phải xử lý tiếp.

Mình cũng không muốn nới lỏng luật chấm span để giữ số đẹp. Nhóm thống nhất dùng evidence gate và ratio guard nghiêm ngặt, dù kết quả recall có thể thấp hơn các lượt chạy cũ.

Mình không đồng ý với việc coi một lần chạy thành công là bằng chứng hệ thống đã ổn định. Kết quả phụ thuộc model, thời điểm gọi API và chất lượng input, nên cần lưu report theo từng lượt và ghi rõ model, logic chấm, số case và các lỗi còn tồn tại. Tuy nhiên, mình vẫn theo quy trình chung của nhóm để mọi người có cùng một baseline và dễ so sánh giữa các commit.

## 3. Nếu làm lại từ đầu

Mình sẽ thiết kế golden set gồm cả positive case và no-flag case ngay từ đầu, đồng thời tách rõ các lỗi chắc chắn có thể bắt bằng rule khỏi các lỗi cần LLM đánh giá ngữ nghĩa. Mỗi lần thay đổi prompt hoặc rule sẽ chạy đủ recall, false positive, no-flag và các case hành vi thay vì chỉ chạy một chỉ số.

Mình cũng sẽ chuẩn bị môi trường chạy và kiểm tra kết nối API trước khi bắt đầu benchmark, đồng thời lưu riêng report của từng lượt để việc so sánh giữa các commit minh bạch hơn.

Mình sẽ thiết kế thêm các cặp testcase đối chứng: một câu có cấu trúc gần giống nhau nhưng một câu thật sự lỗi và một câu hoàn toàn tự nhiên. Cách này giúp đo được hệ thống có phân biệt được lỗi thật với tín hiệu bề mặt hay không. Mình cũng sẽ tách metric theo từng category thay vì chỉ nhìn recall tổng, vì một rule có thể bắt tốt page reference nhưng làm xấu translationese hoặc repetition.

Cuối cùng, mình sẽ đưa verifier vào sau bước sinh finding cho các category dễ gây false positive. Verifier chỉ giữ finding khi model chỉ ra được bằng chứng cụ thể trong span; nếu không có bằng chứng thì loại finding. Mọi thay đổi vẫn phải chạy lại đầy đủ recall, clean false positive, no-flag và các case hành vi trước khi merge.
