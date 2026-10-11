export type SeverityLevel = 'Critical' | 'High' | 'Moderate' | 'Low';
export type IssueStatus = 'Reported' | 'Verified' | 'In progress' | 'Resolved';
export type IssueCategory = 
  | 'Water & Sanitation' 
  | 'Health' 
  | 'Roads & Transport' 
  | 'Public Safety' 
  | 'Waste Management' 
  | 'Environment';

export interface EvidenceSource {
  id: string;
  title: string;
  type: 'Official Record' | 'Lab Analysis' | 'Citizen Report' | 'News Media' | 'NGO Survey';
  date: string;
  link?: string;
  excerpt: string;
  isOfficial: boolean;
  credibilityScore: number; // 0 - 100
}

export interface VolunteerSlot {
  id: string;
  dateTime: string;
  voteCount: number;
  isConfirmed: boolean;
  isPopular?: boolean;
}

export interface Issue {
  id: string;
  title: string;
  locationName: string;
  ward: string;
  locality: string;
  distanceKm: number;
  latitude: number;
  longitude: number;
  category: IssueCategory;
  severity: SeverityLevel;
  urgency: 'Immediate (24h)' | 'Urgent (48-72h)' | 'Moderate (1-2 weeks)' | 'Scheduled';
  status: IssueStatus;
  evidenceConfidence: number; // e.g. 82%
  dateDiscovered: string;
  description: string;
  
  // "What do we know?" section
  cause: {
    documented: string;
    isVerified: boolean;
  };
  affectedPeople: string;
  likelyImpact: string;
  unverifiedAspects: string;
  
  // "Who can help?" section
  responsibleAuthority: {
    name: string;
    department: string;
    contact: string;
    officialStatus: string;
  };
  relevantNgos: Array<{
    name: string;
    verified: boolean;
    focus: string;
  }>;
  availableResources: string[];
  
  // Evidence
  evidence: EvidenceSource[];
  contradictingEvidence?: string;
  mergedReportsCount: number;

  // Action plan
  actionPlan: Array<{
    phase: string;
    description: string;
    status: 'Completed' | 'In progress' | 'Pending';
  }>;

  // Donation campaign
  donationGoal: number;
  donationRaised: number;
  donationBeneficiary: string;

  // Volunteer Coordination
  volunteerSlots: VolunteerSlot[];
  volunteerMeetingPoint: string;
  volunteerActivity: string;
  volunteerResourcesRequired: string;
  registeredVolunteersCount: number;
}

export type UserRole = 'citizen' | 'ngo' | 'government' | 'admin';

export interface UserAccount {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  isVerified: boolean;
  phone?: string;
  locality?: string;
  organizationName?: string;
  focusAreas?: string;
  serviceAreas?: string;
  department?: string;
  designation?: string;
  jurisdiction?: string;
}

export interface DonationRecord {
  id: string;
  issueId: string;
  issueTitle: string;
  amount: number;
  donorName: string;
  isAnonymous: boolean;
  date: string;
  simulatedTxnId: string;
}

export interface VolunteerRegistration {
  id: string;
  issueId: string;
  issueTitle: string;
  volunteerName: string;
  contact: string;
  skills: string;
  slotDateTime: string;
  participantCount: number;
  status: 'Confirmed' | 'Pending Organizer Approval';
}

export interface NgoEvent {
  id: string;
  issueId: string;
  issueTitle: string;
  title: string;
  dateTime: string;
  meetingPoint: string;
  maxVolunteers: number;
  enrolledCount: number;
  activityDescription: string;
  resourcesRequired: string;
  leadCoordinator: string;
  contactPhone: string;
  status: 'Upcoming' | 'In Progress' | 'Completed';
}

export interface NgoFundraisingCampaign {
  id: string;
  issueId: string;
  issueTitle: string;
  targetAmount: number;
  raisedAmount: number;
  purpose: string;
  beneficiaryOrg: string;
  status: 'Active' | 'Target Reached' | 'Closed';
}
