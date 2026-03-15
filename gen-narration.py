#!/usr/bin/env python3
"""Generate two narration versions: longjiaxin_v3 (Cantonese) and longyingxun_v3."""
import dashscope, os, time, subprocess
from dashscope.audio.tts_v2 import SpeechSynthesizer

dashscope.api_key = "sk-8c4a0c0ee3804abbab5d9f37c411416a"

SCRIPT = [
    "每年因合規失誤造成的損失，遠超您的想像。",
    "法規更新頻率越來越快，傳統團隊已經跟不上。",
    "您需要的不是更多人力，而是更聰明的解決方案。",
    "如果有一位數字員工，能7乘24小時處理法律事務。",
    "不需要休假，不會遺漏，持續學習進化。",
    "這不是科幻，這是Lawrence。",
    "WiseLaw打造的AI法律合規數字員工。",
    "Lawrence不是一個聊天機器人。",
    "他是一位真正的數字員工，擁有獨立工作區與記憶系統。",
    "基於120多個國家法規數據庫，即時提供跨法域法律意見。",
    "覆蓋大陸、香港、東南亞及歐盟主要司法管轄區。",
    "秒級響應法規查詢，準確率超過人工檢索。",
    "讓我們看看他的核心能力。",
    "第一，法規智能檢索。",
    "第二，合約智能審查，多份文件同時處理。",
    "第三，數據隱私保護，個保法、PDPO、GDPR全覆蓋。",
    "第四，盡職調查分析，自動梳理證據鏈。",
    "第五，合規風險評估，多維度企業合規體檢。",
    "第六，7乘24自主工作，跨時區全天候運行。",
    "每一個場景都來自法律從業者的日常工作流。",
    "Lawrence不是概念驗證，他已經在運行。",
    "從諮詢到執行的全流程覆蓋。",
    "讓AI處理重複性工作，讓專業人員聚焦高價值判斷。",
    "安全是我們的底線，不是附加功能。",
    "端到端加密，私有化部署，數據永不外流。",
    "通過多項國際安全認證，值得企業信賴。",
    "WiseLaw，學術嚴謹與商業實戰深度融合。",
    "法律AI領域的開拓者。",
    "我們的團隊來自頂尖學府與國際律所。",
    "AI實戰培訓費用可100%折抵首年年費。",
    "零風險入場，先體驗再決定。",
    "每年為企業節省超過22萬元法律合規成本。",
    "讓Lawrence成為您的法律合規夥伴。",
    "不是取代律師，而是讓律師更強大。",
    "現在就開始，預約專屬演示。",
    "WiseLaw，讓合規成為競爭優勢。",
]

VOICES = {
    "longjiaxin_v3": "nuoqi-tts-jiaxin.mp3",
    "longyingxun_v3": "nuoqi-tts-yingxun.mp3",
}

for voice, output_file in VOICES.items():
    print(f"\n=== Generating {voice} → {output_file} ===")
    segments = []
    tmpdir = f"/tmp/narr-{voice}"
    os.makedirs(tmpdir, exist_ok=True)
    
    for i, text in enumerate(SCRIPT):
        seg_path = f"{tmpdir}/seg-{i:03d}.mp3"
        print(f"  [{i+1}/{len(SCRIPT)}] {text[:20]}...", end=" ", flush=True)
        try:
            synth = SpeechSynthesizer(model="cosyvoice-v3-flash", voice=voice)
            audio = synth.call(text)
            if audio and len(audio) > 100:
                with open(seg_path, "wb") as f:
                    f.write(audio)
                segments.append(seg_path)
                print(f"OK ({len(audio)} bytes)")
            else:
                print("EMPTY")
        except Exception as e:
            print(f"ERROR: {e}")
        time.sleep(0.2)
    
    # Concatenate with ffmpeg
    list_file = f"{tmpdir}/list.txt"
    with open(list_file, "w") as f:
        for seg in segments:
            # Add a 0.3s silence gap between segments
            f.write(f"file '{seg}'\n")
    
    out_path = f"/tmp/nuoqi-fix/{output_file}"
    cmd = f"ffmpeg -y -f concat -safe 0 -i {list_file} -af 'apad=pad_dur=0.3' -c:a libmp3lame -q:a 2 {out_path}"
    # Simple concat without gap first
    cmd = f"ffmpeg -y -f concat -safe 0 -i {list_file} -c:a libmp3lame -q:a 2 {out_path}"
    subprocess.run(cmd, shell=True, capture_output=True)
    
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f"\n✓ {output_file}: {size:,} bytes")
    else:
        print(f"\n✗ {output_file}: FAILED")

print("\nDone!")
