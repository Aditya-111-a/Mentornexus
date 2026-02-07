# MentorNexus Frontend

This folder contains the frontend for **MentorNexus**, an AI-driven student–faculty project matching platform.

The frontend is a **pure UI layer**.  
All logic, scoring, decisions, and blockchain interactions are handled by the backend.

---

## System Architecture (Frontend View)

Frontend → FastAPI Backend → (Optional Gemini explanations) → (Blockchain commit on final match only)

Frontend responsibilities:
- Collect student input
- Display faculty and project data
- Trigger search and final match APIs
- Display explanations and blockchain proof

Frontend MUST NOT:
- Recompute scores
- Rank results
- Apply business rules
- Interact with blockchain directly

---

## Backend API Base

Backend runs at:
http://localhost:8000


Frontend must read base URL from:
VITE_API_BASE_URL


---

## Required Screens

### 1. Student Onboarding
Collect:
- skills (list of strings)
- interests (free text)
- availability
- academic_level

Rules:
- No skill levels
- No scoring or filtering logic
- Frontend only validates required fields

---

### 2. Faculty & Project Search (Exploration)
Endpoint:
POST /search

Behavior:
- Displays faculty and associated projects
- Shows explanation text returned by backend
- Full projects remain visible
- No final decision is made
- No blockchain interaction

Purpose:
Exploration and transparency only.

---

### 3. Final Match Confirmation
Endpoint:
POST /match/full

Triggered only after user confirms a selection.

Backend performs:
- deterministic scoring
- project-level matching
- capacity enforcement
- blockchain commit

Frontend responsibility:
- Send request
- Display response exactly as returned

---

### 4. Match Result Screen
Must display:
- faculty name
- project title
- final score
- match mode (research-driven or skill-driven)
- explanation text
- blockchain match_id

The match_id is immutable and read-only.

---

## Blockchain Rules

- Frontend never signs transactions
- Frontend never interacts with Ethereum directly
- Frontend only displays the match_id returned by backend
- Blockchain proof is informational only

---

## Data Rules (Must Be Respected)

- Dataset is CSV-driven (handled entirely by backend)
- Skills are presence-based (no levels)
- Projects can be visible but full
- Full projects cannot accept students
- No student replacement logic exists

---

## Recommended Frontend Structure

frontend/
├── src/
│ ├── api/ # API call wrappers only
│ ├── pages/ # Page-level components
│ ├── components/ # Reusable UI components
│ ├── types/ # Mirrors backend schemas
│ ├── utils/
│ └── main.jsx
├── public/
├── .env
├── package.json
└── vite.config.js


---

## Environment Variables

Create `frontend/.env`:
VITE_API_BASE_URL=http://localhost:8000

Do not commit this file.

---

## Development Commands

Create frontend:
npm create vite@latest

Run:
npm install
npm run dev

---

## Critical Design Constraints

- Search and final match are strictly separate
- Explanations are read-only
- LLM does not affect decisions
- Blockchain commit happens only after final match
- Frontend must reflect backend output exactly

---

## Ownership Rules

- Backend and blockchain code must not be modified
- All frontend work stays inside this folder
- Integration is API-only
