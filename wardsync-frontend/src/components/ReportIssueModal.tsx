import React, { useState } from 'react';
import { X, AlertCircle, UploadCloud, CheckCircle2 } from 'lucide-react';
import { Issue, IssueCategory, SeverityLevel } from '../types';

interface ReportIssueModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddIssue: (newIssue: Issue) => void;
}

export const ReportIssueModal: React.FC<ReportIssueModalProps> = ({
  isOpen,
  onClose,
  onAddIssue
}) => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState<IssueCategory>('Water & Sanitation');
  const [ward, setWard] = useState('Ward G/North');
  const [locality, setLocality] = useState('Dadar West');
  const [description, setDescription] = useState('');
  const [severity, setSeverity] = useState<SeverityLevel>('High');
  const [evidenceNote, setEvidenceNote] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const createdIssue: Issue = {
      id: `issue-${Date.now()}`,
      title,
      locationName: `${ward}, ${locality}, Mumbai`,
      ward,
      locality,
      distanceKm: 0.8,
      latitude: 19.0178 + (Math.random() - 0.5) * 0.04,
      longitude: 72.8478 + (Math.random() - 0.5) * 0.04,
      category,
      severity,
      urgency: severity === 'Critical' ? 'Immediate (24h)' : severity === 'High' ? 'Urgent (48-72h)' : 'Moderate (1-2 weeks)',
      status: 'Reported',
      evidenceConfidence: 58,
      dateDiscovered: 'Just now',
      description,
      cause: {
        documented: 'Citizen field observation reported via mobile intake.',
        isVerified: false
      },
      affectedPeople: 'Nearby residents and pedestrians',
      likelyImpact: 'Civic inconvenience and potential hazard if unaddressed.',
      unverifiedAspects: 'Site inspection pending by local ward officer.',
      responsibleAuthority: {
        name: 'Brihanmumbai Municipal Corporation (BMC)',
        department: 'Borough Civic Response Cell',
        contact: 'civic.response@mcgm.gov.in',
        officialStatus: 'Queued for priority site verification.'
      },
      relevantNgos: [
        { name: 'Ward Action Alliance', verified: true, focus: 'Rapid Neighborhood Response' }
      ],
      availableResources: [
        'Local volunteer monitoring team on standby'
      ],
      evidence: [
        {
          id: `ev-${Date.now()}`,
          title: 'Citizen Direct Submission with Photo Timestamp',
          type: 'Citizen Report',
          date: 'Today',
          excerpt: evidenceNote || description,
          isOfficial: false,
          credibilityScore: 70
        }
      ],
      mergedReportsCount: 1,
      actionPlan: [
        { phase: 'Phase 1: Verification & Hazard Signage', description: 'Municipal field officer site inspection.', status: 'Pending' }
      ],
      donationGoal: 15000,
      donationRaised: 0,
      donationBeneficiary: 'Ward Action Alliance Relief Fund',
      volunteerSlots: [
        { id: `vs-${Date.now()}`, dateTime: 'Upcoming Weekend · 9:00 AM', voteCount: 1, isConfirmed: false }
      ],
      volunteerMeetingPoint: `${locality} Community Junction`,
      volunteerActivity: 'Initial perimeter inspection and reporting.',
      volunteerResourcesRequired: 'Mobile phone with camera.',
      registeredVolunteersCount: 1
    };

    onAddIssue(createdIssue);
    setIsSuccess(true);
    setTimeout(() => {
      setIsSuccess(false);
      onClose();
      // Reset
      setTitle('');
      setDescription('');
    }, 1800);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-200 relative max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {isSuccess ? (
          <div className="text-center py-8">
            <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Civic Report Dispatched</h3>
            <p className="text-xs text-slate-600 mt-1 max-w-sm mx-auto">
              Your submission has been pinned to the local map and broadcasted to neighborhood NGOs and municipal monitors.
            </p>
          </div>
        ) : (
          <>
            <div className="mb-4">
              <h3 className="text-xl font-bold text-slate-900">Report a Civic Problem</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Help WardSync aggregate local issues with evidence-first reporting.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Issue Headline / Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Broken water mains leaking near market gate"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Category</label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value as IssueCategory)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs bg-white"
                  >
                    <option value="Water & Sanitation">Water & Sanitation</option>
                    <option value="Health">Health</option>
                    <option value="Roads & Transport">Roads & Transport</option>
                    <option value="Public Safety">Public Safety</option>
                    <option value="Waste Management">Waste Management</option>
                    <option value="Environment">Environment</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Severity Estimate</label>
                  <select
                    value={severity}
                    onChange={(e) => setSeverity(e.target.value as SeverityLevel)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs bg-white"
                  >
                    <option value="Critical">Critical (Immediate danger)</option>
                    <option value="High">High (Impacting community)</option>
                    <option value="Moderate">Moderate (Civic inconvenience)</option>
                    <option value="Low">Low (Minor upkeep)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Ward Identifier</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Ward G/North or Ward 1"
                    value={ward}
                    onChange={(e) => setWard(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Locality Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Dadar West or Naupada"
                    value={locality}
                    onChange={(e) => setLocality(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                  />
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Problem Description</label>
                <textarea
                  required
                  rows={3}
                  placeholder="Describe what you observed, how long it has been occurring, and how many households are affected..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Evidence / Photo Note</label>
                <div className="border-2 border-dashed border-slate-300 rounded-lg p-3 text-center text-slate-500 hover:border-slate-400 cursor-pointer">
                  <UploadCloud className="w-5 h-5 mx-auto text-slate-400 mb-1" />
                  <span className="text-[11px]">Click or drag photo evidence of the issue (Simulated upload)</span>
                </div>
              </div>

              <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-[11px] text-slate-500 flex items-start gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
                <span>
                  All citizen reports are initially flagged as <em>Reported</em> and undergo automated duplicate clustering to avoid clutter.
                </span>
              </div>

              <button
                type="submit"
                className="w-full py-2.5 bg-[#0284c7] hover:bg-[#0369a1] text-white font-semibold text-sm rounded-lg transition active:scale-95 shadow-xs"
              >
                Submit Civic Issue Report
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
};
