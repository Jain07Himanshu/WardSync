import { Issue } from '../types';

export const SAMPLE_ISSUES: Issue[] = [
  {
    "id": "rep-mum-2026-001",
    "title": "Sewage Overflow & Contaminated Water at Dadar",
    "locationName": "Ranade Road Junction, Near Dadar Railway Station (West), Mumbai",
    "ward": "Ward G/North (Dadar)",
    "locality": "Dadar",
    "distanceKm": 2.6,
    "latitude": 19.0178,
    "longitude": 72.8478,
    "category": "Water & Sanitation",
    "severity": "Critical",
    "urgency": "Immediate (24h)",
    "status": "Verified",
    "evidenceConfidence": 94,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Main sewage distribution pipe ruptured behind Dadar Flower Market; raw effluent entering drinking water distribution network, causing severe foul odor and discolored tap water in 800+ households along Ranade Road.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-MUM-4019 under High Commercial Corridor & Transit Hub.",
      "isVerified": true
    },
    "affectedPeople": "Est. ~4560 residents & commuters traversing Dadar.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to High Commercial Corridor & Transit Hub.",
    "unverifiedAspects": "Detailed site audit from BMC Hydraulic Engineer's Department (Water Supply) assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Brihanmumbai Municipal Corporation (BMC)",
      "department": "BMC Hydraulic Engineer's Department (Water Supply)",
      "contact": "bmc.helpline@mcgm.gov.in / Civic Helpline 1916",
      "officialStatus": "Target resolution within 7 days (Ref: REP-MUM-2026-001)."
    },
    "relevantNgos": [
      {
        "name": "Mumbai March Civic Action Collective",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Mumbai Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Brihanmumbai Municipal Corporation (BMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-mum-2026-001-1",
        "title": "Resident Field Complaint #REP-MUM-2026-001",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Main sewage distribution pipe ruptured behind Dadar Flower Market; raw effluent entering drinking water distribution network, causing severe foul odor and discolored tap water in 800+ households along Ranade Road.",
        "isOfficial": false,
        "credibilityScore": 92
      },
      {
        "id": "ev-rep-mum-2026-001-2",
        "title": "Local Press Corroboration (Mumbai Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Ranade Road Junction, Near Dadar Railway Station (West). Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 38,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by BMC Hydraulic Engineer's Department (Water Supply)",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 12500,
    "donationBeneficiary": "Mumbai March Civic Action Collective Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-mum-2026-001-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 19,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-mum-2026-001-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Ranade Road Junction, Near Dadar Railway Station (West) (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 19
  },
  {
    "id": "rep-mum-2026-002",
    "title": "Potholes & Hazardous Road Damage at Bandra",
    "locationName": "SV Road, Opposite Bandra Talao, Bandra West, Mumbai",
    "ward": "Ward H/West (Bandra)",
    "locality": "Bandra",
    "distanceKm": 1.9,
    "latitude": 19.0596,
    "longitude": 72.8335,
    "category": "Roads & Transport",
    "severity": "Critical",
    "urgency": "Immediate (24h)",
    "status": "In progress",
    "evidenceConfidence": 89,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Clusters of deep craters (up to 8 inches deep) spanning 40 meters along SV Road near Bandra Talao; multiple two-wheeler accidents and heavy morning peak-hour bottlenecks.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-MUM-2810 under Major Arterial Highway & Commercial Zone.",
      "isVerified": false
    },
    "affectedPeople": "Est. ~5640 residents & commuters traversing Bandra.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Major Arterial Highway & Commercial Zone.",
    "unverifiedAspects": "Detailed site audit from BMC Roads & Traffic Department assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Brihanmumbai Municipal Corporation (BMC)",
      "department": "BMC Roads & Traffic Department",
      "contact": "bmc.helpline@mcgm.gov.in / Civic Helpline 1916",
      "officialStatus": "Target resolution within 4 days (Ref: REP-MUM-2026-002)."
    },
    "relevantNgos": [
      {
        "name": "Mumbai March Civic Action Collective",
        "verified": true,
        "focus": "Infrastructure Monitoring & Safety"
      },
      {
        "name": "Mumbai Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Brihanmumbai Municipal Corporation (BMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-mum-2026-002-1",
        "title": "Resident Field Complaint #REP-MUM-2026-002",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Clusters of deep craters (up to 8 inches deep) spanning 40 meters along SV Road near Bandra Talao; multiple two-wheeler accidents and heavy morning peak-hour bottlenecks.",
        "isOfficial": false,
        "credibilityScore": 86
      },
      {
        "id": "ev-rep-mum-2026-002-2",
        "title": "Local Press Corroboration (Mumbai Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along SV Road, Opposite Bandra Talao, Bandra West. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 47,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Completed"
      },
      {
        "phase": "Phase 2: Repair & Intervention by BMC Roads & Traffic Department",
        "description": "Execute targeted municipal engineering fix.",
        "status": "In progress"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 12500,
    "donationBeneficiary": "Mumbai March Civic Action Collective Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-mum-2026-002-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 23,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-mum-2026-002-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "SV Road, Opposite Bandra Talao, Bandra West (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 23
  },
  {
    "id": "rep-tha-2026-003",
    "title": "Stormwater Drain Clogging & Waterlogging at Majiwada",
    "locationName": "Majiwada Junction Service Road, Near Lodha IThink Techno Campus, Thane",
    "ward": "Ward 3 (Majiwada, Thane)",
    "locality": "Majiwada",
    "distanceKm": 1.9,
    "latitude": 19.2183,
    "longitude": 72.9781,
    "category": "Water & Sanitation",
    "severity": "High",
    "urgency": "Urgent (48-72h)",
    "status": "Verified",
    "evidenceConfidence": 84,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Underground box drain completely clogged with plastic packaging and construction debris under Majiwada flyover; 2 feet of waterlogging after moderate rain, submerging pedestrian walkways and bus stops.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-THA-1104 under Major Highway Interchange & Transit Knot.",
      "isVerified": true
    },
    "affectedPeople": "Est. ~3480 residents & commuters traversing Majiwada.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Major Highway Interchange & Transit Knot.",
    "unverifiedAspects": "Detailed site audit from TMC Public Works Department (PWD) assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Thane Municipal Corporation (TMC)",
      "department": "TMC Public Works Department (PWD)",
      "contact": "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108",
      "officialStatus": "Target resolution within 6 days (Ref: REP-THA-2026-003)."
    },
    "relevantNgos": [
      {
        "name": "Thane Citizen Action Council",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Thane Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Thane Municipal Corporation (TMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-tha-2026-003-1",
        "title": "Resident Field Complaint #REP-THA-2026-003",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Underground box drain completely clogged with plastic packaging and construction debris under Majiwada flyover; 2 feet of waterlogging after moderate rain, submerging pedestrian walkways and bus stops.",
        "isOfficial": false,
        "credibilityScore": 81
      },
      {
        "id": "ev-rep-tha-2026-003-2",
        "title": "Local Press Corroboration (Thane Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Majiwada Junction Service Road, Near Lodha IThink Techno Campus. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 29,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by TMC Public Works Department (PWD)",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 6000,
    "donationBeneficiary": "Thane Citizen Action Council Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-tha-2026-003-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 14,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-tha-2026-003-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Majiwada Junction Service Road, Near Lodha IThink Techno Campus (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 14
  },
  {
    "id": "rep-tha-2026-004",
    "title": "Illegal Solid Waste Dumping at Naupada",
    "locationName": "M.G. Road, Behind Naupada Market Yard, Thane West, Thane",
    "ward": "Ward 1 (Naupada, Thane)",
    "locality": "Naupada",
    "distanceKm": 3.3,
    "latitude": 19.1865,
    "longitude": 72.9731,
    "category": "Waste Management",
    "severity": "Critical",
    "urgency": "Immediate (24h)",
    "status": "Reported",
    "evidenceConfidence": 91,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Massive 30-ton unsegregated municipal and e-waste garbage mountain accumulating in open ground near Naupada vegetable market; stray animals, rodents, and severe toxic stench affecting nearby primary school.",
    "cause": {
      "documented": "Documented failure reported by resident ID ANON-THA-089 under Dense Residential & School Zone.",
      "isVerified": false
    },
    "affectedPeople": "Est. ~2640 residents & commuters traversing Naupada.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Dense Residential & School Zone.",
    "unverifiedAspects": "Detailed site audit from TMC Solid Waste Management Division assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Thane Municipal Corporation (TMC)",
      "department": "TMC Solid Waste Management Division",
      "contact": "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108",
      "officialStatus": "Target resolution within 5 days (Ref: REP-THA-2026-004)."
    },
    "relevantNgos": [
      {
        "name": "Thane Citizen Action Council",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Thane Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Thane Municipal Corporation (TMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-tha-2026-004-1",
        "title": "Resident Field Complaint #REP-THA-2026-004",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Massive 30-ton unsegregated municipal and e-waste garbage mountain accumulating in open ground near Naupada vegetable market; stray animals, rodents, and severe toxic stench affecting nearby primary school.",
        "isOfficial": false,
        "credibilityScore": 88
      },
      {
        "id": "ev-rep-tha-2026-004-2",
        "title": "Local Press Corroboration (Thane Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along M.G. Road, Behind Naupada Market Yard, Thane West. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 22,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by TMC Solid Waste Management Division",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 12500,
    "donationBeneficiary": "Thane Citizen Action Council Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-tha-2026-004-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 11,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-tha-2026-004-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "M.G. Road, Behind Naupada Market Yard, Thane West (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 11
  },
  {
    "id": "rep-mum-2026-005",
    "title": "Non-functional High-Mast Streetlights at Andheri",
    "locationName": "Andheri-Kurla Road, Near Chakala Metro Station, Andheri East, Mumbai",
    "ward": "Ward K/East (Andheri)",
    "locality": "Andheri",
    "distanceKm": 1.2,
    "latitude": 19.1136,
    "longitude": 72.8697,
    "category": "Public Safety",
    "severity": "High",
    "urgency": "Urgent (48-72h)",
    "status": "In progress",
    "evidenceConfidence": 78,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Entire 1.2-kilometer stretch of Andheri-Kurla Link Road has 18 consecutive non-functional high-mast and sodium vapor streetlights; complete darkness creating severe crime hazard and pedestrian peril near metro station.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-MUM-7731 under Metro Transit Corridor & Commercial Hub.",
      "isVerified": false
    },
    "affectedPeople": "Est. ~2280 residents & commuters traversing Andheri.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Metro Transit Corridor & Commercial Hub.",
    "unverifiedAspects": "Detailed site audit from BMC Building & Factory (Electrical Division) assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Brihanmumbai Municipal Corporation (BMC)",
      "department": "BMC Building & Factory (Electrical Division)",
      "contact": "bmc.helpline@mcgm.gov.in / Civic Helpline 1916",
      "officialStatus": "Target resolution within 5 days (Ref: REP-MUM-2026-005)."
    },
    "relevantNgos": [
      {
        "name": "Mumbai March Civic Action Collective",
        "verified": true,
        "focus": "Infrastructure Monitoring & Safety"
      },
      {
        "name": "Mumbai Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Brihanmumbai Municipal Corporation (BMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-mum-2026-005-1",
        "title": "Resident Field Complaint #REP-MUM-2026-005",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Entire 1.2-kilometer stretch of Andheri-Kurla Link Road has 18 consecutive non-functional high-mast and sodium vapor streetlights; complete darkness creating severe crime hazard and pedestrian peril near metro station.",
        "isOfficial": false,
        "credibilityScore": 75
      },
      {
        "id": "ev-rep-mum-2026-005-2",
        "title": "Local Press Corroboration (Mumbai Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Andheri-Kurla Road, Near Chakala Metro Station, Andheri East. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 19,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Completed"
      },
      {
        "phase": "Phase 2: Repair & Intervention by BMC Building & Factory (Electrical Division)",
        "description": "Execute targeted municipal engineering fix.",
        "status": "In progress"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 6000,
    "donationBeneficiary": "Mumbai March Civic Action Collective Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-mum-2026-005-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 9,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-mum-2026-005-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Andheri-Kurla Road, Near Chakala Metro Station, Andheri East (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 9
  },
  {
    "id": "rep-mum-2026-006",
    "title": "Open Culvert & Missing Drain Slabs at Bandra",
    "locationName": "Hill Road, Adjacent to Holy Family Hospital, Bandra West, Mumbai",
    "ward": "Ward H/West (Bandra)",
    "locality": "Bandra",
    "distanceKm": 4.0,
    "latitude": 19.0536,
    "longitude": 72.8279,
    "category": "Water & Sanitation",
    "severity": "Critical",
    "urgency": "Immediate (24h)",
    "status": "Verified",
    "evidenceConfidence": 95,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Broken and missing concrete drain slabs leaving 5-foot deep open culvert directly outside Holy Family Convent School on Hill Road; children and elderly pedestrians at extreme injury risk.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-MUM-9241 under School & Hospital Pedestrian Zone.",
      "isVerified": true
    },
    "affectedPeople": "Est. ~4080 residents & commuters traversing Bandra.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to School & Hospital Pedestrian Zone.",
    "unverifiedAspects": "Detailed site audit from BMC Storm Water Drains (SWD) assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Brihanmumbai Municipal Corporation (BMC)",
      "department": "BMC Storm Water Drains (SWD)",
      "contact": "bmc.helpline@mcgm.gov.in / Civic Helpline 1916",
      "officialStatus": "Target resolution within 3 days (Ref: REP-MUM-2026-006)."
    },
    "relevantNgos": [
      {
        "name": "Mumbai March Civic Action Collective",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Mumbai Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Brihanmumbai Municipal Corporation (BMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-mum-2026-006-1",
        "title": "Resident Field Complaint #REP-MUM-2026-006",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Broken and missing concrete drain slabs leaving 5-foot deep open culvert directly outside Holy Family Convent School on Hill Road; children and elderly pedestrians at extreme injury risk.",
        "isOfficial": false,
        "credibilityScore": 94
      },
      {
        "id": "ev-rep-mum-2026-006-2",
        "title": "Local Press Corroboration (Mumbai Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Hill Road, Adjacent to Holy Family Hospital, Bandra West. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 34,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by BMC Storm Water Drains (SWD)",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 12500,
    "donationBeneficiary": "Mumbai March Civic Action Collective Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-mum-2026-006-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 17,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-mum-2026-006-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Hill Road, Adjacent to Holy Family Hospital, Bandra West (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 17
  },
  {
    "id": "rep-tha-2026-007",
    "title": "Drinking Water Pipeline Burst at Central Ward",
    "locationName": "Road No. 16, Wagle Industrial Estate, Near Passport Seva Kendra, Thane",
    "ward": "Ward 2 (Wagle Estate, Thane)",
    "locality": "Central Ward",
    "distanceKm": 1.2,
    "latitude": 19.1932,
    "longitude": 72.9515,
    "category": "Water & Sanitation",
    "severity": "Critical",
    "urgency": "Immediate (24h)",
    "status": "In progress",
    "evidenceConfidence": 96,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Pressurized 400mm water main line ruptured during highway widening trenching; clean drinking water gushing onto highway creating artificial flooding while 1,500 flats in Wagle Estate experience zero water pressure.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-THA-3329 under Industrial & Administrative Center.",
      "isVerified": false
    },
    "affectedPeople": "Est. ~6240 residents & commuters traversing Central Ward.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Industrial & Administrative Center.",
    "unverifiedAspects": "Detailed site audit from TMC Water Supply & Sewerage Directorate assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Thane Municipal Corporation (TMC)",
      "department": "TMC Water Supply & Sewerage Directorate",
      "contact": "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108",
      "officialStatus": "Target resolution within 2 days (Ref: REP-THA-2026-007)."
    },
    "relevantNgos": [
      {
        "name": "Thane Citizen Action Council",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Thane Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Thane Municipal Corporation (TMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-tha-2026-007-1",
        "title": "Resident Field Complaint #REP-THA-2026-007",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Pressurized 400mm water main line ruptured during highway widening trenching; clean drinking water gushing onto highway creating artificial flooding while 1,500 flats in Wagle Estate experience zero water pressure.",
        "isOfficial": false,
        "credibilityScore": 90
      },
      {
        "id": "ev-rep-tha-2026-007-2",
        "title": "Local Press Corroboration (Thane Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Road No. 16, Wagle Industrial Estate, Near Passport Seva Kendra. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 52,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Completed"
      },
      {
        "phase": "Phase 2: Repair & Intervention by TMC Water Supply & Sewerage Directorate",
        "description": "Execute targeted municipal engineering fix.",
        "status": "In progress"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 12500,
    "donationBeneficiary": "Thane Citizen Action Council Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-tha-2026-007-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 26,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-tha-2026-007-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Road No. 16, Wagle Industrial Estate, Near Passport Seva Kendra (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 26
  },
  {
    "id": "rep-mum-2026-008",
    "title": "Dengue / Malaria Mosquito Breeding Ground at Kurla",
    "locationName": "LBS Marg, Near Phoenix Marketcity Mall, Kurla West, Mumbai",
    "ward": "Ward L (Kurla)",
    "locality": "Kurla",
    "distanceKm": 4.0,
    "latitude": 19.0688,
    "longitude": 72.8797,
    "category": "Health",
    "severity": "High",
    "urgency": "Urgent (48-72h)",
    "status": "Verified",
    "evidenceConfidence": 87,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Stagnant toxic water pond formed inside abandoned infrastructure casting yard near LBS Marg; larval index exceeding 32, with 26 confirmed dengue cases reported in surrounding chawls over 10 days.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-MUM-5102 under Dense Residential Settlement & Commercial Zone.",
      "isVerified": true
    },
    "affectedPeople": "Est. ~3360 residents & commuters traversing Kurla.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Dense Residential Settlement & Commercial Zone.",
    "unverifiedAspects": "Detailed site audit from BMC Public Health Department assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Brihanmumbai Municipal Corporation (BMC)",
      "department": "BMC Public Health Department",
      "contact": "bmc.helpline@mcgm.gov.in / Civic Helpline 1916",
      "officialStatus": "Target resolution within 8 days (Ref: REP-MUM-2026-008)."
    },
    "relevantNgos": [
      {
        "name": "Mumbai March Civic Action Collective",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Mumbai Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Brihanmumbai Municipal Corporation (BMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-mum-2026-008-1",
        "title": "Resident Field Complaint #REP-MUM-2026-008",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Stagnant toxic water pond formed inside abandoned infrastructure casting yard near LBS Marg; larval index exceeding 32, with 26 confirmed dengue cases reported in surrounding chawls over 10 days.",
        "isOfficial": false,
        "credibilityScore": 89
      },
      {
        "id": "ev-rep-mum-2026-008-2",
        "title": "Local Press Corroboration (Mumbai Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along LBS Marg, Near Phoenix Marketcity Mall, Kurla West. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 28,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by BMC Public Health Department",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 6000,
    "donationBeneficiary": "Mumbai March Civic Action Collective Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-mum-2026-008-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 14,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-mum-2026-008-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "LBS Marg, Near Phoenix Marketcity Mall, Kurla West (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 14
  },
  {
    "id": "rep-tha-2026-009",
    "title": "Potholes & Hazardous Road Damage at Ghodbunder",
    "locationName": "Ghodbunder Road Service Lane, Near Anand Nagar Naka, Thane West, Thane",
    "ward": "Ward 4 (Ghodbunder, Thane)",
    "locality": "Ghodbunder",
    "distanceKm": 1.2,
    "latitude": 19.2612,
    "longitude": 72.9634,
    "category": "Roads & Transport",
    "severity": "High",
    "urgency": "Urgent (48-72h)",
    "status": "Reported",
    "evidenceConfidence": 82,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Continuous asphalt degradation and heavy cratering spanning 200 meters on Ghodbunder Road service road; heavy container trucks tipping and extreme morning gridlock stretching to Gaimukh.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-THA-6618 under National Freight Corridor & Highway Corridor.",
      "isVerified": false
    },
    "affectedPeople": "Est. ~4920 residents & commuters traversing Ghodbunder.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to National Freight Corridor & Highway Corridor.",
    "unverifiedAspects": "Detailed site audit from TMC Public Works Department (PWD) assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Thane Municipal Corporation (TMC)",
      "department": "TMC Public Works Department (PWD)",
      "contact": "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108",
      "officialStatus": "Target resolution within 7 days (Ref: REP-THA-2026-009)."
    },
    "relevantNgos": [
      {
        "name": "Thane Citizen Action Council",
        "verified": true,
        "focus": "Infrastructure Monitoring & Safety"
      },
      {
        "name": "Thane Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Thane Municipal Corporation (TMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-tha-2026-009-1",
        "title": "Resident Field Complaint #REP-THA-2026-009",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Continuous asphalt degradation and heavy cratering spanning 200 meters on Ghodbunder Road service road; heavy container trucks tipping and extreme morning gridlock stretching to Gaimukh.",
        "isOfficial": false,
        "credibilityScore": 80
      },
      {
        "id": "ev-rep-tha-2026-009-2",
        "title": "Local Press Corroboration (Thane Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Ghodbunder Road Service Lane, Near Anand Nagar Naka, Thane West. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 41,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by TMC Public Works Department (PWD)",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 6000,
    "donationBeneficiary": "Thane Citizen Action Council Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-tha-2026-009-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 20,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-tha-2026-009-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Ghodbunder Road Service Lane, Near Anand Nagar Naka, Thane West (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 20
  },
  {
    "id": "rep-mum-2026-010",
    "title": "Illegal Solid Waste Dumping at Bandra",
    "locationName": "Sion-Bandra Link Road, Near Maharashtra Nature Park, Dharavi, Mumbai",
    "ward": "Ward H/West (Bandra)",
    "locality": "Bandra",
    "distanceKm": 2.6,
    "latitude": 19.0436,
    "longitude": 72.8596,
    "category": "Waste Management",
    "severity": "High",
    "urgency": "Urgent (48-72h)",
    "status": "Verified",
    "evidenceConfidence": 85,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Construction demolition debris, broken tiles, and gypsum plaster illegally dumped in mangrove buffer zone along Mahim Nature Park perimeter; blocking tidal water flow and causing environmental destruction.",
    "cause": {
      "documented": "Documented failure reported by resident ID ANON-MUM-412 under Ecological Wetland & Coastal Mangrove Zone.",
      "isVerified": true
    },
    "affectedPeople": "Est. ~2040 residents & commuters traversing Bandra.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Ecological Wetland & Coastal Mangrove Zone.",
    "unverifiedAspects": "Detailed site audit from BMC Solid Waste Management (SWM) assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Brihanmumbai Municipal Corporation (BMC)",
      "department": "BMC Solid Waste Management (SWM)",
      "contact": "bmc.helpline@mcgm.gov.in / Civic Helpline 1916",
      "officialStatus": "Target resolution within 8 days (Ref: REP-MUM-2026-010)."
    },
    "relevantNgos": [
      {
        "name": "Mumbai March Civic Action Collective",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Mumbai Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Brihanmumbai Municipal Corporation (BMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-mum-2026-010-1",
        "title": "Resident Field Complaint #REP-MUM-2026-010",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Construction demolition debris, broken tiles, and gypsum plaster illegally dumped in mangrove buffer zone along Mahim Nature Park perimeter; blocking tidal water flow and causing environmental destruction.",
        "isOfficial": false,
        "credibilityScore": 87
      },
      {
        "id": "ev-rep-mum-2026-010-2",
        "title": "Local Press Corroboration (Mumbai Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Sion-Bandra Link Road, Near Maharashtra Nature Park, Dharavi. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 17,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by BMC Solid Waste Management (SWM)",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 6000,
    "donationBeneficiary": "Mumbai March Civic Action Collective Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-mum-2026-010-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 8,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-mum-2026-010-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Sion-Bandra Link Road, Near Maharashtra Nature Park, Dharavi (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 8
  },
  {
    "id": "rep-tha-2026-011",
    "title": "Sewage Overflow & Contaminated Water at Kopri",
    "locationName": "Station Road, Kopri Colony, Thane East, Thane",
    "ward": "Ward 5 (Kopri, Thane)",
    "locality": "Kopri",
    "distanceKm": 4.0,
    "latitude": 19.1824,
    "longitude": 72.9845,
    "category": "Water & Sanitation",
    "severity": "Critical",
    "urgency": "Immediate (24h)",
    "status": "In progress",
    "evidenceConfidence": 90,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Choked municipal drainage manhole discharging black foul-smelling sewer water across Kopri market street; water entering ground floor ration shops and low-lying residential apartment lobbies.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-THA-8902 under Railway Station Commuter District.",
      "isVerified": false
    },
    "affectedPeople": "Est. ~3000 residents & commuters traversing Kopri.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Railway Station Commuter District.",
    "unverifiedAspects": "Detailed site audit from TMC Water Supply & Sewerage Directorate assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Thane Municipal Corporation (TMC)",
      "department": "TMC Water Supply & Sewerage Directorate",
      "contact": "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108",
      "officialStatus": "Target resolution within 4 days (Ref: REP-THA-2026-011)."
    },
    "relevantNgos": [
      {
        "name": "Thane Citizen Action Council",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Thane Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Thane Municipal Corporation (TMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-tha-2026-011-1",
        "title": "Resident Field Complaint #REP-THA-2026-011",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Choked municipal drainage manhole discharging black foul-smelling sewer water across Kopri market street; water entering ground floor ration shops and low-lying residential apartment lobbies.",
        "isOfficial": false,
        "credibilityScore": 89
      },
      {
        "id": "ev-rep-tha-2026-011-2",
        "title": "Local Press Corroboration (Thane Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Station Road, Kopri Colony, Thane East. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 25,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Completed"
      },
      {
        "phase": "Phase 2: Repair & Intervention by TMC Water Supply & Sewerage Directorate",
        "description": "Execute targeted municipal engineering fix.",
        "status": "In progress"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 12500,
    "donationBeneficiary": "Thane Citizen Action Council Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-tha-2026-011-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 12,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-tha-2026-011-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Station Road, Kopri Colony, Thane East (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 12
  },
  {
    "id": "rep-mum-2026-012",
    "title": "Potholes & Hazardous Road Damage at Chembur",
    "locationName": "VN Purav Marg, Near Diamond Garden Circle, Chembur, Mumbai",
    "ward": "Ward M/West (Chembur)",
    "locality": "Chembur",
    "distanceKm": 3.3,
    "latitude": 19.0522,
    "longitude": 72.8988,
    "category": "Roads & Transport",
    "severity": "Moderate",
    "urgency": "Moderate (1-2 weeks)",
    "status": "Reported",
    "evidenceConfidence": 72,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Severe road surface breakup and exposed steel reinforcement mesh near Chembur Diamond Garden junction; multiple auto-rickshaw axle damages recorded this week.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-MUM-6190 under Commercial District & Residential Suburb.",
      "isVerified": false
    },
    "affectedPeople": "Est. ~1800 residents & commuters traversing Chembur.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Commercial District & Residential Suburb.",
    "unverifiedAspects": "Detailed site audit from BMC Roads & Traffic Department assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Brihanmumbai Municipal Corporation (BMC)",
      "department": "BMC Roads & Traffic Department",
      "contact": "bmc.helpline@mcgm.gov.in / Civic Helpline 1916",
      "officialStatus": "Target resolution within 6 days (Ref: REP-MUM-2026-012)."
    },
    "relevantNgos": [
      {
        "name": "Mumbai March Civic Action Collective",
        "verified": true,
        "focus": "Infrastructure Monitoring & Safety"
      },
      {
        "name": "Mumbai Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Brihanmumbai Municipal Corporation (BMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-mum-2026-012-1",
        "title": "Resident Field Complaint #REP-MUM-2026-012",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Severe road surface breakup and exposed steel reinforcement mesh near Chembur Diamond Garden junction; multiple auto-rickshaw axle damages recorded this week.",
        "isOfficial": false,
        "credibilityScore": 68
      },
      {
        "id": "ev-rep-mum-2026-012-2",
        "title": "Local Press Corroboration (Mumbai Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along VN Purav Marg, Near Diamond Garden Circle, Chembur. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 15,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by BMC Roads & Traffic Department",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 6000,
    "donationBeneficiary": "Mumbai March Civic Action Collective Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-mum-2026-012-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 7,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-mum-2026-012-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "VN Purav Marg, Near Diamond Garden Circle, Chembur (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 7
  },
  {
    "id": "rep-tha-2026-013",
    "title": "Non-functional High-Mast Streetlights at Kalwa",
    "locationName": "Old Pune Road, Kalwa Naka Roundabout, Kalwa, Thane, Thane",
    "ward": "Ward 6 (Kalwa, Thane)",
    "locality": "Kalwa",
    "distanceKm": 1.9,
    "latitude": 19.1982,
    "longitude": 72.9981,
    "category": "Public Safety",
    "severity": "High",
    "urgency": "Urgent (48-72h)",
    "status": "In progress",
    "evidenceConfidence": 79,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Central high-mast illumination tower at Kalwa Naka roundabout completely dark for 6 nights; heavy pedestrian and auto-rickshaw density resulting in near-miss collisions with divider curb.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-THA-4421 under High-Density Traffic Intersection.",
      "isVerified": false
    },
    "affectedPeople": "Est. ~2520 residents & commuters traversing Kalwa.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to High-Density Traffic Intersection.",
    "unverifiedAspects": "Detailed site audit from TMC Electrical & Street Lighting Department assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Thane Municipal Corporation (TMC)",
      "department": "TMC Electrical & Street Lighting Department",
      "contact": "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108",
      "officialStatus": "Target resolution within 4 days (Ref: REP-THA-2026-013)."
    },
    "relevantNgos": [
      {
        "name": "Thane Citizen Action Council",
        "verified": true,
        "focus": "Infrastructure Monitoring & Safety"
      },
      {
        "name": "Thane Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Thane Municipal Corporation (TMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-tha-2026-013-1",
        "title": "Resident Field Complaint #REP-THA-2026-013",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Central high-mast illumination tower at Kalwa Naka roundabout completely dark for 6 nights; heavy pedestrian and auto-rickshaw density resulting in near-miss collisions with divider curb.",
        "isOfficial": false,
        "credibilityScore": 76
      },
      {
        "id": "ev-rep-tha-2026-013-2",
        "title": "Local Press Corroboration (Thane Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Old Pune Road, Kalwa Naka Roundabout, Kalwa, Thane. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 21,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Completed"
      },
      {
        "phase": "Phase 2: Repair & Intervention by TMC Electrical & Street Lighting Department",
        "description": "Execute targeted municipal engineering fix.",
        "status": "In progress"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 6000,
    "donationBeneficiary": "Thane Citizen Action Council Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-tha-2026-013-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 10,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-tha-2026-013-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Old Pune Road, Kalwa Naka Roundabout, Kalwa, Thane (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 10
  },
  {
    "id": "rep-mum-2026-014",
    "title": "Stormwater Drain Clogging & Waterlogging at Colaba",
    "locationName": "Shahid Bhagat Singh Road, Colaba Causeway, South Mumbai, Mumbai",
    "ward": "Ward A (Colaba)",
    "locality": "Colaba",
    "distanceKm": 2.6,
    "latitude": 18.9186,
    "longitude": 72.8288,
    "category": "Water & Sanitation",
    "severity": "High",
    "urgency": "Urgent (48-72h)",
    "status": "Verified",
    "evidenceConfidence": 83,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Heritage stone arch stormwater outfall at Colaba Causeway blocked by marine silt and beverage cans; tidal surge causes knee-deep seawater accumulation near historic market arcades.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-MUM-1088 under Heritage Tourism District & Commercial Quarter.",
      "isVerified": true
    },
    "affectedPeople": "Est. ~3120 residents & commuters traversing Colaba.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Heritage Tourism District & Commercial Quarter.",
    "unverifiedAspects": "Detailed site audit from BMC Storm Water Drains (SWD) assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Brihanmumbai Municipal Corporation (BMC)",
      "department": "BMC Storm Water Drains (SWD)",
      "contact": "bmc.helpline@mcgm.gov.in / Civic Helpline 1916",
      "officialStatus": "Target resolution within 7 days (Ref: REP-MUM-2026-014)."
    },
    "relevantNgos": [
      {
        "name": "Mumbai March Civic Action Collective",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Mumbai Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Brihanmumbai Municipal Corporation (BMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-mum-2026-014-1",
        "title": "Resident Field Complaint #REP-MUM-2026-014",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Heritage stone arch stormwater outfall at Colaba Causeway blocked by marine silt and beverage cans; tidal surge causes knee-deep seawater accumulation near historic market arcades.",
        "isOfficial": false,
        "credibilityScore": 82
      },
      {
        "id": "ev-rep-mum-2026-014-2",
        "title": "Local Press Corroboration (Mumbai Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Shahid Bhagat Singh Road, Colaba Causeway, South Mumbai. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 26,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by BMC Storm Water Drains (SWD)",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 6000,
    "donationBeneficiary": "Mumbai March Civic Action Collective Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-mum-2026-014-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 13,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-mum-2026-014-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Shahid Bhagat Singh Road, Colaba Causeway, South Mumbai (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 13
  },
  {
    "id": "rep-tha-2026-015",
    "title": "Open Culvert & Missing Drain Slabs at Vartak Nagar",
    "locationName": "Pokhran Road No. 1, Near Vartak Nagar Bus Depot, Thane West, Thane",
    "ward": "Ward 2 (Vartak Nagar, Thane)",
    "locality": "Vartak Nagar",
    "distanceKm": 1.9,
    "latitude": 19.2084,
    "longitude": 72.9621,
    "category": "Water & Sanitation",
    "severity": "Critical",
    "urgency": "Immediate (24h)",
    "status": "Verified",
    "evidenceConfidence": 92,
    "dateDiscovered": "Oct 8, 2026",
    "description": "Unfenced storm culvert trench across pedestrian footpath near Vartak Nagar bus depot; missing 3 concrete slabs, submerged hazard during rains.",
    "cause": {
      "documented": "Documented failure reported by resident ID RES-THA-7751 under Bus Terminal & High Pedestrian Density Zone.",
      "isVerified": true
    },
    "affectedPeople": "Est. ~3720 residents & commuters traversing Vartak Nagar.",
    "likelyImpact": "Severe inconvenience, risk to life/property, and disruption to Bus Terminal & High Pedestrian Density Zone.",
    "unverifiedAspects": "Detailed site audit from TMC Public Works Department (PWD) assistant municipal engineer scheduled.",
    "responsibleAuthority": {
      "name": "Thane Municipal Corporation (TMC)",
      "department": "TMC Public Works Department (PWD)",
      "contact": "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108",
      "officialStatus": "Target resolution within 4 days (Ref: REP-THA-2026-015)."
    },
    "relevantNgos": [
      {
        "name": "Thane Citizen Action Council",
        "verified": true,
        "focus": "Sanitation & Water Rights"
      },
      {
        "name": "Thane Clean & Safe Initiative",
        "verified": true,
        "focus": "Rapid Community Response"
      }
    ],
    "availableResources": [
      "Municipal rapid response crew assigned by Thane Municipal Corporation (TMC)",
      "Local volunteer monitoring team on standby"
    ],
    "evidence": [
      {
        "id": "ev-rep-tha-2026-015-1",
        "title": "Resident Field Complaint #REP-THA-2026-015",
        "type": "Citizen Report",
        "date": "Oct 9, 2026",
        "excerpt": "Unfenced storm culvert trench across pedestrian footpath near Vartak Nagar bus depot; missing 3 concrete slabs, submerged hazard during rains.",
        "isOfficial": false,
        "credibilityScore": 91
      },
      {
        "id": "ev-rep-tha-2026-015-2",
        "title": "Local Press Corroboration (Thane Mirror)",
        "type": "News Media",
        "date": "Oct 10, 2026",
        "excerpt": "Reporters verified civic disruption along Pokhran Road No. 1, Near Vartak Nagar Bus Depot, Thane West. Traffic police alerted.",
        "isOfficial": true,
        "credibilityScore": 91
      }
    ],
    "mergedReportsCount": 31,
    "actionPlan": [
      {
        "phase": "Phase 1: Verification & Perimeter Cordon",
        "description": "Install reflective caution barriers and inspect structural defects.",
        "status": "Pending"
      },
      {
        "phase": "Phase 2: Repair & Intervention by TMC Public Works Department (PWD)",
        "description": "Execute targeted municipal engineering fix.",
        "status": "Pending"
      },
      {
        "phase": "Phase 3: Citizen Closeout Audit",
        "description": "Verify durability and sign-off on public grievance closure.",
        "status": "Pending"
      }
    ],
    "donationGoal": 35000,
    "donationRaised": 12500,
    "donationBeneficiary": "Thane Citizen Action Council Public Fund",
    "volunteerSlots": [
      {
        "id": "vs-rep-tha-2026-015-1",
        "dateTime": "Saturday, Oct 17 \u00b7 9:30 AM - 12:30 PM",
        "voteCount": 15,
        "isConfirmed": true,
        "isPopular": true
      },
      {
        "id": "vs-rep-tha-2026-015-2",
        "dateTime": "Sunday, Oct 18 \u00b7 8:30 AM - 11:30 AM",
        "voteCount": 6,
        "isConfirmed": false
      }
    ],
    "volunteerMeetingPoint": "Pokhran Road No. 1, Near Vartak Nagar Bus Depot, Thane West (Near Landmark)",
    "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
    "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
    "registeredVolunteersCount": 15
  }
];
