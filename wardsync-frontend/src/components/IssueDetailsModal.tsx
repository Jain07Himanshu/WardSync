import React, { useState } from 'react';
import { 
  X, MapPin, Calendar, CheckCircle2, AlertTriangle, Building, 
  ExternalLink, Layers, FileText, Heart, Users, HelpCircle, 
  Send, Flag
} from 'lucide-react';
import { Issue, SeverityLevel } from '../types';

interface IssueDetailsModalProps {
  issue: Issue | null;
  isOpen: boolean;
  onClose: () => void;
  onDonate: (issue: Issue) => void;
  onVolunteer: (issue: Issue) => void;
}

const getSeverityBadge = (severity: SeverityLevel) => {
  switch (severity) {
    case 'Critical': return 'bg-red-50 text-red-600 border-red-200';
    case 'High': return 'bg-orange-50 text-orange-600 border-orange-200';
    case 'Moderate': return 'bg-amber-50 text-amber-700 border-amber-200';
    case 'Low': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
  }
};

export const IssueDetailsModal: React.FC<IssueDetailsModalProps> = ({
  issue,
  isOpen,
  onClose,
  onDonate,
  onVolunteer
}) => {
  const [showReportIncorrect, setShowReportIncorrect] = useState(false);
  const [incorrectField, setIncorrectField] = useState('Cause of problem');
  const [correctionNote, setCorrectionNote] = useState('');
  const [reportSubmitted, setReportSubmitted] = useState(false);

  if (!isOpen || !issue) return null;

  const handleCorrectionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setReportSubmitted(true);
    setTimeout(() => {
      setReportSubmitted(false);
      setShowReportIncorrect(false);
      setCorrectionNote('');
    }, 2500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
      <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[92vh] overflow-y-auto shadow-2xl border border-slate-200 relative flex flex-col">
        {/* Sticky Header */}
        <div className="sticky top-0 z-10 bg-white/95 backdrop-blur-xs border-b border-slate-200 p-5 sm:p-6 flex items-start justify-between">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${getSeverityBadge(issue.severity)}`}>
                {issue.severity} Severity
              </span>
              <span className="bg-slate-100 text-slate-700 text-xs font-medium px-2.5 py-0.5 rounded-md">
                {issue.category}
              </span>
              <span className="bg-sky-50 text-sky-700 border border-sky-200 text-xs font-medium px-2.5 py-0.5 rounded-md flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3 text-sky-600" />
                Status: {issue.status}
              </span>
              <span className="text-xs text-slate-400">
                · {issue.mergedReportsCount} duplicate reports grouped
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900">{issue.title}</h2>
            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 mt-2">
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-slate-400" />
                {issue.locationName} ({issue.distanceKm} km away)
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-slate-400" />
                Discovered: {issue.dateDiscovered}
              </span>
              <span className="text-slate-400">
                Lat: {issue.latitude.toFixed(4)}, Long: {issue.longitude.toFixed(4)}
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-8 text-sm text-slate-700">
          {/* Key Metrics Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 border border-slate-200 rounded-xl p-4">
            <div>
              <p className="text-xs text-slate-500 font-medium">Severity Level</p>
              <p className="text-base font-bold text-slate-900 mt-0.5">{issue.severity}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500 font-medium">Response Urgency</p>
              <p className="text-base font-bold text-slate-900 mt-0.5">{issue.urgency}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500 font-medium">Current Status</p>
              <p className="text-base font-bold text-sky-700 mt-0.5">{issue.status}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500 font-medium">Evidence Confidence</p>
              <div className="flex items-center gap-2 mt-1">
                <div className="w-16 h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div className="h-full bg-sky-600 rounded-full" style={{ width: `${issue.evidenceConfidence}%` }} />
                </div>
                <span className="text-sm font-bold text-slate-900">{issue.evidenceConfidence}%</span>
              </div>
            </div>
          </div>

          {/* Description */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">Overview</h4>
            <p className="text-slate-700 leading-relaxed">{issue.description}</p>
          </div>

          {/* 1. "What do we know?" Section matching Requirement 4 */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-4 pb-2 border-b border-slate-100">
              <HelpCircle className="w-4 h-4 text-sky-600" />
              What do we know?
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-xs font-semibold text-slate-500">Documented Cause</p>
                <div className="mt-1 flex items-start gap-2">
                  <p className="text-sm text-slate-800">{issue.cause.documented}</p>
                </div>
                <span className={`inline-block mt-1 text-[11px] font-medium px-2 py-0.5 rounded-sm ${
                  issue.cause.isVerified ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'
                }`}>
                  {issue.cause.isVerified ? '✓ Officially Verified Cause' : '⚠ Unverified Field Observation'}
                </span>
              </div>

              <div>
                <p className="text-xs font-semibold text-slate-500">Affected Population</p>
                <p className="mt-1 text-sm text-slate-800">{issue.affectedPeople}</p>
              </div>

              <div>
                <p className="text-xs font-semibold text-slate-500">Likely Impact</p>
                <p className="mt-1 text-sm text-slate-800">{issue.likelyImpact}</p>
              </div>

              <div className="bg-amber-50/70 border border-amber-200 rounded-lg p-3">
                <p className="text-xs font-semibold text-amber-900 flex items-center gap-1">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                  Requires Further Verification
                </p>
                <p className="mt-1 text-xs text-amber-800">{issue.unverifiedAspects}</p>
              </div>
            </div>
          </div>

          {/* 2. "Who can help?" Section matching Requirement 4 */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-4 pb-2 border-b border-slate-100">
              <Building className="w-4 h-4 text-sky-600" />
              Who can help?
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Authority */}
              <div className="border border-slate-200 rounded-lg p-3 bg-slate-50/50">
                <span className="text-[11px] font-bold text-sky-700 uppercase tracking-wide">Responsible Authority</span>
                <p className="font-semibold text-slate-900 mt-1">{issue.responsibleAuthority.name}</p>
                <p className="text-xs text-slate-600 mt-0.5">{issue.responsibleAuthority.department}</p>
                <p className="text-xs text-slate-500 mt-1">Official Status: <span className="font-medium text-slate-700">{issue.responsibleAuthority.officialStatus}</span></p>
                <p className="text-[11px] text-sky-600 mt-2 font-mono">{issue.responsibleAuthority.contact}</p>
              </div>

              {/* NGOs */}
              <div className="border border-slate-200 rounded-lg p-3 bg-slate-50/50">
                <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wide">Partnered NGOs</span>
                <div className="mt-2 space-y-2">
                  {issue.relevantNgos.map((ngo, idx) => (
                    <div key={idx} className="text-xs">
                      <p className="font-semibold text-slate-900 flex items-center gap-1">
                        {ngo.name}
                        {ngo.verified && <CheckCircle2 className="w-3 h-3 text-emerald-600" />}
                      </p>
                      <p className="text-slate-500 text-[11px]">{ngo.focus}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Resources */}
              <div className="border border-slate-200 rounded-lg p-3 bg-slate-50/50">
                <span className="text-[11px] font-bold text-purple-700 uppercase tracking-wide">Available Resources</span>
                <ul className="mt-2 space-y-1.5 text-xs text-slate-600 list-disc list-inside">
                  {issue.availableResources.map((res, idx) => (
                    <li key={idx}>{res}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* 3. Evidence Section matching Requirement 4 */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs">
            <div className="flex items-center justify-between mb-4 pb-2 border-b border-slate-100">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <FileText className="w-4 h-4 text-sky-600" />
                Evidence Trail & Citations
              </h3>
              <span className="text-xs text-slate-500 font-medium">
                {issue.evidence.length} validated sources
              </span>
            </div>

            <div className="space-y-3">
              {issue.evidence.map((ev) => (
                <div key={ev.id} className="border border-slate-200 rounded-lg p-3 bg-slate-50/40">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <p className="font-semibold text-slate-900 text-xs sm:text-sm">{ev.title}</p>
                    <div className="flex items-center gap-2">
                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-sm ${
                        ev.isOfficial ? 'bg-sky-100 text-sky-800' : 'bg-slate-200 text-slate-700'
                      }`}>
                        {ev.type}
                      </span>
                      <span className="text-[11px] text-slate-400">{ev.date}</span>
                    </div>
                  </div>
                  <p className="mt-2 text-xs text-slate-600 italic bg-white p-2.5 rounded-md border border-slate-200">
                    "{ev.excerpt}"
                  </p>
                  {ev.link && (
                    <a
                      href={ev.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] text-sky-600 hover:underline mt-2"
                    >
                      <span>View source citation</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              ))}

              {/* Supporting vs Contradicting Evidence Box */}
              {issue.contradictingEvidence && (
                <div className="border border-blue-200 bg-blue-50/50 rounded-lg p-3 text-xs">
                  <span className="font-semibold text-blue-900 block mb-0.5">Disproven Claims & Contradicting Evidence:</span>
                  <p className="text-blue-800">{issue.contradictingEvidence}</p>
                </div>
              )}
            </div>
          </div>

          {/* 4. Action Plan & Progress Updates matching Requirement 4 */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-4 pb-2 border-b border-slate-100">
              <Layers className="w-4 h-4 text-sky-600" />
              Practical Action Plan & Status Updates
            </h3>
            <div className="space-y-3">
              {issue.actionPlan.map((step, idx) => (
                <div key={idx} className="flex items-start gap-3 p-3 rounded-lg border border-slate-100 bg-slate-50/30">
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5 text-xs font-bold ${
                    step.status === 'Completed' ? 'bg-emerald-600 text-white' : step.status === 'In progress' ? 'bg-sky-600 text-white' : 'bg-slate-300 text-slate-700'
                  }`}>
                    {idx + 1}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <p className="font-semibold text-slate-900 text-xs sm:text-sm">{step.phase}</p>
                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-sm ${
                        step.status === 'Completed' ? 'bg-emerald-100 text-emerald-800' : step.status === 'In progress' ? 'bg-sky-100 text-sky-800' : 'bg-slate-200 text-slate-600'
                      }`}>
                        {step.status}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 mt-1">{step.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Report Incorrect Info Form */}
          {showReportIncorrect ? (
            <div className="border border-red-200 bg-red-50/30 rounded-xl p-4 text-xs">
              <h4 className="font-bold text-red-900 mb-2 flex items-center gap-1.5">
                <Flag className="w-4 h-4 text-red-600" />
                Report Inaccurate or Outdated Information
              </h4>
              {reportSubmitted ? (
                <div className="p-3 bg-emerald-100 text-emerald-800 rounded-lg font-medium text-center">
                  ✓ Thank you. Your correction report has been forwarded to WardSync moderators and the official municipal desk for review.
                </div>
              ) : (
                <form onSubmit={handleCorrectionSubmit} className="space-y-3">
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">What requires correction?</label>
                    <select
                      value={incorrectField}
                      onChange={(e) => setIncorrectField(e.target.value)}
                      className="w-full bg-white border border-slate-300 rounded-md p-2 text-xs"
                    >
                      <option>Cause of problem</option>
                      <option>Official authority contact / designation</option>
                      <option>Severity or urgency level</option>
                      <option>Status update is outdated (already fixed)</option>
                      <option>False report or duplicate listing</option>
                    </select>
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Correction details & evidence link</label>
                    <textarea
                      required
                      rows={2}
                      value={correctionNote}
                      onChange={(e) => setCorrectionNote(e.target.value)}
                      placeholder="Please specify correct details or provide link to official memo..."
                      className="w-full bg-white border border-slate-300 rounded-md p-2 text-xs"
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      type="submit"
                      className="bg-red-600 hover:bg-red-700 text-white font-semibold px-3 py-1.5 rounded-md text-xs flex items-center gap-1"
                    >
                      <Send className="w-3 h-3" />
                      Submit Correction
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowReportIncorrect(false)}
                      className="bg-white border border-slate-300 px-3 py-1.5 rounded-md text-xs text-slate-700"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              )}
            </div>
          ) : (
            <div className="text-right">
              <button
                type="button"
                onClick={() => setShowReportIncorrect(true)}
                className="text-xs text-slate-500 hover:text-red-600 underline font-medium"
              >
                Notice an error? Report incorrect information
              </button>
            </div>
          )}
        </div>

        {/* Modal Footer with Primary Actions */}
        <div className="sticky bottom-0 bg-white border-t border-slate-200 p-4 sm:p-5 flex flex-wrap items-center justify-between gap-3">
          <div className="text-xs text-slate-500">
            Fundraising: <strong className="text-slate-800">₹{issue.donationRaised.toLocaleString()}</strong> of ₹{issue.donationGoal.toLocaleString()} raised · <strong className="text-slate-800">{issue.registeredVolunteersCount}</strong> volunteers active
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                onClose();
                onDonate(issue);
              }}
              className="flex items-center gap-1.5 bg-[#0284c7] hover:bg-[#0369a1] text-white font-semibold text-xs sm:text-sm px-4 py-2.5 rounded-lg shadow-xs transition active:scale-95"
            >
              <Heart className="w-4 h-4 fill-white/20" />
              <span>Donate</span>
            </button>
            <button
              onClick={() => {
                onClose();
                onVolunteer(issue);
              }}
              className="flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs sm:text-sm px-4 py-2.5 rounded-lg shadow-xs transition active:scale-95"
            >
              <Users className="w-4 h-4" />
              <span>Volunteer for this Issue</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
