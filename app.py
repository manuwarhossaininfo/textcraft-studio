"""
TextCraft - Linguistic Deconstructor & Advanced Writing Masterclass Studio
Main Streamlit Application
"""

import streamlit as st
import json
import os
import time
from pathlib import Path

# Import modules
from modules.gemini_client import GeminiClient
from modules.analyzer import ArticleAnalyzer
from modules.vocabulary import VocabularyProcessor
from modules.clause_xray import ClauseXRay
from modules.writing_program import WritingProgram
from modules.transformer import SentenceTransformer
from modules.pdf_handler import PDFHandler
from modules.url_handler import URLHandler
from modules.utils import Utils

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="TextCraft Studio",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# Google Analytics 4 Integration
# ============================================
def inject_ga4():
    """Inject Google Analytics 4 tracking code into Streamlit app."""
    GA4_ID = "G-HE6RFMKP45"  # ← আপনার Measurement ID বসান
    
    ga_script = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA4_ID}', {{
            'page_title': 'TextCraft Studio',
            'page_path': window.location.pathname
        }});
        
        // Track tab clicks
        document.addEventListener('click', function(e) {{
            if (e.target && e.target.getAttribute('role') === 'tab') {{
                gtag('event', 'tab_click', {{
                    'tab_name': e.target.innerText,
                    'event_category': 'engagement'
                }});
            }}
        }});
        
        // Track button clicks
        document.addEventListener('click', function(e) {{
            if (e.target && e.target.tagName === 'BUTTON') {{
                gtag('event', 'button_click', {{
                    'button_text': e.target.innerText,
                    'event_category': 'interaction'
                }});
            }}
        }});
    </script>
    """
    
    from streamlit.components.v1 import html
    html(ga_script, height=0, width=0)

# Call the function right after page config
inject_ga4()
# Load custom CSS
css_path = Path("assets/style.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================================
# Session State Initialization
# ============================================
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "flashcard_index" not in st.session_state:
    st.session_state.flashcard_index = 0
if "flashcard_flipped" not in st.session_state:
    st.session_state.flashcard_flipped = False
if "checklist_state" not in st.session_state:
    st.session_state.checklist_state = {}
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ============================================
# Quick Sample Articles
# ============================================
QUICK_SAMPLES = {
    "🌍 Climate Change (The Economist Style)": """Despite mounting evidence that anthropogenic climate change poses an existential threat to biodiversity and human civilization alike, policymakers in many industrialized nations have proven stubbornly reluctant to implement the sweeping regulatory reforms that scientists deem indispensable. While the Paris Agreement of 2015 galvanized unprecedented international consensus on the imperative of limiting global warming to 1.5 degrees Celsius above pre-industrial levels, subsequent progress has been fitful at best. Emissions continue to climb, propelled by insatiable demand for fossil fuels in rapidly developing economies, even as renewable energy technologies achieve remarkable cost reductions that render the transition economically viable. The paradox is stark: never before have the tools to avert catastrophe been so readily available, yet the political will to deploy them at scale remains conspicuously absent. Compounding this inertia, powerful fossil-fuel lobbies exert disproportionate influence over legislative agendas, effectively stymieing carbon-pricing mechanisms that economists across the political spectrum endorse as the most efficient pathway to decarbonization. Meanwhile, vulnerable island nations and coastal communities, which contribute negligibly to global emissions, bear the brunt of rising sea levels and intensifying storms—a cruel irony that underscores the profound inequity embedded in the climate crisis.""",

    "📱 AI & Society (Harvard Review Style)": """The rapid proliferation of artificial intelligence across virtually every sector of the global economy has precipitated a profound reckoning with questions that were, until recently, confined to the realm of speculative fiction. As machine-learning algorithms demonstrate increasingly sophisticated capabilities—from composing persuasive prose to diagnosing complex medical conditions with accuracy that rivals, and occasionally surpasses, that of seasoned physicians—the boundaries between human cognition and computational intelligence have grown disconcertingly porous. This technological metamorphosis, while undeniably auspicious in its potential to alleviate suffering, enhance productivity, and democratize access to knowledge, simultaneously engenders a constellation of ethical dilemmas that demand rigorous and anticipatory governance. Chief among these concerns is the specter of algorithmic bias: when training data reflects the prejudices endemic to the societies that produce it, AI systems risk perpetuating and even amplifying systemic inequities under a veneer of mathematical objectivity. Furthermore, the displacement of human labor by automated systems threatens to exacerbate economic polarization, hollowing out middle-skill occupations while concentrating wealth among those who own and operate the technological infrastructure.""",

    "🏙️ Urbanization (Short Editorial)": """The relentless pace of urbanization in the developing world, where an estimated 1.5 million people migrate to cities each week, is straining infrastructure that was never designed to accommodate such explosive growth. Overcrowded slums proliferate on the periphery of megacities, their inhabitants denied access to clean water, sanitation, and healthcare—basic amenities that most urban planners take for granted. Yet amid this seemingly intractable crisis, innovative approaches are emerging. From Medellín's celebrated cable-car transit system, which has transformed once-isolated hillside favelas into connected communities, to Singapore's pioneering vertical farms that promise food security within densely packed urban landscapes, cities are demonstrating a remarkable capacity for reinvention. The challenge, however, extends far beyond engineering: it demands a fundamental reimagining of governance structures that too often privilege the interests of property developers over the needs of ordinary citizens."""
}


# ============================================
# Helper Functions
# ============================================
def get_client():
    """Get or create Gemini client."""
    api_key = st.session_state.api_key
    if not api_key:
        return None
    return GeminiClient(api_key)


def render_header():
    """Render the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>📝 TextCraft Studio</h1>
        <p>Linguistic Deconstructor & Advanced Writing Masterclass</p>
        <p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">
            আর্টিকেল ব্যবচ্ছেদ করুন • শব্দভান্ডার সমৃদ্ধ করুন • উন্নত লেখা শিখুন
        </p>
    </div>
    """, unsafe_allow_html=True)
# Share buttons
st.markdown("""
<div style="text-align: center; margin: 1rem 0;">
    <a href="https://www.facebook.com/sharer/sharer.php?u=https://manuwarhossaininfo-textcraft-studio-app-vqbkjx.streamlit.app/" 
       target="_blank" 
       style="background: #1877F2; color: white; padding: 8px 16px; 
              border-radius: 5px; text-decoration: none; margin: 5px;">
        📘 Share on Facebook
    </a>
    <a href="https://twitter.com/intent/tweet?text=Check%20out%20TextCraft%20Studio%20-%20Free%20AI%20Writing%20Masterclass!&url=https://manuwarhossaininfo-textcraft-studio-app-vqbkjx.streamlit.app/" 
       target="_blank" 
       style="background: #1DA1F2; color: white; padding: 8px 16px; 
              border-radius: 5px; text-decoration: none; margin: 5px;">
        🐦 Share on Twitter
    </a>
    <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://manuwarhossaininfo-textcraft-studio-app-vqbkjx.streamlit.app/" 
       target="_blank" 
       style="background: #0A66C2; color: white; padding: 8px 16px; 
              border-radius: 5px; text-decoration: none; margin: 5px;">
        💼 Share on LinkedIn
    </a>
</div>
""", unsafe_allow_html=True)


def render_5w1h_tab(data):
    """Visual information extraction — facts highlighted inside sentences."""
    if "error" in data:
        st.error(f"Error: {data.get('error')}")
        if "raw_response" in data:
            with st.expander("📄 Raw"):
                st.text(data["raw_response"])
        return

    # ── Header ──
    st.markdown(f"""
    <div class="info-card">
        <h3>📌 {data.get('title', 'Article')}</h3>
        <p>📊 {data.get('word_count', 0)} words | 📈 {data.get('reading_level', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Color Legend ──
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px 20px; margin: 15px 0; display: flex; gap: 25px; flex-wrap: wrap;">
        <span style="font-size: 14px;">🎨 রঙের মানে:</span>
        <span style="background: rgba(255,107,107,0.25); color: #FF6B6B; padding: 3px 10px; border-radius: 5px; font-weight: bold;">🔴 কাঁচা তথ্য (Raw Info)</span>
        <span style="background: rgba(77,163,255,0.2); color: #4da3ff; padding: 3px 10px; border-radius: 5px; font-weight: bold;">🔵 যোগ করা সাজসজ্জা (Decoration)</span>
        <span style="background: rgba(255,217,61,0.2); color: #ffd93d; padding: 3px 10px; border-radius: 5px; font-weight: bold;">🟡 হুক (Hook)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Section 1: Raw Facts ──
    st.subheader("📋 কাঁচা তথ্য (Raw Facts)")
    st.caption("আর্টিকেল থেকে সব অলংকার সরিয়ে শুধু তথ্য")

    facts = data.get("raw_facts", [])
    facts_bn = data.get("raw_facts_bn", [])

    cols = st.columns(2)
    for i, fact in enumerate(facts):
        with cols[i % 2]:
            bn = facts_bn[i] if i < len(facts_bn) else ""
            st.markdown(f"""
            <div style="background: rgba(255,107,107,0.08); border-left: 3px solid #FF6B6B; 
                        border-radius: 6px; padding: 8px 12px; margin: 4px 0;">
                <span style="color: #FF6B6B; font-weight: bold;">#{i+1}</span>
                <span style="color: #d0d0d0;"> {fact}</span>
                <br><span style="color: #888; font-size: 0.85rem;">🇧🇩 {bn}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Section 2: Fact → Sentence (THE MAIN VISUAL) ──
    st.subheader("🔬 তথ্য → বাক্য: কীভাবে তথ্য বাক্যে রূপ নেয়")
    st.caption("🔴 লাল = কাঁচা তথ্য | 🔵 নীল = সাজসজ্জা | দেখুন কীভাবে তথ্য বড় হয়েছে")

    mappings = data.get("fact_to_sentence", [])
    for i, m in enumerate(mappings, 1):
        fact = m.get("fact", "")
        fact_bn = m.get("fact_bn", "")
        sentence = m.get("full_sentence", "")
        info_words = m.get("info_words", [])
        added_words = m.get("added_words", [])
        role = m.get("role", "")
        role_bn = m.get("role_bn", "")

        # Build highlighted sentence HTML
        highlighted = _highlight_sentence(sentence, info_words, added_words)

        # Role badge color
        role_colors = {
            "hook": "#ffd93d", "support": "#28a745", "conclusion": "#a88beb",
            "context": "#4da3ff", "contrast": "#fd7e14", "data": "#17a2b8"
        }
        rc = role_colors.get(role.lower(), "#888")

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 15px; margin: 10px 0; border: 1px solid rgba(255,255,255,0.06);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="color: #FF6B6B; font-weight: bold; font-size: 1rem;">📌 তথ্য #{i}: {fact}</span>
                <span style="background: {rc}22; color: {rc}; padding: 2px 10px; border-radius: 10px; font-size: 0.8rem; font-weight: bold;">{role_bn}</span>
            </div>
            <div style="color: #888; font-size: 0.85rem; margin-bottom: 8px;">🇧🇩 {fact_bn}</div>
            <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 12px; line-height: 2; font-size: 1rem;">
                {highlighted}
            </div>
            <div style="margin-top: 8px; font-size: 0.8rem; color: #666;">
                🔴 তথ্যের শব্দ: {', '.join(info_words[:8])} &nbsp;|&nbsp; 
                🔵 সাজসজ্জা: {', '.join(added_words[:8])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Section 3: Idea Flow ──
    st.subheader("💡 Idea Flow — তথ্য মিলে ধারণা তৈরি")
    st.caption("কোন তথ্যগুলো একসাথে মিলে কী ধারণা বানাচ্ছে")

    ideas = data.get("idea_flow", [])
    for i, idea in enumerate(ideas, 1):
        facts_used = idea.get("facts_used", [])
        st.markdown(f"""
        <div style="background: rgba(40,167,69,0.08); border-left: 3px solid #28a745; 
                    border-radius: 8px; padding: 10px 15px; margin: 6px 0;">
            <span style="color: #28a745; font-weight: bold;">💡 Idea {i}:</span>
            <span style="color: #d0d0d0;"> {idea.get('idea', '')}</span>
            <br><span style="color: #888; font-size: 0.85rem;">🇧🇩 {idea.get('idea_bn', '')}</span>
            <br><span style="color: #4da3ff; font-size: 0.8rem;">📎 তথ্য: {' + '.join(facts_used)}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Section 4: Hook Analysis ──
    st.subheader("🪝 Hook — কীভাবে তথ্য দিয়ে পাঠক ধরা হয়")

    hooks = data.get("hook_analysis", [])
    if hooks:
        for h in hooks:
            h_type = h.get("hook_type_bn", h.get("hook_type", ""))
            st.markdown(f"""
            <div style="background: rgba(255,217,61,0.08); border-left: 3px solid #ffd93d; 
                        border-radius: 8px; padding: 12px 15px; margin: 6px 0;">
                <span style="color: #ffd93d; font-weight: bold;">🪝 {h_type}</span>
                <p style="color: #d0d0d0; margin: 5px 0; font-style: italic;">"{h.get('hook_sentence', '')}"</p>
                <span style="color: #FF6B6B; font-size: 0.85rem;">📌 কাঁচা তথ্য: {h.get('fact', '')}</span>
                <br><span style="color: #888; font-size: 0.8rem;">🇧🇩 {h.get('fact_bn', '')}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hook data available.")


def _highlight_sentence(sentence: str, info_words: list, added_words: list) -> str:
    """Highlight info words in red and added words in blue within a sentence."""
    import re as _re

    if not sentence:
        return ""

    result = sentence

    # Highlight info words (red)
    for word in info_words:
        if not word or len(word) < 2:
            continue
        pattern = _re.compile(r'(\b' + _re.escape(word) + r'\b)', _re.IGNORECASE)
        result = pattern.sub(
            r'<span style="background: rgba(255,107,107,0.3); color: #FF6B6B; padding: 1px 4px; border-radius: 3px; font-weight: bold;">\1</span>',
            result,
            count=1
        )

    # Highlight added words (blue)
    for word in added_words:
        if not word or len(word) < 2:
            continue
        pattern = _re.compile(r'(\b' + _re.escape(word) + r'\b)', _re.IGNORECASE)
        result = pattern.sub(
            r'<span style="background: rgba(77,163,255,0.2); color: #4da3ff; padding: 1px 4px; border-radius: 3px;">\1</span>',
            result,
            count=1
        )

    return result


def render_vocabulary_tab(data):
    """Render the GRE Vocabulary Matrix tab."""
    if "error" in data:
        st.error(f"Vocabulary Error: {data.get('error')}")
        if "raw_response" in data:
            with st.expander("📄 Raw Response"):
                st.text(data["raw_response"])
        return

    matrix = data.get("vocabulary_matrix", [])
    if not matrix:
        st.warning("No vocabulary data found.")
        return

    # Stats
    total = data.get("total_words_analyzed", len(matrix))
    dist = data.get("tier_distribution", {})

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Total Words", total)
    with col2:
        st.metric("🟢 Essential", dist.get("essential", 0))
    with col3:
        st.metric("🟠 Advanced", dist.get("advanced_editorial", 0))
    with col4:
        st.metric("🔴 Mastery", dist.get("mastery", 0))

    st.markdown("---")

    # View Mode Toggle
    view_mode = st.radio(
        "View Mode:",
        ["📊 Table View", "🃏 Flashcard Mode", "📋 Detailed Cards"],
        horizontal=True,
        key="vocab_view_mode"
    )

    if view_mode == "📊 Table View":
        render_vocab_table(matrix)
    elif view_mode == "🃏 Flashcard Mode":
        render_flashcards(matrix)
    else:
        render_vocab_cards(matrix)

    # CSV Download
    st.markdown("---")
    csv_data = VocabularyProcessor(None).generate_csv_data(data) if data else ""
    if csv_data:
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="textcraft_vocabulary.csv",
            mime="text/csv",
            use_container_width=True
        )


def render_vocab_table(matrix):
    """Render vocabulary as a table."""
    for item in matrix:
        tier = item.get("frequency_tier", "")
        emoji = Utils.get_tier_emoji(tier)
        synonyms = ", ".join([s.get("word", "") for s in item.get("gre_synonyms", [])])
        antonyms = ", ".join(item.get("antonyms", []))

        st.markdown(f"""
        <div class="info-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0;">
                    {item.get('basic_word', '')} → <span style="color: #ffd93d;">{item.get('article_word', '')}</span>
                </h3>
                <span>{emoji} {tier}</span>
            </div>
            <p><strong>Part of Speech:</strong> {item.get('part_of_speech', '')}</p>
            <p><strong>🇧🇩 বাংলা:</strong> {item.get('bangla_meaning', '')}</p>
            <p><strong>🇬🇧 Definition:</strong> {item.get('english_definition', '')}</p>
            <p><strong>🎵 Pronunciation:</strong> <code>{item.get('pronunciation', '')}</code></p>
            <p><strong>📖 Root/Etymology:</strong> {item.get('root_etymology', '')}</p>
            <p><strong>🧠 Mnemonic:</strong> {item.get('mnemonic', '')}</p>
            <p><strong>🧠 মনে রাখার কৌশল:</strong> {item.get('mnemonic_bn', '')}</p>
            <p><strong>✅ GRE Synonyms:</strong> {synonyms}</p>
            <p><strong>❌ Antonyms:</strong> {antonyms}</p>
            <p><strong>📝 Example:</strong> <em>{item.get('example_sentence', '')}</em></p>
            <p style="color: #666; font-size: 0.85rem;"><strong>📌 Article Context:</strong> <em>{item.get('article_sentence', '')}</em></p>
        </div>
        """, unsafe_allow_html=True)

        # Show synonym nuances
        if item.get("gre_synonyms"):
            with st.expander(f"🔬 Synonym Nuances for '{item.get('article_word', '')}'"):
                for syn in item["gre_synonyms"]:
                    st.markdown(f"""
                    - **{syn.get('word', '')}**: {syn.get('nuance', '')}
                      - 🇧🇩 {syn.get('nuance_bn', '')}
                    """)


def render_flashcards(matrix):
    """Render flashcard mode."""
    if not matrix:
        return

    total = len(matrix)
    idx = st.session_state.flashcard_index % total

    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if st.button("⬅️ Previous", use_container_width=True):
            st.session_state.flashcard_index = (idx - 1) % total
            st.session_state.flashcard_flipped = False
            st.rerun()

    with col3:
        if st.button("➡️ Next", use_container_width=True):
            st.session_state.flashcard_index = (idx + 1) % total
            st.session_state.flashcard_flipped = False
            st.rerun()

    with col2:
        st.markdown(f"**Card {idx + 1} of {total}**")

    item = matrix[idx]

    if st.button("🔄 Flip Card", use_container_width=True, key="flip_btn"):
        st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
        st.rerun()

    if not st.session_state.flashcard_flipped:
        # Front of card
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #2a3a4a, #1e2a3a);
                    border: 2px solid rgba(255, 107, 107, 0.3);
                    border-radius: 15px; padding: 3rem; text-align: center;
                    min-height: 200px; display: flex; flex-direction: column;
                    align-items: center; justify-content: center;">
            <div style="font-size: 2.5rem; color: #FF6B6B; font-weight: bold; margin-bottom: 1rem;">
                {item.get('article_word', '')}
            </div>
            <div style="color: #666; font-size: 0.9rem;">
                ({item.get('part_of_speech', '')}) • {Utils.get_tier_emoji(item.get('frequency_tier', ''))} {item.get('frequency_tier', '')}
            </div>
            <div style="color: #888; font-size: 0.85rem; margin-top: 1rem;">
                Click "Flip Card" to see the meaning ↕️
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Back of card
        synonyms = ", ".join([s.get("word", "") for s in item.get("gre_synonyms", [])])
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1e2a3a, #162030);
                    border: 2px solid rgba(255, 217, 61, 0.3);
                    border-radius: 15px; padding: 2rem; text-align: center;
                    min-height: 200px;">
            <div style="font-size: 1.5rem; color: #ffd93d; font-weight: bold; margin-bottom: 0.5rem;">
                {item.get('article_word', '')}
            </div>
            <div style="color: #d0d0d0; font-size: 1rem; margin: 0.5rem 0;">
                🇧🇩 {item.get('bangla_meaning', '')}
            </div>
            <div style="color: #a0a0a0; font-size: 0.9rem; margin: 0.5rem 0;">
                🇬🇧 {item.get('english_definition', '')}
            </div>
            <div style="color: #888; font-size: 0.85rem; margin: 0.5rem 0;">
                🎵 {item.get('pronunciation', '')}
            </div>
            <div style="color: #28a745; font-size: 0.85rem; margin: 0.5rem 0;">
                📖 {item.get('root_etymology', '')}
            </div>
            <div style="color: #fd7e14; font-size: 0.85rem; margin: 0.5rem 0;">
                🧠 {item.get('mnemonic', '')}
            </div>
            <div style="color: #4da3ff; font-size: 0.85rem; margin: 0.5rem 0;">
                ✅ Synonyms: {synonyms}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_vocab_cards(matrix):
    """Render detailed vocabulary cards."""
    for i, item in enumerate(matrix):
        with st.expander(
            f"{Utils.get_tier_emoji(item.get('frequency_tier', ''))} "
            f"**{item.get('article_word', '')}** — {item.get('bangla_meaning', '')}",
            expanded=(i == 0)
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Basic Word:** {item.get('basic_word', '')}")
                st.markdown(f"**Article Word:** `{item.get('article_word', '')}`")
                st.markdown(f"**Part of Speech:** {item.get('part_of_speech', '')}")
                st.markdown(f"**Pronunciation:** `{item.get('pronunciation', '')}`")
                st.markdown(f"**Tier:** {item.get('frequency_tier', '')}")
            with col2:
                st.markdown(f"**🇧🇩 বাংলা অর্থ:** {item.get('bangla_meaning', '')}")
                st.markdown(f"**🇬🇧 Definition:** {item.get('english_definition', '')}")
                st.markdown(f"**📖 Root:** {item.get('root_etymology', '')}")
                st.markdown(f"**🧠 Mnemonic:** {item.get('mnemonic', '')}")

            st.markdown(f"**📝 Example:** *{item.get('example_sentence', '')}*")
            st.markdown(f"**📌 Context:** *{item.get('article_sentence', '')}*")

            if item.get("gre_synonyms"):
                st.markdown("**GRE Synonyms with Nuances:**")
                for syn in item["gre_synonyms"]:
                    st.markdown(f"  - **{syn.get('word', '')}**: {syn.get('nuance', '')} / {syn.get('nuance_bn', '')}")


def render_clause_tab(data):
    """Render the comprehensive Clause & Grammar X-Ray tab (15+ sentences)."""
    if "error" in data:
        st.error(f"Clause Analysis Error: {data.get('error')}")
        if "raw_response" in data:
            with st.expander("📄 Raw Response"):
                st.text(data["raw_response"])
        return

    # Stats header
    total = data.get("total_sentences_in_article", "N/A")
    analyzed = data.get("sentences_analyzed", "N/A")
    st.markdown(f"""
    <div class="info-card">
        <h3>📊 Analysis Coverage</h3>
        <p>Total sentences in article: <strong>{total}</strong> | Sentences analyzed: <strong>{analyzed}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Overall Style Profile
    profile = data.get("overall_style_profile", {})
    if profile:
        st.markdown("---")
        st.subheader("📊 Overall Style Profile")

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Avg Clauses/Sentence", profile.get("average_clauses_per_sentence", "N/A"))
        with c2: st.metric("Avg Sentence Length", f"{profile.get('average_sentence_length', 'N/A')} words")
        with c3: st.metric("Longest Sentence", f"{profile.get('longest_sentence_word_count', 'N/A')} words")
        with c4: st.metric("Difficulty", profile.get("difficulty_level", "N/A"))

        st.markdown(f"""
        <div class="info-card">
            <p>🇬🇧 {profile.get('style_description', 'N/A')}</p>
            <p style="color: #a0a0a0;">🇧🇩 {profile.get('style_description_bn', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

        if profile.get("dominant_clause_patterns"):
            st.markdown("**🔗 Dominant Patterns:**")
            for p in profile["dominant_clause_patterns"]:
                st.markdown(f"  • {p}")

        if profile.get("most_common_connectors"):
            st.markdown(f"**🔗 Common Connectors:** {', '.join(profile['most_common_connectors'])}")

        if profile.get("writing_lessons"):
            with st.expander("🎓 Writing Lessons from This Article"):
                lessons_en = profile.get("writing_lessons", [])
                lessons_bn = profile.get("writing_lessons_bn", [])
                for i, lesson in enumerate(lessons_en):
                    st.markdown(f"**{i+1}.** {lesson}")
                    if i < len(lessons_bn):
                        st.markdown(f"   🇧🇩 *{lessons_bn[i]}*")

    st.markdown("---")

    # Individual Sentence Analysis
    st.subheader("🔬 Sentence-by-Sentence X-Ray")
    analyses = data.get("clause_analysis", [])

    for idx, analysis in enumerate(analyses):
        sent_num = analysis.get("sentence_number", idx + 1)
        word_count = analysis.get("sentence_length_words", "")

        with st.expander(
            f"📝 Sentence #{sent_num} ({word_count} words) — "
            f"{analysis.get('syntactic_formula', '')[:60]}...",
            expanded=(idx < 3)  # First 3 expanded by default
        ):
            # Original sentence
            st.markdown(f"""
            <div class="clause-box">
                <p style="color: #ffd93d; font-size: 1.05rem; line-height: 1.8;">
                    "{analysis.get('original_sentence', '')}"
                </p>
                <p style="color: #888;">
                    <strong>Formula:</strong> <code>{analysis.get('syntactic_formula', '')}</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Clause Breakdown
            st.markdown("**📐 Clause Breakdown:**")
            for clause in analysis.get("clause_breakdown", []):
                ct = clause.get("clause_type", "")
                css = "clause-independent"
                if "subordinate" in ct.lower() or "adverbial" in ct.lower():
                    css = "clause-subordinate"
                elif "relative" in ct.lower() or "adjective" in ct.lower():
                    css = "clause-relative"
                elif "participial" in ct.lower():
                    css = "clause-participial"

                st.markdown(f"""
                <div style="margin: 0.5rem 0; padding: 0.8rem; background: rgba(255,255,255,0.03); border-radius: 8px;">
                    <span class="clause-tag {css}">{ct}</span>
                    <span class="clause-tag" style="background: rgba(255,255,255,0.05); color: #a0a0a0;">{clause.get('clause_type_bn', '')}</span>
                    <p style="color: #d0d0d0; margin: 0.5rem 0;">📝 <em>"{clause.get('clause_text', '')}"</em></p>
                    <p style="color: #888; font-size: 0.85rem;">🔧 {clause.get('function', '')}</p>
                    <p style="color: #888; font-size: 0.85rem;">🇧🇩 {clause.get('function_bn', '')}</p>
                    {f'<p style="color: #4da3ff; font-size: 0.85rem;">🔗 Connector: <code>{clause.get("connector", "")}</code></p>' if clause.get("connector") else ''}
                    {f'<p style="color: #28a745; font-size: 0.85rem;">📖 {clause.get("grammar_note", "")}</p>' if clause.get("grammar_note") else ''}
                    {f'<p style="color: #28a745; font-size: 0.85rem;">🇧🇩 {clause.get("grammar_note_bn", "")}</p>' if clause.get("grammar_note_bn") else ''}
                </div>
                """, unsafe_allow_html=True)

            # Beginner vs Editorial
            col_beg, col_ed = st.columns(2)
            beginner = analysis.get("beginner_version", {})
            editorial = analysis.get("editorial_technique", {})

            with col_beg:
                st.markdown("**❌ Beginner Version:**")
                for sent in beginner.get("sentences", []):
                    st.markdown(f"  • *{sent}*")
                st.markdown(f"  🇧🇩 *{beginner.get('explanation_bn', beginner.get('explanation', ''))}*")

            with col_ed:
                st.markdown(f"**✅ {editorial.get('technique_name', 'Editorial Technique')}:**")
                st.markdown(f"🇧🇩 {editorial.get('technique_name_bn', '')}")
                st.markdown(f"{editorial.get('explanation', '')}")
                st.markdown(f"🇧🇩 *{editorial.get('explanation_bn', '')}*")
                if editorial.get("stylistic_devices"):
                    st.markdown(f"Devices: {', '.join(editorial['stylistic_devices'])}")
                if editorial.get("impact_on_reader"):
                    st.markdown(f"🎯 Impact: {editorial['impact_on_reader']}")
                    st.markdown(f"🇧🇩 {editorial.get('impact_on_reader_bn', '')}")

            # Deep dive
            if analysis.get("grammar_deep_dive_bn"):
                st.info(f"📝 **গভীর ব্যাকরণ বিশ্লেষণ:** {analysis['grammar_deep_dive_bn']}")

            # Replication template
            if analysis.get("replication_template"):
                st.markdown(f"**🔧 Replication Template:** `{analysis['replication_template']}`")
                if analysis.get("replication_template_bn"):
                    st.markdown(f"🇧🇩 {analysis['replication_template_bn']}")

        st.markdown("---")


def render_writing_tab(data):
    """Render the Writing Masterclass tab."""
    if "error" in data:
        st.error(f"Writing Program Error: {data.get('error')}")
        if "raw_response" in data:
            with st.expander("📄 Raw Response"):
                st.text(data["raw_response"])
        return

    mc = data.get("masterclass", {})

    # Overview
    st.markdown(f"""
    <div class="info-card">
        <h3>🎓 Masterclass Overview</h3>
        <p>🇬🇧 {mc.get('overview', 'N/A')}</p>
        <p style="color: #a0a0a0; font-style: italic;">🇧🇩 {mc.get('overview_bn', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Steps
    st.subheader("📶 Step-by-Step Writing Blueprint")

    step_colors = ["#28a745", "#17a2b8", "#ffc107", "#fd7e14", "#FF6B6B"]

    for step in mc.get("steps", []):
        num = step.get("step_number", 0)
        color = step_colors[(num - 1) % len(step_colors)]

        st.markdown(f"""
        <div class="step-card step-{num}" style="border-left-color: {color};">
            <h3 style="color: {color};">Step {num}: {step.get('step_name', '')} | {step.get('step_name_bn', '')}</h3>
            <p>🇬🇧 {step.get('description', '')}</p>
            <p style="color: #a0a0a0; font-style: italic;">🇧🇩 {step.get('description_bn', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Example from article
        example = step.get("example_from_article", {})
        if example:
            with st.expander(f"📝 Example from Article - Step {num}"):
                if "original" in example:
                    st.markdown(f"**Original:** *{example['original']}*")
                if "stripped" in example:
                    st.markdown(f"**Stripped/Basic:** *{example['stripped']}*")
                if "stripped_bn" in example:
                    st.markdown(f"**🇧🇩:** *{example['stripped_bn']}*")
                if "basic" in example:
                    st.markdown(f"**Basic Version:** *{example['basic']}*")
                if "elevated" in example:
                    st.markdown(f"**Elevated Version:** *{example['elevated']}*")
                if "words_changed" in example:
                    st.markdown("**Words Changed:**")
                    for wc in example["words_changed"]:
                        st.markdown(f"  • `{wc.get('from', '')}` → `{wc.get('to', '')}` — {wc.get('why', '')} / {wc.get('why_bn', '')}")
                if "simple_sentences" in example:
                    st.markdown("**Simple Sentences:**")
                    for ss in example["simple_sentences"]:
                        st.markdown(f"  • *{ss}*")
                if "combined" in example:
                    st.markdown(f"**Combined:** *{example['combined']}*")
                if "technique" in example:
                    st.markdown(f"**Technique:** {example['technique']} / {example.get('technique_bn', '')}")

                # Devices found (for step 4)
                if step.get("devices_found"):
                    st.markdown("**Stylistic Devices Found:**")
                    for device in step["devices_found"]:
                        st.markdown(f"""
                        - **{device.get('device', '')}** ({device.get('device_bn', '')})
                          - Example: *{device.get('example', '')}*
                          - Effect: {device.get('effect', '')}
                          - 🇧🇩 {device.get('effect_bn', '')}
                        """)

                # Cohesion devices (for step 5)
                if step.get("cohesion_devices_used"):
                    st.markdown("**Cohesion Devices Used:**")
                    for cd in step["cohesion_devices_used"]:
                        st.markdown(f"  - **{cd.get('device', '')}** ({cd.get('device_bn', '')}): *{cd.get('example', '')}*")

        # Practice exercise
        if step.get("practice_exercise"):
            with st.expander(f"🏋️ Practice Exercise - Step {num}"):
                st.markdown(f"🇬🇧 {step['practice_exercise']}")
                if step.get("practice_exercise_bn"):
                    st.markdown(f"🇧🇩 {step['practice_exercise_bn']}")

    st.markdown("---")

    # Clause Templates
    st.subheader("🔧 Plug-and-Play Clause Templates")
    templates = mc.get("clause_templates", [])
    for tmpl in templates:
        st.markdown(f"""
        <div class="template-card">
            <h4 style="color: #FF6B6B;">{tmpl.get('template_name', '')} | {tmpl.get('template_name_bn', '')}</h4>
            <p><strong>Formula:</strong> <code>{tmpl.get('formula', '')}</code></p>
            <p><strong>Example:</strong> <em>{tmpl.get('example', '')}</em></p>
            <p><strong>Use When:</strong> {tmpl.get('use_case', '')}</p>
            <p style="color: #a0a0a0;">🇧🇩 {tmpl.get('use_case_bn', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Editorial Checklist
    st.subheader("✅ Editorial Checklist")
    st.markdown("*Use this to evaluate your own writing:*")

    checklist = mc.get("editorial_checklist", [])
    completed = 0
    for i, item in enumerate(checklist):
        key = f"check_{i}"
        if key not in st.session_state.checklist_state:
            st.session_state.checklist_state[key] = False

        checked = st.checkbox(
            f"**{item.get('item', '')}** | {item.get('item_bn', '')} [{item.get('category', '')}]",
            value=st.session_state.checklist_state[key],
            key=key
        )
        st.session_state.checklist_state[key] = checked
        if checked:
            completed += 1

    if checklist:
        progress = completed / len(checklist)
        st.progress(progress, text=f"Completed: {completed}/{len(checklist)} ({progress*100:.0f}%)")


def render_transformer_tab():
    """Render the Sentence Transformer Lab tab."""
    st.subheader("🔄 Live Sentence Transformer Lab")
    st.markdown("""
    আপনার যেকোনো সাধারণ বাক্য বা কাঁচা ভাব ইনপুট দিন। সিস্টেম এটিকে ৪টি স্তরে রূপান্তর করে দেখাবে।
    
    *Enter any basic sentence or raw idea. The system will transform it through 4 levels of sophistication.*
    """)

    default_text = "Air pollution is rising in big cities. It causes sickness. Government must ban unfit cars."
    raw_input = st.text_area(
        "✍️ Enter your raw sentence(s):",
        value="",
        placeholder=default_text,
        height=120,
        key="transformer_input"
    )

    if st.button("🚀 Transform!", use_container_width=True, key="transform_btn"):
        if not raw_input.strip():
            st.warning("Please enter some text to transform.")
            return

        client = get_client()
        if not client:
            st.error("Please set your Gemini API key in the sidebar.")
            return

        transformer = SentenceTransformer(client)

        with st.spinner("🔄 Transforming through 4 levels..."):
            result = transformer.transform(raw_input.strip())

        if "error" in result:
            st.error(f"Transformation Error: {result.get('error')}")
            if "raw_response" in result:
                with st.expander("📄 Raw Response"):
                    st.text(result["raw_response"])
            return

        st.session_state["transformer_result"] = result

    # Display results
    if "transformer_result" in st.session_state:
        result = st.session_state["transformer_result"]

        st.markdown(f"""
        <div class="info-card">
            <h3>📥 Original Input</h3>
            <p>"{result.get('original_input', '')}"</p>
        </div>
        """, unsafe_allow_html=True)

        level_styles = [
            ("#28a745", "level-1", "🟢"),
            ("#ffc107", "level-2", "🟡"),
            ("#007bff", "level-3", "🔵"),
            ("#FF6B6B", "level-4", "🔴"),
        ]

        for t in result.get("transformations", []):
            lvl = t.get("level", 1)
            color, css, emoji = level_styles[(lvl - 1) % 4]

            chars = t.get("characteristics", [])
            chars_bn = t.get("characteristics_bn", [])

            st.markdown(f"""
            <div class="level-card {css}">
                <div class="level-badge" style="background: {color}; color: white;">
                    Level {lvl}
                </div>
                <h4 style="color: {color};">{emoji} {t.get('level_name', '')} | {t.get('level_name_bn', '')}</h4>
                <p style="color: #d0d0d0; line-height: 1.8; font-size: 1rem; margin: 1rem 0;">
                    "{t.get('text', '')}"
                </p>
                <p style="color: #888; font-size: 0.85rem;">
                    📊 Words: {t.get('word_count', 'N/A')} |
                    Features: {', '.join(chars)}
                </p>
                <p style="color: #666; font-size: 0.8rem;">
                    🇧🇩 বৈশিষ্ট্য: {', '.join(chars_bn)}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Level 4 Analysis
        l4 = result.get("level_4_analysis", {})
        if l4:
            st.markdown("---")
            st.subheader("🔬 Level 4 Deep Analysis")

            # Clause breakdown
            if l4.get("clause_breakdown"):
                st.markdown("**📐 Clause Breakdown:**")
                for cb in l4["clause_breakdown"]:
                    st.markdown(f"""
                    - `{cb.get('clause_type', '')}` ({cb.get('clause_type_bn', '')}): *"{cb.get('clause_text', '')}"*
                    """)

            # GRE words used
            if l4.get("gre_words_used"):
                st.markdown("**📚 GRE Words Used:**")
                for gw in l4["gre_words_used"]:
                    st.markdown(f"""
                    - **{gw.get('word', '')}** (🇧🇩 {gw.get('meaning_bn', '')}) — replaced `{gw.get('replaced_from', '')}`
                    """)

            # Techniques applied
            if l4.get("techniques_applied"):
                st.markdown("**⚡ Techniques Applied:**")
                for ta in l4["techniques_applied"]:
                    st.markdown(f"""
                    - **{ta.get('technique', '')}** ({ta.get('technique_bn', '')}): {ta.get('example', '')}
                    """)


# ============================================
# Main Application
# ============================================
def main():
    render_header()

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Settings")

        # API Key
        api_key = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            value=st.session_state.api_key,
            placeholder="Enter your Google Gemini API key",
            help="Get your free API key from https://aistudio.google.com/apikey"
        )
        st.session_state.api_key = api_key

        if api_key:
            st.success("✅ API Key set!")
        else:
            st.warning("⚠️ Please enter your Gemini API key")
            st.markdown("[🔗 Get Free API Key](https://aistudio.google.com/apikey)")

        st.markdown("---")
        st.markdown("## 📖 How to Use")
        st.markdown("""
        1. **Enter API Key** above
        2. **Paste text**, upload PDF, or enter URL
        3. Click **Deconstruct & Analyze**
        4. Explore all **5 tabs**
        5. Use **Sentence Transformer** to practice
        """)

        st.markdown("---")
        st.markdown("## 📋 Quick Samples")
        for name, text in QUICK_SAMPLES.items():
            if st.button(name, use_container_width=True, key=f"sample_{name}"):
                st.session_state.input_text = text
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p>Made with ❤️ by TextCraft</p>
            <p>Powered by Google Gemini</p>
        </div>
        """, unsafe_allow_html=True)

    # Main Content Area
    st.subheader("📥 Input Your Text")

    input_method = st.radio(
        "Choose input method:",
        ["📝 Paste Text", "📄 Upload PDF", "🌐 Enter URL"],
        horizontal=True,
        key="input_method"
    )

    article_text = ""

    if input_method == "📝 Paste Text":
        article_text = st.text_area(
            "Paste your article here:",
            value=st.session_state.input_text,
            height=250,
            placeholder="Paste any article, essay, or text here for analysis...",
            key="text_input"
        )

    elif input_method == "📄 Upload PDF":
        uploaded_file = st.file_uploader("Upload PDF file:", type=["pdf"])
        if uploaded_file:
            if PDFHandler.is_available():
                with st.spinner("📄 Extracting text from PDF..."):
                    text = PDFHandler.extract_text(uploaded_file.read())
                    if text:
                        article_text = text
                        st.success(f"✅ Extracted {Utils.word_count(text)} words from PDF")
                        with st.expander("Preview extracted text"):
                            st.text(text[:2000] + ("..." if len(text) > 2000 else ""))
                    else:
                        st.error("❌ Could not extract text from PDF. Try pasting text directly.")
            else:
                st.error("❌ PyPDF2 not installed. Please install: `pip install PyPDF2`")

    elif input_method == "🌐 Enter URL":
        url = st.text_input(
            "Enter article URL:",
            placeholder="https://www.example.com/article",
            key="url_input"
        )
        if url:
            if URLHandler.is_available():
                if Utils.is_valid_url(url):
                    with st.spinner("🌐 Fetching article from URL..."):
                        text = URLHandler.extract_text(url)
                        if text:
                            article_text = text
                            st.success(f"✅ Extracted {Utils.word_count(text)} words from URL")
                            with st.expander("Preview extracted text"):
                                st.text(text[:2000] + ("..." if len(text) > 2000 else ""))
                        else:
                            st.error("❌ Could not extract text from URL. Try pasting text directly.")
                else:
                    st.error("❌ Invalid URL format. Please enter a valid URL starting with http:// or https://")
            else:
                st.error("❌ Required packages not installed. Please install: `pip install requests beautifulsoup4 lxml`")

    # Analyze Button
    st.markdown("---")

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        analyze_clicked = st.button(
            "🔬 Deconstruct & Analyze",
            use_container_width=True,
            type="primary",
            key="analyze_btn"
        )
    with col_btn2:
        if st.button("🗑️ Clear All", use_container_width=True, key="clear_btn"):
            st.session_state.analysis_results = {}
            st.session_state.input_text = ""
            if "transformer_result" in st.session_state:
                del st.session_state["transformer_result"]
            st.rerun()

    # Run Analysis
    if analyze_clicked:
        if not article_text.strip():
            st.error("❌ Please provide text to analyze!")
        elif not st.session_state.api_key:
            st.error("❌ Please enter your Gemini API key in the sidebar!")
        else:
            client = get_client()
            if not client:
                st.error("❌ Failed to initialize Gemini client.")
            else:
                processed_text = Utils.truncate_text(article_text.strip())

                progress_bar = st.progress(0, text="Starting analysis...")
                results = {}

                # Step 1: 5W1H
                progress_bar.progress(10, text="📊 Analyzing 5W1H Information Matrix...")
                analyzer = ArticleAnalyzer(client)
                results["5w1h"] = analyzer.analyze_5w1h(processed_text)

                # Step 2: Vocabulary
                progress_bar.progress(35, text="📚 Extracting GRE Vocabulary Matrix...")
                vocab_proc = VocabularyProcessor(client)
                results["vocabulary"] = vocab_proc.extract_vocabulary(processed_text)

                # Step 3: Clause X-Ray
                progress_bar.progress(60, text="🔬 Performing Clause & Grammar X-Ray...")
                clause_xray = ClauseXRay(client)
                results["clauses"] = clause_xray.analyze_clauses(processed_text)

                # Step 4: Writing Program
                progress_bar.progress(85, text="🎓 Generating Writing Masterclass Blueprint...")
                writing = WritingProgram(client)
                results["writing"] = writing.generate_masterclass(processed_text)

                progress_bar.progress(100, text="✅ Analysis Complete!")
                time.sleep(0.5)
                progress_bar.empty()

                st.session_state.analysis_results = results
                st.success("🎉 Full analysis complete! Explore the tabs below.")

    # Results Tabs
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 1. Basic Info & 5W1H",
            "📚 2. GRE Vocabulary",
            "🔬 3. Clause X-Ray",
            "🎓 4. Writing Program",
            "🔄 5. Transformer Lab"
        ])

        with tab1:
            if "5w1h" in results:
                render_5w1h_tab(results["5w1h"])

        with tab2:
            if "vocabulary" in results:
                render_vocabulary_tab(results["vocabulary"])

        with tab3:
            if "clauses" in results:
                render_clause_tab(results["clauses"])

        with tab4:
            if "writing" in results:
                render_writing_tab(results["writing"])

        with tab5:
            render_transformer_tab()

    else:
        # Show transformer tab even without analysis
        st.markdown("---")
        with st.expander("🔄 Quick Access: Sentence Transformer Lab", expanded=False):
            render_transformer_tab()


if __name__ == "__main__":
    main()
    # Results Tabs
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results

        # ========================================================
        # 📥 ALL-IN-ONE PDF EXPORT BUTTON
        # ========================================================
        st.markdown("---")
        pdf_col1, pdf_col2 = st.columns([3, 1])
        with pdf_col1:
            st.markdown("### 📑 Full Masterclass PDF Export")
            st.markdown("*সম্পূর্ণ অ্যানালাইসিস, ভোকাবুলারি, ক্লজ ব্যবচ্ছেদ ও রাইটিং ব্লুপ্রিন্ট একটি প্রফেশনাল PDF ফাইলে ডাউনলোড করুন।*")
        
        with pdf_col2:
            try:
                from modules.pdf_generator import TextCraftPDFReport
                pdf_gen = TextCraftPDFReport()
                
                # Check if transformer results exist
                tr_res = st.session_state.get("transformer_result", None)
                pdf_bytes = pdf_gen.generate(results, tr_res)

                st.download_button(
                    label="📥 Download Full PDF Report",
                    data=pdf_bytes,
                    file_name="TextCraft_Masterclass_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.error(f"PDF তৈরি করতে সমস্যা হয়েছে: {e}")

        st.markdown("---")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 1. Basic Info & 5W1H",
            "📚 2. GRE Vocabulary",
            "🔬 3. Clause X-Ray",
            "🎓 4. Writing Program",
            "🔄 5. Transformer Lab"
        ])
st.markdown("---")
st.markdown("### 💬 Feedback")
feedback = st.text_area("আপনার মতামত দিন (বাগ রিপোর্ট / ফিচার রিকোয়েস্ট):")
if st.button("Submit Feedback"):
    st.success("ধন্যবাদ! আপনার ফিডব্যাক পেয়েছি। 🙏")