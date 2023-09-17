import DbUtilities

category_keywords_list = [
    ["Finance", ["investment", "banking", "stocks", "portfolio", "dividend", "planning", "management", "markets", "hedge", "funds", "capital", "asset", "equity", "insurance", "retirement", "savings", "taxes", "credit", "loans", "economy"]],
    ["Regulation", ["compliance", "regulatory", "legislation", "policy", "enforcement", "audit", "laws", "oversight", "rules", "standards", "governance", "complianceofficer", "risk", "security", "ethical", "disclosure", "transparency", "reporting", "accountability"]],
    ["MarketTrends", ["analysis", "trends", "research", "consumer", "segmentation", "growth", "industry", "competition", "forecasting", "opportunities", "demand", "supply", "pricing", "innovation", "customer", "preferences", "globalization", "sustainability", "digitalization", "disruption"]],
    ["RiskManagement", ["assessment", "mitigation", "analysis", "modeling", "tolerance", "factors", "strategy", "exposure", "control", "framework", "insurance", "strategic", "operational", "financial", "compliance", "cybersecurity", "reputation", "market", "liquidity"]],
    ["Disasters", ["disaster", "recovery", "emergency", "catastrophe", "preparedness", "resilience", "insuranceclaims", "responseplan", "crisismanagement", "natural", "hurricane", "earthquake", "flood", "wildfire", "pandemic", "climatechange", "vulnerability", "reconstruction", "community"]],
    ["Strategies", ["strategy", "planning", "growth", "marketing", "competitive", "innovation", "entry", "pricing", "sales", "product", "digital", "branding", "customer", "segment", "marketshare", "partnerships", "diversification", "sustainability", "talent"]],
    ["Challenges", ["challenges", "problems", "issues", "obstacles", "difficulties", "barriers", "constraints", "risks", "constraints", "disruptions", "crises", "uncertainty", "complexity", "volatility", "competition", "regulation", "technology", "sustainability", "talent", "costs"]],
    ["Events", ["event", "conference", "seminar", "exhibition", "webinar", "tradeshow", "networking", "workshop", "symposium", "summit", "convention", "meeting", "forum", "expo", "gathering", "presentation", "keynote", "panel", "discussion", "roundtable"]],
    ["Technology", ["technology", "innovation", "digital", "transformation", "artificialintelligence", "data", "cybersecurity", "cloud", "IoT", "blockchain", "automation", "emerging", "trends", "disruption", "smart", "devices", "connectivity", "analytics", "software", "hardware"]]
]

category_description = [
    "This category encompasses topics related to monetary matters, such as investment, banking, stocks, portfolio management, and financial planning. It also includes aspects like insurance, retirement, taxes, credit, loans, and various financial instruments.",
    "Regulation focuses on the rules and policies governing different industries and sectors. It involves compliance, legislation, enforcement, and oversight, ensuring that organizations adhere to ethical and legal standards while disclosing information transparently.",
    "This category deals with the analysis of trends and shifts in consumer behavior, market dynamics, and industry developments. It covers areas like research, competition, innovation, globalization, sustainability, and the impact of digitalization on markets.",
    "Risk management involves assessing and mitigating various types of risks that organizations face. This includes strategies for managing operational, financial, strategic, and compliance risks, as well as cybersecurity and market-related risks.",
    "Disasters concern events that can have catastrophic impacts on communities and organizations. Topics in this category include disaster recovery, emergency preparedness, insurance claims, and strategies for resilience in the face of natural disasters, pandemics, and climate change.",
    "Strategies revolve around planning and implementing approaches to achieve organizational goals. This includes marketing, competitive strategies, innovation, market entry, and branding, as well as talent and diversification strategies.",
    "Challenges encompass the various obstacles and difficulties that organizations encounter. These can include issues related to competition, regulation, technology, sustainability, talent, and cost management in an environment characterized by complexity and volatility.",
    "This category pertains to gatherings and activities where professionals can exchange knowledge and network. It includes events such as conferences, seminars, webinars, and exhibitions, where experts come together to share insights and experiences.",
    "Technology involves the latest advancements in the digital world, including artificial intelligence, data, cybersecurity, cloud computing, IoT (Internet of Things), blockchain, and emerging tech trends. It covers both software and hardware innovations."
]

for x, category in enumerate(category_keywords_list):
    category_name = category[0]
    category_keywords = category[1]
    DbUtilities.add_category(category_name, category_description[x], ','.join(category_keywords))