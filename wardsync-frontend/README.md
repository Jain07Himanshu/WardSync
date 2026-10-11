# WardSync — Local Problems. Collective Action.

WardSync is a clean, minimal, responsive civic action web application that discovers local problems using citizen reports, public information, and official records. It connects citizens, NGOs, and municipal authorities to coordinate donations, volunteering, and verified problem resolution.

---

## 🚀 Commands to Run the Project

To run the application locally:

```powershell
cd C:\Users\ACER\.gemini\antigravity\scratch\wardsync
npm run dev
```

Then open `http://localhost:5173` in your browser.

To verify the production build:
```powershell
npm run build
npm run preview
```

---

## 🏢 New NGO Section & Workflows Added

When logged in or switching to the **NGO persona** (e.g. *CleanWater Bengal*):

1. **Map & Issue Actions Switch Dynamically**:
   - The map view stays identical to the citizen view (interactive Leaflet OpenStreetMap with severity color-coded markers).
   - The 3 issue action buttons dynamically switch from:
     - Citizen View: `[Donate]` `[Volunteer]` `[Know More]`
     - **NGO View**: `[Raise Funds]` `[Create Event]` `[Know More]`

2. **Create Event Functionality (`NgoCreateEventModal.tsx`)**:
   - Allows the NGO to organize and publish ground response drives for any issue.
   - Fields configured:
     - Event Headline (e.g., *“Rapid Water Pipeline Repair & Filter Distribution Drive”*)
     - Scheduled Date & Time Slot
     - Specific Meeting Point (e.g., *“Entally Community Hall Gate 3”*)
     - Volunteer Capacity Needed
     - Ground Activity Briefing (exact tasks for volunteers)
     - Resources to bring & provided by NGO
     - Field Coordinator Name & Emergency Phone
   - **Citizen Integration**: Once created, this event is immediately set as the **confirmed schedule** for that issue. When any citizen opens the volunteer modal, they can see this exact date, time, and meeting point to RSVP!

3. **Raise Funds Functionality (`NgoRaiseFundsModal.tsx`)**:
   - Allows verified NGOs to set the target fundraising goal (INR).
   - Specify the exact relief purpose and transparent fund allocation breakdown (Direct Relief Kits, Transport/Logistics, Safety Equipment).
   - When launched, citizen donations contribute toward this active goal.

4. **NGO Workspace Dashboard (`Dashboards.tsx`)**:
   - **NGO Civic Action Console**: Embedded interactive map where NGOs can select issues and launch events/campaigns directly.
   - **Scheduled Events Hub**: Manage organized volunteer events, track volunteer capacity vs enrolled count, and view coordinator contacts.
   - **Active Fundraising Campaigns**: Monitor collected funds vs goals with animated progress bars.
   - **Citizen Volunteer Sign-up Roster**: Live table of all registered citizen volunteers (Name, Issue, Selected Slot, Phone, Skills, Headcount).

---

## 📁 Updated Project Architecture

```
wardsync/
├── src/
│   ├── types/
│   │   └── index.ts                 # Added NgoEvent, NgoFundraisingCampaign
│   ├── components/
│   │   ├── FeaturedIssueCard.tsx    # Switches buttons: [Raise Funds] [Create Event] [Know More]
│   │   ├── NgoCreateEventModal.tsx  # NEW: Event scheduling & briefing creator
│   │   ├── NgoRaiseFundsModal.tsx   # NEW: Fundraising target & purpose manager
│   │   ├── Dashboards.tsx           # Enhanced NGO workspace with map & volunteer roster
│   │   ├── IssueMap.tsx             # Interactive Leaflet map
│   │   ├── VolunteerModal.tsx       # Citizen RSVP reflecting NGO scheduled events
│   │   ├── DonateModal.tsx          # Citizen donation reflecting NGO campaigns
│   │   └── Header.tsx               # Quick persona switcher for testing
│   └── App.tsx                      # Event and campaign state synchronization
```
