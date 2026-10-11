import React from 'react';
import { Shield, Users, CheckCircle, MapPin, Mail, ArrowLeft } from 'lucide-react';

interface InfoPagesProps {
  view: 'about' | 'privacy' | 'terms' | 'contact' | 'explore' | 'volunteer';
  onBackToHome: () => void;
  onExploreIssueClick?: () => void;
  onVolunteerClick?: () => void;
}

export const InfoPages: React.FC<InfoPagesProps> = ({
  view,
  onBackToHome,
  onExploreIssueClick,
  onVolunteerClick
}) => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-in fade-in">
      <button
        onClick={onBackToHome}
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-sky-600 hover:text-sky-800 mb-6 group"
      >
        <ArrowLeft className="w-4 h-4 transition group-hover:-translate-x-1" />
        <span>Return to Home & Map</span>
      </button>

      {view === 'about' && (
        <div className="space-y-6 text-slate-700">
          <div className="border-b border-slate-200 pb-4">
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">About WardSync</h1>
            <p className="text-base text-slate-500 mt-1">Local Problems. Collective Action.</p>
          </div>

          <p className="text-sm leading-relaxed">
            <strong>WardSync</strong> is a civic action platform engineered to bridge the persistent gap between citizen grievances, ground NGOs, and municipal authorities. Instead of grievances disappearing into black boxes, WardSync aggregates citizen reports, correlates them with official records and lab analyses, and clusters duplicate listings into transparent, action-oriented neighborhood files.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4">
            <div className="p-4 border border-slate-200 rounded-xl bg-slate-50">
              <Shield className="w-6 h-6 text-sky-600 mb-2" />
              <h3 className="font-bold text-slate-900 text-sm">Evidence-First Integrity</h3>
              <p className="text-xs text-slate-600 mt-1">Every issue maintains an evidence trail, distinguishing official municipal records from citizen tips.</p>
            </div>
            <div className="p-4 border border-slate-200 rounded-xl bg-slate-50">
              <Users className="w-6 h-6 text-emerald-600 mb-2" />
              <h3 className="font-bold text-slate-900 text-sm">Collective Coordination</h3>
              <p className="text-xs text-slate-600 mt-1">Volunteer scheduling via group polling brings citizens and verified NGOs together on confirmed slots.</p>
            </div>
            <div className="p-4 border border-slate-200 rounded-xl bg-slate-50">
              <CheckCircle className="w-6 h-6 text-amber-600 mb-2" />
              <h3 className="font-bold text-slate-900 text-sm">Accountable Resolution</h3>
              <p className="text-xs text-slate-600 mt-1">Government authorities track prioritized ward queues and log official status milestones directly.</p>
            </div>
          </div>
        </div>
      )}

      {view === 'privacy' && (
        <div className="space-y-4 text-slate-700 text-sm">
          <h1 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-3">Privacy Policy</h1>
          <p>
            WardSync respects citizen privacy. When reporting civic issues, citizens can choose to remain anonymous on public issue logs. Location data collected via browser geolocation is utilized strictly to determine municipal ward proximity and is never sold or distributed to commercial advertisers.
          </p>
          <p>
            In this prototype demonstration, simulated donations and mock volunteer registrations do not store financial or confidential identity credentials.
          </p>
        </div>
      )}

      {view === 'terms' && (
        <div className="space-y-4 text-slate-700 text-sm">
          <h1 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-3">Terms of Civic Coordination</h1>
          <p>
            Users of WardSync agree to submit accurate, non-defamatory reports. Disinformation, false emergencies, or fraudulent verification claims will lead to account suspension by platform administrators.
          </p>
          <p>
            Only organizations verified by WardSync administration with legitimate 80G/FCRA documentation are eligible to coordinate community relief campaigns.
          </p>
        </div>
      )}

      {view === 'contact' && (
        <div className="space-y-6 text-slate-700">
          <h1 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-3">Contact WardSync Desk</h1>
          <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200 space-y-3 text-sm">
            <div className="flex items-center gap-2">
              <Mail className="w-4 h-4 text-sky-600" />
              <span>General Inquiries: <strong className="text-slate-900">desk@wardsync.org</strong></span>
            </div>
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-emerald-600" />
              <span>NGO Verification Liaison: <strong className="text-slate-900">verify-ngo@wardsync.org</strong></span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-amber-600" />
              <span>Civic Operations Center: Mumbai & Thane Metropolitan Innovation Hub, BKC, Mumbai 400051</span>
            </div>
          </div>
        </div>
      )}

      {view === 'explore' && (
        <div className="space-y-6 text-slate-700">
          <h1 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-3">Explore Local Civic Issues</h1>
          <p className="text-sm">
            Browse through active neighborhood issues sorted by severity, location proximity, and evidence confidence score. Use our interactive map on the homepage to inspect geo-located markers.
          </p>
          <button
            onClick={onBackToHome}
            className="px-4 py-2 bg-sky-600 hover:bg-sky-700 text-white text-xs font-semibold rounded-lg shadow-xs"
          >
            Launch Interactive Map on Home
          </button>
        </div>
      )}

      {view === 'volunteer' && (
        <div className="space-y-6 text-slate-700">
          <h1 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-3">Volunteer Opportunities</h1>
          <p className="text-sm">
            WardSync pairs citizens with verified community relief drives. Check the most important issue near you to join scheduled door-to-door distributions or safety patrols.
          </p>
          <button
            onClick={onBackToHome}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-xs"
          >
            View Active Volunteer Drives
          </button>
        </div>
      )}
    </div>
  );
};
