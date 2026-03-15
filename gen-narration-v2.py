#!/usr/bin/env python3
"""Generate V2 narration: follows page content exactly. Two voices."""
import dashscope, os, time, subprocess
from dashscope.audio.tts_v2 import SpeechSynthesizer

dashscope.api_key = "sk-8c4a0c0ee3804abbab5d9f37c411416a"

# Script follows page section order exactly
SCRIPT = [
    # HERO
    "法律AI，全新範式，2026。",
    "Lawrence，新一代法律合規數字員工。",
    "不是聊天機器人——是懂法律、會執行、能進化的數字員工。長期駐場在你的工作環境，擁有獨立工作區與記憶系統。你睡着的時候，他繼續推進任務。",
    # I · 認識 Lawrence (feature cards)
    "認識Lawrence。專業性——他是專業領域內擁有獨到Skill的專家，覆蓋120多個國家的法規數據庫。",
    "實用性——7乘24小時主動幹活，多渠道接入飛書、WhatsApp、郵件、Telegram。",
    "靈活性——深度記憶系統，越用越懂你。可操作文件系統、數據庫、Git倉庫和定時任務。",
    "安全性——支持本地部署。三層安全體系：架構級沙箱、服務級巡檢、認證級合規。",
    # Timeline
    "我們正在經歷AI工作範式的第三次躍遷。從Prompt Engineer，到Context Engineer，再到Harness Engineer。人類從操作員變成管理者。",
    # I-b · 標配
    "大模型是員工的大腦，WiseLaw是整套工位。",
    "數據主權——原始文檔留在你的機器，僅任務相關片段經過大模型API。當客戶問我的案件資料在哪裏，最有力的回答是指着辦公室裏的一台機器說：就在那裏。",
    "持久化工作——WiseLaw的AI有自己的物理工作區。它不只記得你說過什麼，還能在你不在的時候自動執行工作。",
    "完整運行環境——你不能只給員工一個大腦就讓他上班。WiseLaw就是整套工位。",
    "六大渠道統一接入：飛書、WhatsApp、Telegram、郵件、Slack、Web Chat。",
    # II · 六大核心能力
    "六大核心能力。法規智能檢索、合約智能審查、數據隱私保護、盡職調查分析、合規風險評估、7乘24自主工作。",
    "多份關聯合同同時處理，自動標註風險條款，輸出修訂痕跡與風險匯總報告。",
    # II-b · 產品定位
    "專業垂直versus通用廣泛。Lawrence是企業法律數字員工，不是個人通用AI工具。",
    "自研沙箱加插件白名單，對比社區自治。120多個國家法規庫，對比通用技能。幫客戶跑通前100個任務全程陪跑，對比工具交付。",
    # II-c · 技術架構
    "Lawrence的工位全景。每一個組件都運行在你的本地環境，數據從不離開你的控制範圍。",
    # II-d · 數據流向
    "你的數據，始終在你的掌控之中。客戶郵件進入後本地接收，Gateway本地處理，Lawrence本地推理。僅任務片段經過LLM API，生成的回覆草稿本地存儲，最後人工審批發出。",
    # III · 合規挑戰
    "醫療健康企業面臨的三重合規壓力——多法域合規、健康數據出境、醫療器械監管。這些挑戰不會消失，只會加劇。",
    # IV · 場景演示
    "每一個場景都來自法律從業者的日常工作流。Lawrence不是概念驗證——他已經在運行。",
    # IV · 工作實錄
    "Lawrence工作實錄。真實場景，即時響應。合同審查、跨境合規、證據梳理、郵件處理、工作區管理——五大場景實時演示。",
    # IV-b · 安全體系
    "安全不是功能，是基因。法律數據極度敏感——合同內容、客戶信息、訴訟策略。Lawrence從架構設計層面杜絕風險。",
    "第一層：架構級安全。自研安全沙箱，插件白名單，Rules Injector。",
    "第二層：服務級安全。定期巡檢，漏洞實時響應，安全分析報告。",
    "第三層：認證級安全。PDPO、ISO 27001、SOC 2 Type II合規認證路線圖。",
    "護城河戰略——越用越難替代。安全防護、法律知識深度、可信網絡效應、AI組織方法論、數據資產鎖定、安全售後服務。六大壁壘，構建結構性競爭優勢。",
    # V · 我們的故事
    "WiseLaw是率先進化為AI Native組織的實踐者。我們不只賣Lawrence——我們每天都在用他。",
    "從任務分配到客戶跟進到內容生產，每一個工作流都有AI員工參與。這不是Demo，這是每天在運行的生產系統。",
    "1500多位法律專業人士正在使用。覆蓋120多個國家法規數據庫。效率提升5到10倍。",
    # VI · AI 員工矩陣
    "四角色數字員工矩陣。Luke負責協同，Lawra負責成交，Lawrence負責交付，Lancelot負責成長。各司其職，協同運轉。",
    # VII · 專業團隊
    "跨學科精英團隊，深耕法律科技。學術嚴謹與商業實戰深度融合。",
    # 企業口碑
    "企業信賴的法律AI夥伴。金融科技、醫療健康、跨境電商，多個行業已在使用。",
    # VIII · 定價
    "先體驗，再決策。培訓課程《打造你的AI數字員工》HKD 6,888，全程用Lawrence實時演示，100%折抵首年年費。",
    "基礎版HKD 68,888每台每年，快速體驗核心價值。企業版HKD 118,888每台每年，十台起，全團隊AI組織轉型。",
    # VIII-b · 陪跑服務
    "不只賣軟件，全程陪跑。12節實戰培訓加AI組織診斷。前100個任務全程跟進，確保Lawrence真正融入你的工作流。",
    # IX · 快速入職
    "14天，讓Lawrence成為你的團隊成員。Day 1硬件交付，Day 2到3渠道接入，Day 4到7首批任務，Day 8到14效果評估。支持遠程或線下安裝，無需技術人員。",
    # CTA
    "讓Lawrence為你的企業工作。不是取代律師，而是讓律師更強大。WiseLaw——讓合規成為競爭優勢。",
]

VOICES = {
    "longjiaxin_v3": "nuoqi-tts-jiaxin.mp3",
    "longyingxun_v3": "nuoqi-tts-yingxun.mp3",
}

for voice, output_file in VOICES.items():
    print(f"\n=== {voice} → {output_file} ({len(SCRIPT)} segments) ===")
    tmpdir = f"/tmp/narr-v2-{voice}"
    os.makedirs(tmpdir, exist_ok=True)
    segments = []

    for i, text in enumerate(SCRIPT):
        seg_path = f"{tmpdir}/seg-{i:03d}.mp3"
        print(f"  [{i+1}/{len(SCRIPT)}] {text[:25]}...", end=" ", flush=True)
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

    # Concat
    list_file = f"{tmpdir}/list.txt"
    with open(list_file, "w") as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")

    out_path = f"/tmp/nuoqi-fix/{output_file}"
    subprocess.run(
        f"ffmpeg -y -f concat -safe 0 -i {list_file} -c:a libmp3lame -q:a 2 {out_path}",
        shell=True, capture_output=True
    )

    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        # Get duration
        r = subprocess.run(f"ffprobe -i {out_path} -show_entries format=duration -v quiet -of csv=p=0", 
                          shell=True, capture_output=True, text=True)
        dur = float(r.stdout.strip()) if r.stdout.strip() else 0
        print(f"\n✓ {output_file}: {size:,} bytes, {dur:.1f}s")
    else:
        print(f"\n✗ FAILED")

print("\nDone!")
