import DbUtilities

category_keywords_list = [
    ["金融", ["investment", "banking", "stocks", "portfolio", "dividend", "planning", "management", "markets", "hedge", "funds", "capital", "asset", "equity", "insurance", "retirement", "savings", "taxes", "credit", "loans", "economy"]],
    ["規範", ["compliance", "regulatory", "legislation", "policy", "enforcement", "audit", "laws", "oversight", "rules", "standards", "governance", "complianceofficer", "risk", "security", "ethical", "disclosure", "transparency", "reporting", "accountability"]],
    ["市場趨勢", ["analysis", "trends", "research", "consumer", "segmentation", "growth", "industry", "competition", "forecasting", "opportunities", "demand", "supply", "pricing", "innovation", "customer", "preferences", "globalization", "sustainability", "digitalization", "disruption"]],
    ["風險管理", ["assessment", "mitigation", "analysis", "modeling", "tolerance", "factors", "strategy", "exposure", "control", "framework", "insurance", "strategic", "operational", "financial", "compliance", "cybersecurity", "reputation", "market", "liquidity"]],
    ["災害", ["disaster", "recovery", "emergency", "catastrophe", "preparedness", "resilience", "insuranceclaims", "responseplan", "crisismanagement", "natural", "hurricane", "earthquake", "flood", "wildfire", "pandemic", "climatechange", "vulnerability", "reconstruction", "community"]],
    ["策略", ["strategy", "planning", "growth", "marketing", "competitive", "innovation", "entry", "pricing", "sales", "product", "digital", "branding", "customer", "segment", "marketshare", "partnerships", "diversification", "sustainability", "talent"]],
    ["挑戰", ["challenges", "problems", "issues", "obstacles", "difficulties", "barriers", "constraints", "risks", "constraints", "disruptions", "crises", "uncertainty", "complexity", "volatility", "competition", "regulation", "technology", "sustainability", "talent", "costs"]],
    ["活動", ["event", "conference", "seminar", "exhibition", "webinar", "tradeshow", "networking", "workshop", "symposium", "summit", "convention", "meeting", "forum", "expo", "gathering", "presentation", "keynote", "panel", "discussion", "roundtable"]],
    ["科技", ["technology", "innovation", "digital", "transformation", "artificialintelligence", "data", "cybersecurity", "cloud", "IoT", "blockchain", "automation", "emerging", "trends", "disruption", "smart", "devices", "connectivity", "analytics", "software", "hardware"]]
]

category_description = [
    "此類別涵蓋與金錢相關的主題，如投資、銀行、股票、投資組合管理和財務規劃。它還包括保險、退休、稅收、信用、貸款和各種金融工具。",
    "規範關注不同行業和部門的規則和政策。它涉及合規性、立法、執法和監督，確保組織遵守道德和法律標準，並透明地披露信息。",
    "此類別處理消費者行為、市場動態和產業發展的趨勢分析。它涵蓋了研究、競爭、創新、全球化、可持續性以及數位化對市場的影響。",
    "風險管理涉及評估和緩解組織面臨的各種風險。這包括管理運營、財務、戰略和合規性風險的策略，以及信息安全和市場相關風險。",
    "災害涉及對社區和組織產生災難性影響的事件。此類主題包括災害恢復、緊急情況、保險索賠以及面對自然災害、大流行和氣候變遷時的恢復力策略。",
    "策略圍繞著制定和實施實現組織目標的方法。這包括市場營銷、競爭策略、創新、市場進入、品牌塑造以及人才和多元化策略。",
    "挑戰包括組織遇到的各種障礙和困難。這些可能涉及競爭、監管、技術、可持續性、人才和成本管理等問題，在一個複雜和波動的環境中。",
    "此類別涉及專業人士交流知識和建立網絡的各種聚會和活動。它包括活動，如會議、研討會、網絡研討會和展覽，專家們可以在這些場合分享見解和經驗。",
    "科技涵蓋數位世界的最新進展，包括人工智慧、資料、資訊安全、雲端、物聯網、區塊鏈、自動化、新興趨勢、顛覆性技術、智慧設備、連接性、分析、軟體和硬體創新。"
]


for x, category in enumerate(category_keywords_list):
    category_name = category[0]
    category_keywords = category[1]
    DbUtilities.add_category(category_name, category_description[x], ','.join(category_keywords))