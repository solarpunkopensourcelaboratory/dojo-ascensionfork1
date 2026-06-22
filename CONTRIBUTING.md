# 🌱 Contributing to Dojo Ascension

Welcome, fellow cultivator of code and community. Whether you're a beginner learning Python or an experienced developer, your contributions help grow this learning ecosystem.

**Dojo Ascension v5.0** is built on the belief that code is not syntax—it's a framework for thinking about systems. We welcome contributions that expand the curriculum, improve the engine, and strengthen the community.

---

## 🎯 How You Can Contribute

### 1. **Add a Mission** (Easiest!)

Non-programmers and subject-matter experts are welcome here. If you understand a concept deeply—whether it's Git, web scraping, data analysis, genealogy research, or journalism—you can contribute a mission.

**Mission writers do NOT need to know Python.** You only need to:
- Understand your topic
- Write it clearly
- Follow the JSON mission format (see below)
- Test it locally (one command)

### 2. **Improve Existing Missions**

- Fix typos, clarify explanations
- Add hints or better analogies
- Adjust honor rewards based on difficulty
- Propose reflective questions

### 3. **Code Contributions**

- Bug fixes
- Performance improvements
- New features (e.g., offline mode, dashboard enhancements)
- Testing and quality assurance

### 4. **Documentation & Translation**

- Improve README, guides, examples
- Translate missions into other languages
- Create video walkthroughs
- Write blog posts about the Dojo philosophy

---

## 📝 How to Add a Mission

### The Mission JSON Format

All missions live in `missions.json`. To add a new mission, add a JSON object to the `"missions"` array.

#### Minimal Example

```json
{
  "id": "git_remote_collaboration",
  "number": 11,
  "title": "Remote Collaboration with Git",
  "philosophy": "Your philosophy anchor here.",
  "economics": "Your economic parallel here.",
  "tech_concept": "The actual technical explanation.",
  "challenge": "The question or task prompt.",
  "answer": "git push origin main",
  "skill": "git",
  "honor_base": 20
}
```

#### Full Schema Documentation

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ Yes | **Stable identifier** — never changes. Format: `lowercase_with_underscores`. Example: `python_list_comprehension`, `json_parsing_api_response` |
| `number` | integer | ✅ Yes | Sequence number in curriculum. Can be 1-100+. If you add mission 11, use `11`. |
| `title` | string | ✅ Yes | Mission title. Keep it under 50 characters. Example: `"APIs & HTTP"` |
| `philosophy` | string | ✅ Yes | Cross-disciplinary anchor (martial arts, theatre, economics, activism, history). 2-4 sentences. This is where you connect code to the human world. |
| `economics` | string | ✅ Yes | How this concept relates to resource management, infrastructure, governance, or markets. 2-3 sentences. |
| `tech_concept` | string | ✅ Yes | The actual technical explanation without jargon. Show a brief code example if helpful. |
| `challenge` | string | ✅ Yes | The question or prompt the learner will answer. Can be a question, instruction, or scenario. |
| `answer` | string | ✅ Yes | The expected answer (case-insensitive, whitespace-flexible). Can be partial match (e.g., user types "def" and we check if "def" is in their input). |
| `skill` | string | ✅ Yes | Domain this teaches: `python`, `git`, `json`, `architecture`, `review`, or another lowercase domain name |
| `honor_base` | integer | ✅ Yes | Base honor points (typically 15-30). Harder missions earn more. |
| `hint` | string | ⚠️ Optional | A helpful hint revealed after 3 failed attempts. |
| `learning_level` | string | ⚠️ Optional | Cognitive complexity: `recall`, `application`, `analysis`, or `reflection`. Helps learners understand progression. |

#### Real Examples from the Core Curriculum

**Example 1: Simple Recall**
```json
{
  "id": "git_system_grounding",
  "number": 1,
  "title": "System Grounding",
  "philosophy": "Like Tai Chi, where you must feel the ground before moving, a programmer must understand their environment. 'Wu Wei' is achieved when your tools become extensions of your mind.",
  "economics": "Infrastructure is the basis of all macro-economic stability. Before building goods, we build roads. Here, your terminal and shell are your economic infrastructure.",
  "tech_concept": "The terminal. Git is our tool for interacting with the open-source global supply chain of ideas.",
  "challenge": "Type the command to clone a git repository.",
  "answer": "git clone",
  "skill": "git",
  "honor_base": 20
}
```

**Example 2: Multiple Acceptable Answers**
```json
{
  "id": "python_variables",
  "number": 2,
  "title": "Variables & Data Lineage",
  "philosophy": "Genealogy teaches us that tracing lineage reveals identity. A variable is a named vessel; its lineage of data determines its behavior in the ecosystem.",
  "economics": "Micro-economics dictates that resources are scarce. Variables allocate memory—our most precious digital resource. Good naming prevents systemic inflation.",
  "tech_concept": "In Python, we assign values using the '=' operator. E.g., `water_supply = 100`.",
  "challenge": "Write exactly this: assign the integer 42 to a variable named 'seed'.",
  "answer": "seed = 42",
  "skill": "python",
  "honor_base": 15,
  "hint": "Format: variable_name = value"
}
```

---

## ✍️ Writing Your Mission

### Philosophy Anchor (the heart of the mission)

Connect the code to something meaningful. Examples:
- **Martial Arts**: Wu Wei (effortlessness), Jeet Kune Do (efficiency), BJJ (collaboration)
- **History/Politics**: Estonia's e-governance, Cornel West's justice, activism and accountability
- **Theatre**: Uta Hagen's acting techniques, roles and characters, improvisation
- **Economics**: Resource scarcity, infrastructure, markets, supply chains
- **Your field**: Journalism, genealogy, biology, music, climate science—bring your expertise

**Why?** Learners remember code better when it connects to ideas they already care about.

### Economics Parallel

How does this concept relate to real-world resource management or infrastructure? Examples:
- **Variables** → "Resources are scarce; memory allocation prevents inflation"
- **Git Commits** → "Ledgers hold institutions accountable; immutability prevents corruption"
- **Functions** → "Factories take raw inputs and produce finished goods; reuse prevents waste"
- **APIs** → "Open data democratizes power; closed APIs create monopolies"

**Why?** This frames code as part of larger systems—not isolated syntax.

### Technical Concept

Keep it simple. Use plain language. If you use code examples, make them brief. Don't assume learners know advanced topics yet.

### Challenge

Write a clear, unambiguous prompt. Can be:
- A question: `"What keyword is used to define a function?"`
- An instruction: `"Write a print() statement that outputs your name."`
- A scenario: `"You are a Git maintainer. What command isolates your experimental branch?"`

### Answer

Keep it short. The engine checks for **substring match** (case-insensitive). So:
- `"answer": "def"` matches "def", "DEF", "def is the keyword", "define using def"
- `"answer": "git clone"` matches "git clone", "git clone my-repo", "GIT CLONE"

If the answer needs to be exact (e.g., `seed = 42`), note that in the challenge itself: *"Write exactly this..."*

### Hint

Optional but powerful. Hints appear after 3 failed attempts. They should:
- Point toward the concept, not give the answer
- Examples:
  - Challenge: "What does JSON stand for?"  Hint: "Think of the initials: J_S_O_N"
  - Challenge: "Create a list with 3 numbers"  Hint: "Use square brackets: [1, 2, 3]"

---

## 🧪 Testing Your Mission Locally

1. **Edit `missions.json`** — Add your mission object to the `"missions"` array.

2. **Run the Dojo:**
   ```bash
   python dojo_classroom.py
   ```

3. **Navigate to your mission:**
   - Choose option 2 (Choose Specific Mission)
   - Enter your mission number (e.g., 11)

4. **Test the challenge:**
   - Try the correct answer
   - Try wrong answers and verify the error message
   - Verify the hint appears after 3 failed attempts

5. **Check the save file:**
   ```bash
   cat ~/.dojo_save.json
   ```
   - Confirm your mission ID appears in `"completed"`
   - Confirm honor points were awarded

---

## 🤝 Proposing a Mission Pack

Want to create a whole collection? Examples:

**Journalism Pack** (`missions_journalism.json`)
- Web scraping basics
- Data validation
- Ethical APIs
- Fact-checking with code

**Genealogy Pack** (`missions_genealogy.json`)
- JSON for family trees
- CSV parsing
- Recursive algorithms (descendants)
- Data privacy & consent

**Governance Pack** (`missions_governance.json`)
- Public data APIs
- Open-source contribution workflows
- Policy simulation in code
- Transparency through logs

To propose a pack:
1. Open an issue with the title: `Pack Proposal: [Your Pack Name]`
2. List the missions you want to write
3. Describe why this domain matters to learners
4. We'll discuss scope and integration

---

## 🎯 Contribution Workflow

### Fork & Clone

```bash
git clone https://github.com/YOUR-USERNAME/dojo-ascension.git
cd dojo-ascension
```

### Create a Branch

```bash
git checkout -b feature/add-mission-webscraping
# Or for a mission pack:
git checkout -b feature/pack-journalism
```

### Make Your Changes

- Edit `missions.json` (or create `missions_[pack-name].json` for a full pack)
- Test locally
- Update README if needed

### Commit

```bash
git commit -m "feat: add webscraping mission

- New mission: Web Scraping 101 (BeautifulSoup basics)
- Covers: HTML parsing, API requests, ethical considerations
- Skill: architecture (python+web)
- Honor: 25 points

Tested locally and verified save/load works correctly."
```

### Push & Open PR

```bash
git push origin feature/add-mission-webscraping
```

Then open a PR on GitHub. Use this template:

```markdown
## What This PR Adds

[Brief description of your mission(s)]

## Missions Included

- [ ] Mission 11: Web Scraping 101
- (Add more with checkboxes)

## Testing

- [x] Tested locally with `python dojo_classroom.py`
- [x] Verified mission appears in menu
- [x] Verified correct answer is accepted
- [x] Verified save file updates
- [x] Verified hint system works (if applicable)

## Links

- Related issue (if any): #XX
- Philosophy reference: [Your source]
- Economic parallel: [Your source]
```

---

## 🧠 Tips for Great Missions

### 1. **Test Rigorously**
- Does the engine parse your JSON?
- Does the challenge make sense?
- Are there edge cases in the answer checking?

### 2. **Honor Difficulty**
- Simple recall (definitions): 15-20 honor
- Application (write code): 20-25 honor
- Analysis (explain why): 25-30 honor
- Reflection (systems thinking): 30-35 honor

### 3. **Connect Broadly**
Don't assume learners know much about your field. Explain why it matters:
- "Genealogy teaches..." → relates to variables and data lineage
- "Journalism teaches..." → relates to Git history and accountability
- "Martial arts teaches..." → relates to efficiency and discipline in code

### 4. **Avoid Gatekeeping**
- Don't assume advanced knowledge
- Provide context in `tech_concept`
- Make hints genuinely helpful
- Remember: your learner might be 14 or 74, from any background

### 5. **Be Precise with Answers**
- Substring matching is flexible (good for "contains" checks)
- For exact matches, note it in the challenge: *"Write exactly..."*
- Test with whitespace variations: `seed = 42`, `seed=42`, `seed = 42 `

---

## 🎓 Philosophy & Tone

This project values:
- **Clarity over jargon** — Explain hard concepts in plain language
- **Breadth over depth** — Touch many disciplines, not just CS
- **Practice over perfection** — Celebrate returning, not just winning
- **Community over ego** — Assume good intent, offer constructive feedback

When writing a mission, ask yourself:
- *Does this connect to something real?*
- *Could a non-programmer understand the analogy?*
- *Does this teach mastery, not just answers?*
- *Would I want to learn from this?*

---

## 🐛 Reporting Issues

Found a bug or have feedback? Open an issue:

1. **For mission content:** "Mission X has unclear wording" → Suggest improvement
2. **For the engine:** "Save/load fails on Windows" → Provide error message & environment
3. **For docs:** "README doesn't mention X" → Suggest what should be added

### Good Issue Title
- ✅ "Mission 3 answer validation too strict"
- ✅ "dojo_classroom.py fails if ~/.dojo_save.json corrupted"
- ❌ "bug" or "help"

---

## 🙏 Code of Conduct

We're building a learning community. Be kind:
- **Assume good intent** in reviews and feedback
- **Ask questions** instead of making demands
- **Celebrate learning**, not just expertise
- **Welcome all backgrounds** — your unique perspective is valuable

---

## 📚 Resources

- **Python Learning:** [Official Python Docs](https://docs.python.org/)
- **Git Learning:** [Git Book](https://git-scm.com/book)
- **Philosophy References:**
  - Bruce Lee on efficiency: *"Absorb what is useful..."*
  - Cornel West on justice: *"Justice is what love looks like in public"*
  - Uta Hagen on acting: *"Nine Questions"* (foundation of reflection journal)
- **Educational Design:** See `README.md` for pedagogical model

---

## 🚀 Ready to Contribute?

1. Pick a topic you know and care about
2. Write your mission following the JSON format
3. Test it locally
4. Open a PR with a clear description
5. Engage with feedback
6. Merge and celebrate! 🎉

**Questions?** Open an issue, start a discussion, or reach out to maintainers.

**Let us never stop learning from Galileo.** — SolarPunk HackNet
