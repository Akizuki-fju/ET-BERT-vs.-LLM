# 加密流量分析實作與模型比較 (ET-BERT vs. LLM)

本專案旨在探討並比較 **ET-BERT (Encrypted Traffic BERT)** 與現代 **大型語言模型 (LLM)** 在惡意加密流量分析（如區分 Cobalt Strike C2 與 TeamViewer）上的應用成效與限制。

## 1. 專案背景與目標 (Overview)
隨著網路傳輸全面加密化 (TLS/SSL)，傳統的特徵碼檢測 (Signature-based) 已難以應對。
* **ET-BERT 方法**：將封包的 Hex Payload 視為一種「語言」，透過預訓練模型來識別惡意流量的潛在特徵。
* **研究目標**：實作 ET-BERT 的資料預處理流程，並將相同數據輸入 GPT-4 進行比較，分析兩者在資安防禦上的定位差異。

## 2. 實作一：資料預處理 (Data Pre-processing)
為了驗證 ET-BERT 的運作機制，我們撰寫了 Python 自動化腳本 (基於 `scapy` 框架)，負責生成/讀取 PCAP 流量，並將其轉換為 BERT 模型專用的輸入格式。

* **轉換邏輯**：將 Payload Bytes 轉換為 Hex String，並依序切割為 Token。
* **格式標準**：`[CLS] Hex_Token_1 Hex_Token_2 ... [SEP]`

### 實作成果截圖
下圖顯示腳本成功將 TLS ClientHello 封包轉換為 BERT Token 序列，證明了模型輸入管道的可行性。

![資料預處理成果](evidence_preprocessing.png)

## 3. 實作二：LLM 流量分析實驗 (LLM Comparison)
作為對照組，我們提取了相同的 Hex Payload，直接輸入大型語言模型 (ChatGPT/GPT-4) 進行 "Zero-shot" 分析，測試其對純封包數據的理解能力。

### 分析結果
* **協定識別 (Protocol ID)**：LLM 能精準識別出這是 **TLS ClientHello** 封包，並解析出 TLS 版本與 Cipher Suites。
* **惡意判斷 (Detection)**：LLM 態度保守。在缺乏上下文 (如 IP 信譽、JA3 指紋) 的情況下，LLM 難以單憑封包內容斷定是否為惡意攻擊。

![LLM 分析成果](evidence_llm1.png, evidence_llm2.png,evidence_llm3.png,evidence_llm4.png)

## 4. 綜合比較結論 (Conclusion)

本研究總結出兩種技術在資安實務上的不同定位：

| 比較項目 | ET-BERT (專用小模型) | LLM (通用大模型) |
| :--- | :--- | :--- |
| **輸入資料** | Hex Token 序列 | 自然語言 / Hex / Log |
| **推論速度** | **極快** (適合即時串流偵測) | 慢 (高延遲，僅適合離線分析) |
| **強項** | **檢測 (Detection)**：抓出隱蔽的惡意特徵 | **調查 (Investigation)**：解釋協定內容與欄位意義 |
| **應用場景** | 大規模流量過濾、防火牆自動阻擋 | SOC 分析師輔助工具、威脅獵捕 (Threat Hunting) |

## 5. 如何執行腳本 (Usage)
本專案包含一個 Python 預處理腳本 `traffic_preprocessing.py`。

```bash
# 安裝依賴
pip install scapy

# 執行腳本 (將自動生成測試 PCAP 並轉換格式)
python traffic_preprocessing.py