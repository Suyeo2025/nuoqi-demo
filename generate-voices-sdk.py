#!/usr/bin/env python3
"""Generate 20 TTS MP3 files using DashScope SDK + CosyVoice v3-flash."""
import dashscope, os, time
from dashscope.audio.tts_v2 import SpeechSynthesizer

dashscope.api_key = "sk-8c4a0c0ee3804abbab5d9f37c411416a"
OUTPUT_DIR = "/tmp/nuoqi-fix/nuoqi/pet-voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VOICES = [
    ("luke-zh.mp3", "longanyang", "你好，我是Luke，WiseLaw的协同数字员工。负责内部运营、任务管理和团队协调，让工作流程更高效。"),
    ("luke-yue.mp3", "longanyue_v3", "你好，我係Luke，WiseLaw嘅协同数字员工。负责内部运营、任务管理同团队协调。"),
    ("luke-en.mp3", "longanyang", "Hi, I'm Luke, WiseLaw's collaboration digital employee. I handle internal operations, task management, and team coordination."),
    ("luke-ja.mp3", "loongtomoka_v3", "こんにちは、WiseLawのコラボレーションデジタル社員のLukeです。社内業務、タスク管理、チーム連携を担当しています。"),
    ("luke-ko.mp3", "loongkyong_v3", "안녕하세요, 저는 WiseLaw의 협업 디지털 직원 Luke입니다. 내부 운영, 작업 관리 및 팀 조정을 담당합니다."),
    ("lawra-zh.mp3", "longanli_v3", "你好，我是Lawra，WiseLaw的商务数字员工。专注于客户拓展、销售支持和商务对接，帮助团队达成交易。"),
    ("lawra-yue.mp3", "longjiaxin_v3", "你好，我係Lawra，WiseLaw嘅商务数字员工。专注于客户拓展、销售支持同商务对接。"),
    ("lawra-en.mp3", "longanli_v3", "Hello, I'm Lawra, WiseLaw's business digital employee. I focus on client development, sales support, and business partnerships."),
    ("lawra-ja.mp3", "loongriko_v3", "こんにちは、WiseLawのビジネスデジタル社員のLawraです。クライアント開発、営業支援、ビジネス連携に注力しています。"),
    ("lawra-ko.mp3", "loongkyong_v3", "안녕하세요, 저는 WiseLaw의 비즈니스 디지털 직원 Lawra입니다. 고객 개발, 영업 지원 및 비즈니스 파트너십에 집중합니다."),
    ("lawrence-zh.mp3", "longsanshu_v3", "你好，我是Lawrence，WiseLaw的法律合规数字员工。覆盖一百二十多个法域，专注法律执行、合同审查和合规报告。"),
    ("lawrence-yue.mp3", "longanyue_v3", "你好，我係Lawrence，WiseLaw嘅法律合规数字员工。覆盖一百二十多个法域，专注法律执行、合同审查同合规报告。"),
    ("lawrence-en.mp3", "longsanshu_v3", "Hello, I'm Lawrence, WiseLaw's legal compliance digital employee. Covering over one hundred and twenty jurisdictions, I specialize in legal execution, contract review, and compliance reporting."),
    ("lawrence-ja.mp3", "loongtomoka_v3", "こんにちは、WiseLawの法務コンプライアンスデジタル社員のLawrenceです。百二十以上の法域をカバーし、法務執行、契約審査、コンプライアンスレポートを専門としています。"),
    ("lawrence-ko.mp3", "loongkyong_v3", "안녕하세요, 저는 WiseLaw의 법률 컴플라이언스 디지털 직원 Lawrence입니다. 백이십 개 이상의 법역을 다루며 법률 실행, 계약 검토 및 컴플라이언스 보고를 전문으로 합니다."),
    ("lancelot-zh.mp3", "longcheng_v3", "你好，我是Lancelot，WiseLaw的知识管理数字员工。负责法规研究、知识整理和持续学习，让团队的法律知识库始终保持最新。"),
    ("lancelot-yue.mp3", "longanyue_v3", "你好，我係Lancelot，WiseLaw嘅知识管理数字员工。负责法规研究、知识整理同持续学习。"),
    ("lancelot-en.mp3", "longcheng_v3", "Hi, I'm Lancelot, WiseLaw's knowledge management digital employee. I handle regulatory research, knowledge organization, and continuous learning."),
    ("lancelot-ja.mp3", "loongriko_v3", "こんにちは、WiseLawのナレッジマネジメントデジタル社員のLancelotです。法規調査、知識整理、継続学習を担当しています。"),
    ("lancelot-ko.mp3", "loongkyong_v3", "안녕하세요, 저는 WiseLaw의 지식 관리 디지털 직원 Lancelot입니다. 규정 조사, 지식 정리 및 지속적 학습을 담당합니다."),
]

for i, (filename, voice, text) in enumerate(VOICES, 1):
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"[{i}/20] {filename} (voice={voice})...", end=" ", flush=True)
    try:
        synth = SpeechSynthesizer(model="cosyvoice-v3-flash", voice=voice)
        audio = synth.call(text)
        if audio and len(audio) > 100:
            with open(filepath, "wb") as f:
                f.write(audio)
            print(f"OK ({len(audio)} bytes)")
        else:
            print(f"EMPTY or too small")
    except Exception as e:
        print(f"ERROR: {e}")
    time.sleep(0.3)

print("\n=== Results ===")
for f in sorted(os.listdir(OUTPUT_DIR)):
    size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
    print(f"  {f}: {size:,} bytes")
