"""Spoken-Script QA — backend MVP.

Kiến trúc AI: WORKFLOW cố định, đúng 1 bước LLM, luật cứng ở hai đầu, người quyết cuối.

  ① [Luật]  Tách câu, gom khối ≤40 câu theo ranh giới đoạn
  ② [LLM]   Mỗi khối 1 lời gọi, chạy song song. Dùng NGUYÊN call_ai + SYSTEM_PROMPT + MODEL
            của eval/run_eval.py — bản demo chạy đúng thứ đã đo ở spec §7
  ③ [Luật]  Evidence Gate: span phải có nguyên văn trong khối, không có thì loại
  ④ [Người] Áp dụng / Sửa tay / Bỏ qua / Hoàn tác — mỗi quyết định ghi audit
  Nghe thử (TTS) chỉ chạy khi người duyệt bấm, để so câu gốc với bản sửa — không tham gia phát hiện lỗi:
  giọng máy đọc trơn cả câu dịch cứng (spec §1), nên nghe chỉ bắt được lỗi cách đọc số/viết tắt.
  "Xem chữ máy đọc": chép lại chính audio vừa nghe rồi so với chữ viết, chỉ ra máy đọc số/viết tắt thành gì.
  "So cách đọc": đo chỗ ngắt hơi, đoạn dài nhất không ngắt, tốc độ, độ lên xuống giọng của bản gốc và bản sửa.

Không ReAct, không tool: LLM chỉ trả JSON, không có quyền làm gì khác (spec §7, SEC1-SEC4).
Không lưu kịch bản (non-goal §4): trace.jsonl chỉ có số đếm, audit.jsonl chỉ có span đã quyết.

Chạy: python codebase/server.py  →  http://localhost:8000
"""
import base64
import bisect
import datetime
import difflib
import functools
import io
import json
import os
import re
import sys
import threading
import time
import unicodedata
import uuid
import warnings
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

import numpy as np
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "eval"))
from run_eval import MODEL, call_ai  # noqa: E402

CHUNK_SENTENCES = 40      # cỡ khối đã đo trong eval (clean_script 40 câu, 1 lời gọi)
LONG_SENTENCE_WORDS = 40  # mining §1: 19,1% câu nói thật dài hơn ngưỡng này mà vẫn xuôi
MAX_WORKERS = 4           # ponytail: cố định theo TPM tier thấp; call_ai đã tự retry 429
LOGS = ROOT / "logs"
# Giọng đọc và bước chép lại là hai model riêng: Piper đọc offline (không key, không 503),
# Gemini chỉ dùng để chép lại audio khi người duyệt bấm "Xem chữ máy đọc".
# Đã thử gemini-3.1-flash-tts-preview làm giọng đọc (17/9): ~8 giây mỗi câu, hay 503 — bỏ.
PIPER_VOICE = os.environ.get("PIPER_VOICE", str(ROOT / "models" / "vi_VN-vais1000-medium.onnx"))
# Piper gần như không ngừng giữa hai câu (đo 17/9: tách câu vẫn đọc liền); chèn lặng như `piper --sentence_silence`
PIPER_SENTENCE_SILENCE = float(os.environ.get("PIPER_SENTENCE_SILENCE", "0.3"))
# Tốc độ đọc → length_scale của Piper. Không tỉ lệ thuận với model này nên đặt theo số đo 17/9 trên 2 câu dài:
# 1.0 → ~5 tiếng/giây (giọng gốc) · 1.6 → ~4,1 · 2.0 → ~3,6.
SPEEDS = {"nhanh": 1.0, "vua": 1.6, "cham": 2.0}
# Giọng Piper tiếng Việt đọc từ tiếng Anh theo luật tiếng Việt ("cost-of-error" → "cát xê", "McKinsey" → "Mắc Kin Xi").
# Nhận ra từ tiếng Anh rồi đưa phiên âm tiếng Anh của espeak cho chính giọng Việt đọc: [[ kˈɔst ʌv ˈɛɹɚ ]].
# Từ tiếng Anh = chữ Latin không dấu mà không phải âm tiết Việt hợp lệ, hoặc có f/j/w/z, hoặc viết tắt in hoa 2–5 chữ.
VI_SYLLABLE = re.compile(r"(ngh|ng|gh|gi|kh|nh|ph|th|tr|ch|qu|[bcdghklmnpqrstvx])?[aeiouy]{1,3}(ch|ng|nh|[cmnptiouy])?")
ASCII_WORD = re.compile(r"(?<!\w)[A-Za-z]+(?!\w)")
PIPER_LOCK = threading.Lock()  # espeak giữ ngôn ngữ đang dùng ở trạng thái toàn cục: không cho hai lượt đọc chen nhau
VOICE_LABEL = f"piper {Path(PIPER_VOICE).stem}"
# Bản chuyên chép (gemini-3.5-transcribe) tự đổi "bảy mươi phần trăm" về "70%" nên không dùng được ở đây.
TRANSCRIBE_MODEL = os.environ.get("TRANSCRIBE_MODEL", "gemini-3.6-flash")
READBACK_PROMPT = ("Chép lại NGUYÊN VĂN từng tiếng được nói trong audio. Viết số, ký hiệu, viết tắt, tên riêng "
                   "đúng như được đọc thành lời (ví dụ 'bảy mươi phần trăm', 'ây ai'), không sửa, không giải thích.")
# Từ gồm chữ/số/ký hiệu, được nối bằng . / : - bên trong: "70%", "GPT-4o-mini", "example.com/a"; "AI." → "AI"
WORD = re.compile(r"[\w%$&#@+]+(?:[./:-][\w%$&#@+]+)*")

# Một câu kết thúc ở dấu câu đứng trước khoảng trắng/hết văn bản, hoặc ở cuối dòng.
# "2.5", "45,7%", "example.com" không bị cắt vì sau dấu chấm không có khoảng trắng.
SENTENCE = re.compile(r"\S.*?(?:[.!?…]+(?=\s|$)|(?=\n)|$)")


def split_sentences(script):
    return [m.span() for m in SENTENCE.finditer(script)]


def pack_chunks(script, sents, size=CHUNK_SENTENCES):
    """Gom câu thành khối ≤size câu, không cắt ngang đoạn (dòng trống) trừ khi một đoạn dài hơn size.
    Cắt ngang đoạn thì câu có nguồn ở khối bên cạnh sẽ bị gắn cờ UNGROUNDED_CLAIM oan."""
    paras = []
    for i, s in enumerate(sents):
        if i == 0 or re.search(r"\n\s*\n", script[sents[i - 1][1]:s[0]]):
            paras.append([])
        paras[-1].append(s)
    chunks, cur = [], []
    for p in paras:
        if cur and len(cur) + len(p) > size:
            chunks.append(cur)
            cur = []
        cur += p
        while len(cur) > size:
            chunks.append(cur[:size])
            cur = cur[size:]
    if cur:
        chunks.append(cur)
    return [(c[0][0], c[-1][1]) for c in chunks]


def review(script, llm=None):
    llm = llm or call_ai
    sents = split_sentences(script)
    chunks = pack_chunks(script, sents)
    starts = [s for s, _ in sents]

    def run(chunk):
        t = time.perf_counter()
        raw = llm(script[chunk[0]:chunk[1]])
        return raw, round((time.perf_counter() - t) * 1000)

    t0 = time.perf_counter()
    with ThreadPoolExecutor(MAX_WORKERS) as ex:
        results = list(ex.map(run, chunks))

    findings, trace_chunks, used = [], [], set()
    for (a, b), (raw, ms) in zip(chunks, results):
        kept = dup = 0
        for f in raw:
            span = f.get("exact_span") or ""
            pos = script.find(span, a, b) if span else -1
            while pos >= 0 and (pos, pos + len(span)) in used:  # cùng cụm lặp lại → lần xuất hiện kế tiếp
                pos = script.find(span, pos + 1, b)
            if pos < 0:
                dup += bool(span) and span in script[a:b]  # span có thật nhưng trùng finding khác, không phải bịa
                continue
            used.add((pos, pos + len(span)))
            conf = f.get("confidence") or "MEDIUM"
            findings.append({
                "id": f"f{len(findings) + 1}",
                "start": pos,
                "end": pos + len(span),
                "sentence": bisect.bisect_right(starts, pos),
                "category": f.get("category") or "OTHER",
                "severity": f.get("severity") or "MEDIUM",
                "issue_type": f.get("issue_type") or "CONTENT",
                "confidence": conf,
                "reason": f.get("reason") or "",
                "suggestion": "" if conf == "LOW" else (f.get("minimal_suggestion") or ""),
            })
            kept += 1
        trace_chunks.append({"sentences": sum(1 for s in starts if a <= s < b), "ms": ms,
                             "returned": len(raw), "kept": kept, "dropped": len(raw) - kept - dup,
                             "duplicates": dup})

    flagged = {f["sentence"] for f in findings}
    long_unflagged = [{"sentence": i + 1, "words": len(script[s:e].split())}
                      for i, (s, e) in enumerate(sents)
                      if i + 1 not in flagged and len(script[s:e].split()) > LONG_SENTENCE_WORDS]

    return {
        "session_id": uuid.uuid4().hex[:12],
        "sentences": sents,
        "findings": sorted(findings, key=lambda f: f["start"]),
        "long_unflagged": long_unflagged,
        "trace": {
            "model": MODEL,
            "sentences": len(sents),
            "llm_calls": len(chunks),
            "chunks": trace_chunks,
            "ms_total": round((time.perf_counter() - t0) * 1000),
            "kept": len(findings),
            "dropped": sum(c["dropped"] for c in trace_chunks),
        },
    }


def gemini(model, body):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Thiếu GEMINI_API_KEY")
    for attempt in range(3):
        r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                          headers={"x-goog-api-key": key}, json=body, timeout=60)
        if r.status_code != 503:  # 503 = Gemini báo quá tải tạm thời, thường qua sau vài giây
            break
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"]


@functools.cache
def piper_voice():
    from piper import PiperVoice
    if not Path(PIPER_VOICE).exists():
        raise RuntimeError(f"Chưa có giọng {Path(PIPER_VOICE).name}, tải theo codebase/README.md")
    # espeak-ng không đọc được thư mục dữ liệu nếu đường dẫn dài hơn ~160 ký tự (hay gặp trong venv lồng sâu)
    extra = {"espeak_data_dir": os.environ["PIPER_ESPEAK_DATA"]} if os.environ.get("PIPER_ESPEAK_DATA") else {}
    return PiperVoice.load(PIPER_VOICE, **extra)


def is_english(word):
    if word.isupper() and 2 <= len(word) <= 5:
        return True
    w = word.lower()
    return bool(re.search(r"[fjwz]", w)) or not VI_SYLLABLE.fullmatch(w)
    # ponytail: âm tiết Việt không dấu trùng từ Anh ("bot", "chat", "top") vẫn đọc giọng Việt — nghe gần đúng nên để vậy


def english_spans(text):
    """Vị trí các cụm từ tiếng Anh; từ liền nhau chỉ cách bằng khoảng trắng/gạch nối gộp thành một cụm."""
    spans = []
    for m in ASCII_WORD.finditer(text):
        if not is_english(m.group()):
            continue
        if spans and re.fullmatch(r"[ \t-]+", text[spans[-1][1]:m.start()]):
            spans[-1][1] = m.end()
        else:
            spans.append([m.start(), m.end()])
    return spans


@functools.cache
def en_phonemizer():
    from piper.phonemize_espeak import EspeakPhonemizer
    return EspeakPhonemizer(piper_voice().espeak_data_dir)


def mark_english(text):
    text = text.replace("[[", "[").replace("]]", "]")  # kịch bản không được tự chèn phiên âm thô
    out, pos = "", 0
    for a, b in english_spans(text):
        sents = en_phonemizer().phonemize("en-us", re.sub(r"[\s-]+", " ", text[a:b]))  # espeak tự đánh vần AI, GPT
        out += text[pos:a] + "[[ " + " ".join("".join(s) for s in sents) + " ]]"
        pos = b
    return out + text[pos:]


def synthesize(text, speed="vua"):
    """Văn bản → WAV. Không cache phía server: câu kịch bản không nằm lại sau buổi duyệt (non-goal §4)."""
    from piper import SynthesisConfig
    voice, buf = piper_voice(), io.BytesIO()
    # Tắt nhiễu ngẫu nhiên: cùng một câu luôn ra cùng một audio, nên so bản gốc/bản sửa mới công bằng
    # (đo 17/9: để mặc định, quãng ngắt ở dấu phẩy dao động 0,08–0,18 s giữa các lần đọc)
    config = SynthesisConfig(noise_scale=0.0, noise_w_scale=0.0, length_scale=SPEEDS[speed])
    with PIPER_LOCK, wave.open(buf, "wb") as w:  # đo 17/9 trên M1: 0,1–0,35 giây cho 3–8 giây audio
        for i, chunk in enumerate(voice.synthesize(mark_english(text), syn_config=config)):  # mỗi chunk là một câu
            if i == 0:
                w.setframerate(chunk.sample_rate)
                w.setsampwidth(chunk.sample_width)
                w.setnchannels(chunk.sample_channels)
            else:
                w.writeframes(bytes(int(chunk.sample_rate * PIPER_SENTENCE_SILENCE) * chunk.sample_width))
            w.writeframes(chunk.audio_int16_bytes)
    return buf.getvalue()


def transcribe(wav_b64):
    parts = gemini(TRANSCRIBE_MODEL, {"contents": [{"parts": [
        {"text": READBACK_PROMPT}, {"inlineData": {"mimeType": "audio/wav", "data": wav_b64}}]}]})
    return unicodedata.normalize("NFC", " ".join(p["text"] for p in parts if "text" in p).strip())


def readback_changes(written, spoken):
    """So chữ viết với chữ máy đọc theo từng từ. Trả về chỗ khác nhau: số/viết tắt đọc thành chữ, từ bị bỏ, từ thêm.
    start/end là vị trí trong `spoken` (None nếu máy bỏ không đọc)."""
    w = list(WORD.finditer(written))
    sp = list(WORD.finditer(spoken))
    ops = difflib.SequenceMatcher(None, [m.group().lower() for m in w], [m.group().lower() for m in sp],
                                  autojunk=False).get_opcodes()
    changes = []
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        start, end = (sp[j1].start(), sp[j2 - 1].end()) if j2 > j1 else (None, None)
        changes.append({"written": written[w[i1].start():w[i2 - 1].end()] if i2 > i1 else "",
                        "spoken": spoken[start:end] if start is not None else "",
                        "start": start, "end": end})
    return changes


def read_wav(wav):
    with wave.open(io.BytesIO(wav)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return x, sr


def prosody(wav, text, min_pause_s=0.12):
    """Đo cách đọc từ audio: âm lượng + cao độ mỗi 10 ms, chỗ ngắt hơi, đoạn dài nhất không ngắt.
    ponytail: ngưỡng im lặng = 10% âm lượng p95, cao độ bằng tự tương quan — đủ để so hai bản đọc
    của cùng một giọng, không phải phân tích ngữ âm chuẩn. Ngắt ≥0,12 s: đo 17/9 với Piper, dấu phẩy
    tạo lặng 0,12–0,14 s còn phụ âm tắc trong câu tối đa 0,11 s."""
    x, sr = read_wav(wav)
    hop, win = sr // 100, sr // 25  # bước 10 ms, cửa sổ 40 ms (đủ cho giọng thấp tới 70 Hz)
    if len(x) < win:
        return None
    frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop]
    rms = np.sqrt((frames ** 2).mean(axis=1))
    voiced = rms > 0.1 * np.percentile(rms, 95)
    idx = np.flatnonzero(voiced)
    if not len(idx):
        return None
    first, last = int(idx[0]), int(idx[-1]) + 1  # bỏ im lặng đầu/cuối

    pauses, start = [], None
    for i in range(first, last):
        if not voiced[i] and start is None:
            start = i
        elif voiced[i] and start is not None:
            if i - start >= round(min_pause_s * 100):
                pauses.append((start, i))
            start = None
    edges = [first] + [e for p in pauses for e in p] + [last]
    runs = [(edges[k + 1] - edges[k]) * 0.01 for k in range(0, len(edges), 2)]
    speech_s = sum(runs)

    # Cao độ: tự tương quan qua FFT, lấy độ trễ mạnh nhất trong khoảng 70–400 Hz
    f = frames - frames.mean(axis=1, keepdims=True)
    ac = np.fft.irfft(np.abs(np.fft.rfft(f, n=2 * win, axis=1)) ** 2, axis=1)[:, :win]
    lo, hi = sr // 400, sr // 70
    lag = lo + ac[:, lo:hi].argmax(axis=1)
    strength = ac[np.arange(len(ac)), lag] / np.maximum(ac[:, 0], 1e-9)
    f0 = np.where(voiced & (strength > 0.3), sr / lag, np.nan)
    with np.errstate(all="ignore"), warnings.catch_warnings():  # trung vị 5 khung bỏ gai nhảy quãng tám
        warnings.simplefilter("ignore", RuntimeWarning)
        smooth = np.nanmedian(np.lib.stride_tricks.sliding_window_view(np.pad(f0, 2, constant_values=np.nan), 5), axis=1)
    f0 = np.where(np.isnan(f0), np.nan, smooth)
    v = f0[~np.isnan(f0)]
    p10, p90 = (np.percentile(v, 10), np.percentile(v, 90)) if len(v) else (np.nan, np.nan)

    return {
        "duration": round(len(x) / sr, 2),
        "speech_s": round(speech_s, 2),
        "pauses": [[round(a * 0.01, 2), round(b * 0.01, 2)] for a, b in pauses],
        "longest_run_s": round(max(runs), 2),
        "rate": round(len(text.split()) / speech_s, 1) if speech_s else None,  # tiếng Việt: mỗi tiếng ~1 âm tiết
        "pitch_range_st": round(float(12 * np.log2(p90 / p10)), 1) if len(v) else None,  # nửa cung, p10→p90
        "envelope": np.round(rms / max(rms.max(), 1e-9), 3).tolist(),
        "pitch": [None if np.isnan(p) else round(float(p), 1) for p in f0],
    }


def log(name, record):
    LOGS.mkdir(exist_ok=True)
    record = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), **record}
    with open(LOGS / name, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


app = FastAPI(title="Spoken-Script QA")


class ReviewIn(BaseModel):
    script: str = Field(max_length=60_000)


class TtsIn(BaseModel):
    text: str = Field(min_length=1, max_length=2_000)
    speed: Literal["nhanh", "vua", "cham"] = "vua"


class ReadbackIn(BaseModel):
    text: str = Field(min_length=1, max_length=2_000)
    audio: str = Field(max_length=8_000_000)  # WAV base64, ~2 phút giọng đọc


class ProsodyIn(BaseModel):
    text: str = Field(min_length=1, max_length=2_000)
    audio: str = Field(max_length=8_000_000)


class AuditIn(BaseModel):
    session_id: str = Field(max_length=32)
    finding_id: str = Field(max_length=16)
    action: Literal["accept", "edit", "reject", "undo"]
    sentence: int
    category: str = Field(max_length=40)
    confidence: str = Field(max_length=10)
    span: str = Field(max_length=4_000)
    replacement: str = Field(default="", max_length=4_000)


@app.get("/")
def index():
    return FileResponse(ROOT / "web" / "index.html")


@app.post("/api/review")
def api_review(body: ReviewIn):
    try:
        result = review(body.script)
    except Exception as e:  # thiếu key, lỗi API, JSON hỏng — trả rõ cho UI, không nuốt lỗi
        raise HTTPException(502, f"Lời gọi LLM thất bại: {e}")
    log("trace.jsonl", {"session_id": result["session_id"], **result["trace"]})
    return result


@app.post("/api/tts")
def api_tts(body: TtsIn):
    try:
        wav = synthesize(body.text, body.speed)
    except Exception as e:  # UI tự chuyển sang giọng trình duyệt
        raise HTTPException(502, f"Không tạo được giọng đọc: {e}")
    rate = (prosody(wav, body.text) or {}).get("rate")  # tốc độ đo thật trên audio, để UI hiện "vừa nghe: x tiếng/giây"
    return Response(wav, media_type="audio/wav", headers={"X-Speech-Rate": str(rate or "")})


@app.get("/api/features")
def api_features():  # để giao diện báo trước nút nào dùng được, không đợi bấm rồi mới lỗi
    return {"readback": bool(os.environ.get("GEMINI_API_KEY")), "voice": VOICE_LABEL}


@app.post("/api/prosody")
def api_prosody(body: ProsodyIn):
    try:
        wav = base64.b64decode(body.audio, validate=True)
        result = prosody(wav, body.text)
    except Exception as e:  # base64 hỏng, không phải WAV
        raise HTTPException(400, f"Không phân tích được audio: {e}")
    if result is None:
        raise HTTPException(400, "Audio quá ngắn hoặc im lặng")
    return result


@app.post("/api/readback")
def api_readback(body: ReadbackIn):
    try:
        wav = base64.b64decode(body.audio, validate=True)
    except ValueError:
        raise HTTPException(400, "Audio không phải base64 hợp lệ")
    if wav[:4] != b"RIFF":
        raise HTTPException(400, "Audio phải là WAV")
    t = time.perf_counter()
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(503, "Chép lại audio cần GEMINI_API_KEY trong .env (OpenCode Go không có model nghe audio)")
    try:
        spoken = transcribe(body.audio)
    except Exception as e:
        raise HTTPException(502, f"Không chép lại được audio: {e}")
    return {"transcript": spoken, "model": TRANSCRIBE_MODEL, "voice": VOICE_LABEL, "ms": round((time.perf_counter() - t) * 1000),
            "changes": readback_changes(unicodedata.normalize("NFC", body.text), spoken)}


@app.post("/api/audit")
def api_audit(body: AuditIn):
    log("audit.jsonl", body.model_dump())
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
