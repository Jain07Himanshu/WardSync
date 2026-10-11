import React, { useState } from 'react';
import { 
  User, Building2, Landmark, ShieldCheck, CheckCircle2, 
  Clock, Heart, Users, MapPin, Check, 
  CircleDollarSign, CalendarPlus, AlertCircle
} from 'lucide-react';
import { Issue, UserAccount, DonationRecord, VolunteerRegistration, NgoEvent, NgoFundraisingCampaign } from '../types';
import { IssueMap } from './IssueMap';
import { FeaturedIssueCard } from './FeaturedIssueCard';

interface DashboardsProps {
  currentUser: UserAccount | null;
  issues: Issue[];
  selectedIssue: Issue;
  donations: DonationRecord[];
  volunteerRegistrations: VolunteerRegistration[];
  ngoEvents: NgoEvent[];
  ngoCampaigns: NgoFundraisingCampaign[];
  onSelectIssue: (issue: Issue) => void;
  onUpdateIssueStatus: (issueId: string, newStatus: Issue['status']) => void;
  onOpenReportModal: () => void;
  onRaiseFunds: (issue: Issue) => void;
  onCreateEvent: (issue: Issue) => void;
  onKnowMore: (issue: Issue) => void;
}

export const Dashboards: React.FC<DashboardsProps> = ({
  currentUser,
  issues,
  selectedIssue,
  donations,
  volunteerRegistrations,
  ngoEvents,
  ngoCampaigns,
  onSelectIssue,
  onUpdateIssueStatus,
  onOpenReportModal,
  onRaiseFunds,
  onCreateEvent,
  onKnowMore
}) => {
  const activeRole = currentUser?.role || 'citizen';
  const [selectedTab, setSelectedTab] = useState<'citizen' | 'ngo' | 'government' | 'admin'>(activeRole);

  // Simulated Admin approval state for prototype
  const [pendingNgos, setPendingNgos] = useState([
    { id: 'p-ngo-1', name: 'Youth Green Volunteers Trust', regNo: 'MH-2024-MUM-91', contact: 'youthgreen@trust.org', docs: '80G_Cert.pdf' }
  ]);
  const [pendingGovs, setPendingGovs] = useState([
    { id: 'p-gov-1', name: 'Er. S. More (BMC Roads)', email: 'smore.roads@mcgm.gov.in', jurisdiction: 'Ward G/North & Ward 3 (Thane)' }
  ]);

  const handleApproveNgo = (id: string) => {
    setPendingNgos(pendingNgos.filter((n) => n.id !== id));
  };

  const handleApproveGov = (id: string) => {
    setPendingGovs(pendingGovs.filter((g) => g.id !== id));
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Dashboard Role Selector Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-200">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Civic Action Hub & Dashboards
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Role-based visibility, event management, and execution workflows.
          </p>
        </div>

        {/* Tab switchers */}
        <div className="flex rounded-xl bg-slate-100 p-1 text-xs font-semibold">
          <button
            onClick={() => setSelectedTab('citizen')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              selectedTab === 'citizen' ? 'bg-white text-sky-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <User className="w-3.5 h-3.5" />
            Citizen
          </button>
          <button
            onClick={() => setSelectedTab('ngo')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              selectedTab === 'ngo' ? 'bg-white text-emerald-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Building2 className="w-3.5 h-3.5" />
            NGO Workspace
          </button>
          <button
            onClick={() => setSelectedTab('government')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              selectedTab === 'government' ? 'bg-white text-amber-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Landmark className="w-3.5 h-3.5" />
            Government
          </button>
          <button
            onClick={() => setSelectedTab('admin')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              selectedTab === 'admin' ? 'bg-white text-purple-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            Admin
          </button>
        </div>
      </div>

      {/* 1. CITIZEN DASHBOARD */}
      {selectedTab === 'citizen' && (
        <div className="py-8 space-y-8 animate-in fade-in">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-sky-50 border border-sky-200 rounded-2xl p-6">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-slate-900">Welcome, {currentUser?.name || 'Citizen'}</h2>
                <span className="bg-sky-200/70 text-sky-900 text-xs px-2 py-0.5 rounded font-semibold">Active Citizen</span>
              </div>
              <p className="text-xs text-slate-600 mt-1">
                Your primary locality: <strong>{currentUser?.locality || 'Dadar West, Ward G/North, Mumbai'}</strong>
              </p>
            </div>
            <button
              onClick={onOpenReportModal}
              className="bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs px-4 py-2.5 rounded-lg shadow-xs transition"
            >
              + Report a Civic Issue
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Volunteer Events RSVP */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                  <Users className="w-4 h-4 text-emerald-600" />
                  My Registered Volunteer Activities
                </h3>
                <span className="text-xs text-slate-500 font-semibold">{volunteerRegistrations.length} events</span>
              </div>

              {volunteerRegistrations.length === 0 ? (
                <p className="text-xs text-slate-500 py-6 text-center">
                  You haven't signed up for any volunteer drives yet. Explore issues to join local relief actions!
                </p>
              ) : (
                <div className="space-y-3">
                  {volunteerRegistrations.map((v) => (
                    <div key={v.id} className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1">
                      <p className="font-semibold text-slate-900">{v.issueTitle}</p>
                      <p className="text-slate-600 flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" /> {v.slotDateTime}
                      </p>
                      <div className="flex justify-between items-center pt-1 text-[11px]">
                        <span className="text-slate-500">{v.participantCount} participant(s) registered</span>
                        <span className="text-emerald-700 font-semibold">{v.status}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Simulated Donation Receipts */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                  <Heart className="w-4 h-4 text-sky-600" />
                  My Simulated Contributions
                </h3>
                <span className="text-xs text-slate-500 font-semibold">{donations.length} records</span>
              </div>

              {donations.length === 0 ? (
                <p className="text-xs text-slate-500 py-6 text-center">
                  No contributions made yet. You can support local NGO relief drives through simulated demo payments.
                </p>
              ) : (
                <div className="space-y-3">
                  {donations.map((d) => (
                    <div key={d.id} className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs flex justify-between items-center">
                      <div>
                        <p className="font-semibold text-slate-900">{d.issueTitle}</p>
                        <p className="text-slate-400 text-[11px] font-mono mt-0.5">{d.simulatedTxnId} · {d.date}</p>
                      </div>
                      <div className="text-right">
                        <span className="font-bold text-emerald-700 text-sm">₹{d.amount.toLocaleString()}</span>
                        <span className="block text-[10px] text-slate-400">Demo Success</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Local Watchlist */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs">
            <h3 className="font-bold text-slate-900 text-base mb-4 flex items-center gap-2">
              <MapPin className="w-4 h-4 text-sky-600" />
              Civic Issues in Your Locality ({issues.length})
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {issues.slice(0, 3).map((iss) => (
                <div key={iss.id} className="border border-slate-200 rounded-xl p-4 text-xs bg-slate-50/50 flex flex-col justify-between">
                  <div>
                    <span className="text-[10px] font-bold text-sky-700">{iss.category}</span>
                    <h4 className="font-semibold text-slate-900 mt-1 line-clamp-1">{iss.title}</h4>
                    <p className="text-slate-500 mt-1">{iss.distanceKm} km away · {iss.status}</p>
                  </div>
                  <button
                    onClick={() => onSelectIssue(iss)}
                    className="mt-3 text-sky-600 font-semibold hover:underline text-left"
                  >
                    View in map & action &rarr;
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 2. NGO WORKSPACE DASHBOARD (COMPREHENSIVE MAP + ACTIONS + EVENTS + FUNDS) */}
      {selectedTab === 'ngo' && (
        <div className="py-8 space-y-8 animate-in fade-in">
          {/* Organization Profile Card */}
          <div className="bg-emerald-50/60 border border-emerald-200 rounded-2xl p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-slate-900">
                  {currentUser?.organizationName || 'Mumbai March Civic Action Collective'}
                </h2>
                <span className="bg-emerald-200 text-emerald-900 text-xs px-2.5 py-0.5 rounded-full font-semibold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Officially Verified NGO
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-1">
                Focus Areas: <strong>Pothole Audits, Public Safety & Drainage Relief</strong> · Service Jurisdiction: <strong>Mumbai & Thane Metropolitan Region</strong>
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => onCreateEvent(selectedIssue)}
                className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-xs transition"
              >
                <CalendarPlus className="w-4 h-4" />
                <span>+ Create Event</span>
              </button>
              <button
                onClick={() => onRaiseFunds(selectedIssue)}
                className="bg-[#0284c7] hover:bg-[#0369a1] text-white font-semibold text-xs px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-xs transition"
              >
                <CircleDollarSign className="w-4 h-4" />
                <span>+ Raise Funds</span>
              </button>
            </div>
          </div>

          {/* Civic Issues Map & NGO Action Console matching request:
              "the map park would be the same as it is in the citizen now as there is donate , voluenter n more info in the citizen change that to raise funds , create event and more info" */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold text-slate-900">NGO Civic Action Console</h3>
                <p className="text-xs text-slate-500">
                  Select an issue on the map to deploy fundraising campaigns or schedule volunteer operations.
                </p>
              </div>
              <div className="text-xs text-slate-500 font-medium">
                Selected: <strong className="text-slate-800">{selectedIssue.title}</strong>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
              <div className="lg:col-span-7">
                <IssueMap
                  issues={issues}
                  selectedIssue={selectedIssue}
                  onSelectIssue={onSelectIssue}
                />
              </div>

              <div className="lg:col-span-5">
                <FeaturedIssueCard
                  issue={selectedIssue}
                  isNgoRole={true}
                  onDonate={() => {}}
                  onVolunteer={() => {}}
                  onKnowMore={onKnowMore}
                  onRaiseFunds={onRaiseFunds}
                  onCreateEvent={onCreateEvent}
                />
              </div>
            </div>
          </div>

          {/* NGO EVENTS & CAMPAIGNS HUB */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Created Events Hub */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                    <CalendarPlus className="w-4 h-4 text-emerald-600" />
                    Scheduled Volunteer Events ({ngoEvents.length})
                  </h3>
                  <button
                    onClick={() => onCreateEvent(selectedIssue)}
                    className="text-xs font-semibold text-emerald-700 hover:underline flex items-center gap-1"
                  >
                    <span>+ New Event</span>
                  </button>
                </div>

                <div className="space-y-3">
                  {ngoEvents.map((ev) => (
                    <div key={ev.id} className="p-4 bg-emerald-50/40 border border-emerald-200/80 rounded-xl text-xs space-y-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-bold text-slate-900 text-sm">{ev.title}</p>
                          <p className="text-slate-500 text-[11px] font-medium mt-0.5">For: {ev.issueTitle}</p>
                        </div>
                        <span className="bg-emerald-200 text-emerald-900 text-[10px] font-bold px-2 py-0.5 rounded">
                          {ev.status}
                        </span>
                      </div>

                      <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-600 bg-white p-2.5 rounded-lg border border-emerald-100">
                        <div>
                          <span className="text-slate-400 block">Date & Time:</span>
                          <span className="font-semibold text-slate-800">{ev.dateTime}</span>
                        </div>
                        <div>
                          <span className="text-slate-400 block">Meeting Point:</span>
                          <span className="font-semibold text-slate-800 truncate block">{ev.meetingPoint}</span>
                        </div>
                      </div>

                      <div className="flex justify-between items-center text-[11px] pt-1">
                        <span className="text-slate-500">
                          Capacity: <strong>{ev.enrolledCount}</strong> / {ev.maxVolunteers} volunteers enrolled
                        </span>
                        <span className="text-slate-500 font-mono">
                          Lead: {ev.contactPhone}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <p className="text-[11px] text-slate-400 italic mt-4 pt-2 border-t border-slate-100">
                Events created here are immediately shown to citizens on the issue card for 1-click RSVP.
              </p>
            </div>

            {/* Active Fundraising Campaigns Hub */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                    <CircleDollarSign className="w-4 h-4 text-sky-600" />
                    Active Fundraising Campaigns ({ngoCampaigns.length})
                  </h3>
                  <button
                    onClick={() => onRaiseFunds(selectedIssue)}
                    className="text-xs font-semibold text-sky-700 hover:underline flex items-center gap-1"
                  >
                    <span>+ Launch Campaign</span>
                  </button>
                </div>

                <div className="space-y-3">
                  {ngoCampaigns.map((camp) => {
                    const percent = Math.min(100, Math.round((camp.raisedAmount / camp.targetAmount) * 100));

                    return (
                      <div key={camp.id} className="p-4 bg-sky-50/40 border border-sky-200/80 rounded-xl text-xs space-y-2.5">
                        <div className="flex justify-between items-start">
                          <div>
                            <p className="font-bold text-slate-900 text-sm">{camp.issueTitle}</p>
                            <p className="text-slate-500 text-[11px] line-clamp-1">{camp.purpose}</p>
                          </div>
                          <span className="bg-sky-200 text-sky-900 text-[10px] font-bold px-2 py-0.5 rounded">
                            {camp.status}
                          </span>
                        </div>

                        <div className="space-y-1">
                          <div className="flex justify-between text-[11px]">
                            <span className="text-slate-500">Collected: <strong className="text-emerald-700 font-bold">₹{camp.raisedAmount.toLocaleString()}</strong></span>
                            <span className="text-slate-500">Goal: <strong className="text-slate-800">₹{camp.targetAmount.toLocaleString()}</strong></span>
                          </div>
                          <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                            <div className="h-full bg-sky-600 rounded-full" style={{ width: `${percent}%` }} />
                          </div>
                          <div className="flex justify-between text-[10px] text-slate-400">
                            <span>{percent}% funded by citizens</span>
                            <span>Remaining: ₹{Math.max(0, camp.targetAmount - camp.raisedAmount).toLocaleString()}</span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-[11px] text-slate-600 mt-4 flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                <span>
                  Disbursements are held in audited escrow. Proof of expenditure must be uploaded once funds are utilized.
                </span>
              </div>
            </div>
          </div>

          {/* Registered Volunteers Roster */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <Users className="w-4 h-4 text-emerald-600" />
                Citizen Volunteer Sign-up Roster ({volunteerRegistrations.length})
              </h3>
              <span className="text-xs text-slate-500">Updated in real-time</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-400 font-semibold uppercase text-[11px]">
                    <th className="pb-3">Volunteer Name</th>
                    <th className="pb-3">Civic Issue</th>
                    <th className="pb-3">Event Slot</th>
                    <th className="pb-3">Contact</th>
                    <th className="pb-3">Skills / Background</th>
                    <th className="pb-3 text-right">Headcount</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {volunteerRegistrations.map((reg) => (
                    <tr key={reg.id} className="hover:bg-slate-50/60">
                      <td className="py-3 font-semibold text-slate-900">{reg.volunteerName}</td>
                      <td className="py-3 text-slate-600 max-w-[200px] truncate">{reg.issueTitle}</td>
                      <td className="py-3 text-slate-600">{reg.slotDateTime}</td>
                      <td className="py-3 font-mono text-[11px] text-sky-700">{reg.contact}</td>
                      <td className="py-3 text-slate-600">{reg.skills}</td>
                      <td className="py-3 text-right font-bold text-emerald-700">+{reg.participantCount}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 3. GOVERNMENT AUTHORITY DASHBOARD */}
      {selectedTab === 'government' && (
        <div className="py-8 space-y-8 animate-in fade-in">
          {/* Municipal Authority Header */}
          <div className="bg-amber-50/60 border border-amber-200 rounded-2xl p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-slate-900">
                  {currentUser?.name || 'Er. Rajesh Sawant'}
                </h2>
                <span className="bg-amber-200 text-amber-900 text-xs px-2.5 py-0.5 rounded-full font-semibold flex items-center gap-1">
                  <Landmark className="w-3.5 h-3.5" /> Official Department Desk
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-1">
                {currentUser?.department || 'Brihanmumbai Municipal Corporation (BMC) & TMC Directorate'} · Jurisdiction: <strong>Ward G/North & Ward 1 (Thane)</strong>
              </p>
            </div>
            <div className="text-xs font-mono bg-white px-3 py-2 rounded-xl border border-amber-200 text-amber-900">
              Desk: bmc.civic@mcgm.gov.in
            </div>
          </div>

          {/* Priority Queue & Status Updaters */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
              <div>
                <h3 className="font-bold text-slate-900 text-base">Jurisdiction Priority Action Queue</h3>
                <p className="text-xs text-slate-500">Sorted by Severity, Urgency and Verified Evidence Confidence.</p>
              </div>
              <span className="text-xs text-slate-500 font-semibold">{issues.length} active civic files</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-400 font-semibold uppercase text-[11px]">
                    <th className="pb-3">Issue Title</th>
                    <th className="pb-3">Ward & Locality</th>
                    <th className="pb-3">Severity</th>
                    <th className="pb-3">Evidence Confidence</th>
                    <th className="pb-3">Current Status</th>
                    <th className="pb-3 text-right">Update Resolution</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {issues.map((iss) => (
                    <tr key={iss.id} className="hover:bg-slate-50/60">
                      <td className="py-3.5 font-semibold text-slate-900 max-w-[220px] truncate">
                        {iss.title}
                      </td>
                      <td className="py-3.5 text-slate-600">{iss.ward}, {iss.locality}</td>
                      <td className="py-3.5">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          iss.severity === 'Critical' ? 'bg-red-100 text-red-700' : 'bg-orange-100 text-orange-700'
                        }`}>
                          {iss.severity}
                        </span>
                      </td>
                      <td className="py-3.5 font-semibold text-sky-700">{iss.evidenceConfidence}%</td>
                      <td className="py-3.5">
                        <span className="font-medium text-slate-700">{iss.status}</span>
                      </td>
                      <td className="py-3.5 text-right">
                        <div className="inline-flex gap-1">
                          <button
                            onClick={() => onUpdateIssueStatus(iss.id, 'In progress')}
                            className={`px-2 py-1 rounded text-[11px] font-semibold border ${
                              iss.status === 'In progress' ? 'bg-sky-600 text-white border-sky-600' : 'bg-white hover:bg-slate-100 text-slate-700 border-slate-300'
                            }`}
                          >
                            In Progress
                          </button>
                          <button
                            onClick={() => onUpdateIssueStatus(iss.id, 'Resolved')}
                            className={`px-2 py-1 rounded text-[11px] font-semibold border ${
                              iss.status === 'Resolved' ? 'bg-emerald-600 text-white border-emerald-600' : 'bg-white hover:bg-slate-100 text-emerald-700 border-slate-300'
                            }`}
                          >
                            Resolved
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 4. ADMIN DASHBOARD */}
      {selectedTab === 'admin' && (
        <div className="py-8 space-y-8 animate-in fade-in">
          {/* Admin Header */}
          <div className="bg-purple-50/60 border border-purple-200 rounded-2xl p-6">
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-purple-600" />
              Platform Moderation & Verification Desk
            </h2>
            <p className="text-xs text-slate-600 mt-1">
              Review NGO documents, verify municipal officer affiliations, and supervise evidence authenticity.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* NGO Approvals Queue */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs">
              <h3 className="font-bold text-slate-900 text-base mb-3 flex items-center gap-2">
                <Building2 className="w-4 h-4 text-emerald-600" />
                Pending NGO Verification Requests ({pendingNgos.length})
              </h3>

              {pendingNgos.length === 0 ? (
                <p className="text-xs text-slate-500 py-6 text-center">All NGO applications processed!</p>
              ) : (
                <div className="space-y-3">
                  {pendingNgos.map((ngo) => (
                    <div key={ngo.id} className="p-3.5 border border-slate-200 rounded-xl text-xs bg-slate-50/50 space-y-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-semibold text-slate-900">{ngo.name}</p>
                          <p className="text-slate-500 text-[11px]">{ngo.contact} · {ngo.regNo}</p>
                        </div>
                        <span className="text-[10px] bg-amber-100 text-amber-800 px-2 py-0.5 rounded font-semibold">Review Doc</span>
                      </div>
                      <div className="flex justify-end gap-2 pt-1">
                        <button
                          onClick={() => handleApproveNgo(ngo.id)}
                          className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-semibold flex items-center gap-1"
                        >
                          <Check className="w-3.5 h-3.5" /> Approve & Grant Verified Badge
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Gov Authority Approvals Queue */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs">
              <h3 className="font-bold text-slate-900 text-base mb-3 flex items-center gap-2">
                <Landmark className="w-4 h-4 text-amber-600" />
                Pending Government Official Requests ({pendingGovs.length})
              </h3>

              {pendingGovs.length === 0 ? (
                <p className="text-xs text-slate-500 py-6 text-center">All official requests validated!</p>
              ) : (
                <div className="space-y-3">
                  {pendingGovs.map((gov) => (
                    <div key={gov.id} className="p-3.5 border border-slate-200 rounded-xl text-xs bg-slate-50/50 space-y-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-semibold text-slate-900">{gov.name}</p>
                          <p className="text-slate-500 text-[11px]">{gov.email} · Jurisdiction: {gov.jurisdiction}</p>
                        </div>
                        <span className="text-[10px] bg-amber-100 text-amber-800 px-2 py-0.5 rounded font-semibold">Pending</span>
                      </div>
                      <div className="flex justify-end gap-2 pt-1">
                        <button
                          onClick={() => handleApproveGov(gov.id)}
                          className="px-2.5 py-1 bg-amber-600 hover:bg-amber-700 text-white rounded text-xs font-semibold flex items-center gap-1"
                        >
                          <Check className="w-3.5 h-3.5" /> Validate Gov Authority
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
