/**
 * WardSync Backend API Client
 * Seamlessly connects wardsync-frontend to the Unified Civic Engine & Pipeline backend.
 */

import { Issue, VolunteerRegistration, DonationRecord, NgoEvent, NgoFundraisingCampaign } from '../types';
import { SAMPLE_ISSUES } from '../data/sampleIssues';

const RAW_BASE = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, '') || '';
const API_BASE = `${RAW_BASE}/api`;

export const civicApi = {
  /**
   * Fetch all verified issues with complete intelligence dossiers from backend.
   * Gracefully falls back to SAMPLE_ISSUES if the backend is currently starting up.
   */
  async fetchIssues(): Promise<Issue[]> {
    try {
      const response = await fetch(`${API_BASE}/public/issues`, {
        headers: { 'Accept': 'application/json' },
      });
      if (!response.ok) {
        console.warn(`[WardSync API] Failed to fetch issues (${response.status}). Using fallback sample data.`);
        return SAMPLE_ISSUES;
      }
      const data: Issue[] = await response.json();
      return data.length > 0 ? data : SAMPLE_ISSUES;
    } catch (err) {
      console.warn('[WardSync API] Backend offline or unreachable. Operating in offline demo mode with sample issues.', err);
      return SAMPLE_ISSUES;
    }
  },

  /**
   * Citizen reports a new civic issue.
   * Triggers AI verification, credibility scoring, authority mapping, and action blueprinting.
   */
  async reportIssue(issue: Partial<Issue> & { evidenceNote?: string }): Promise<Issue | null> {
    try {
      const payload = {
        title: issue.title,
        category: issue.category,
        ward: issue.ward,
        locality: issue.locality,
        description: issue.description,
        severity: issue.severity || 'High',
        evidenceNote: issue.evidenceNote || issue.description,
        latitude: issue.latitude,
        longitude: issue.longitude,
      };

      const response = await fetch(`${API_BASE}/public/issues`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Report issue failed with status ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      console.error('[WardSync API] Error reporting issue to backend:', err);
      return null;
    }
  },

  /**
   * Citizen registers for volunteer mobilization slot.
   */
  async registerVolunteer(reg: VolunteerRegistration): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE}/events/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_id: reg.issueId, // or linked event ID
          citizen_name: reg.volunteerName,
          citizen_email: reg.contact.includes('@') ? reg.contact : 'volunteer@citizen.in',
          phone: reg.contact,
          participant_count: reg.participantCount,
          skills_notes: reg.skills,
        }),
      });
      return response.ok;
    } catch (err) {
      console.warn('[WardSync API] Error syncing volunteer registration:', err);
      return false;
    }
  },

  /**
   * Citizen completes simulated donation toward NGO relief drive.
   */
  async recordDonation(donation: DonationRecord): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE}/donations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          issueId: donation.issueId,
          amount: donation.amount,
          donorName: donation.donorName,
          isAnonymous: donation.isAnonymous,
        }),
      });
      return response.ok;
    } catch (err) {
      console.warn('[WardSync API] Error syncing donation:', err);
      return false;
    }
  },

  /**
   * NGO launches a fundraising campaign.
   */
  async launchCampaign(campaign: NgoFundraisingCampaign): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE}/campaigns`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          issueId: campaign.issueId,
          targetAmount: campaign.targetAmount,
          purpose: campaign.purpose,
          beneficiaryOrg: campaign.beneficiaryOrg,
        }),
      });
      return response.ok;
    } catch (err) {
      console.warn('[WardSync API] Error syncing campaign:', err);
      return false;
    }
  },

  /**
   * NGO accepts and publishes a volunteer mobilization event blueprint.
   */
  async publishNgoEvent(event: NgoEvent): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE}/events/publish`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_id: event.id,
          ngo_id: 'c1111111-1111-4111-8111-111111111111',
          event_title: event.title,
          event_date: new Date().toISOString().split('T')[0],
          meeting_point: event.meetingPoint,
          target_volunteers: event.maxVolunteers,
          required_gear: [event.resourcesRequired],
          tasks_breakdown: [event.activityDescription],
          safety_guidelines: ['Follow safety instructions', 'Wear required gear'],
        }),
      });
      return response.ok;
    } catch (err) {
      console.warn('[WardSync API] Error publishing NGO event:', err);
      return false;
    }
  },

  /**
   * Government dashboard updates status of an issue.
   */
  async updateIssueStatus(issueId: string, status: string): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE}/issues/${issueId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      });
      return response.ok;
    } catch (err) {
      console.warn('[WardSync API] Error updating issue status:', err);
      return false;
    }
  },

  /**
   * Check unified health status of all engines.
   */
  async checkHealth(): Promise<Record<string, unknown> | null> {
    try {
      const response = await fetch(`${RAW_BASE}/health`);
      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch {
      return null;
    }
  },
};
