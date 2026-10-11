import React from 'react';
import { MapPin, Info, Heart, Users, CheckCircle, Clock, CalendarPlus, CircleDollarSign, ShieldCheck } from 'lucide-react';
import { Issue, SeverityLevel } from '../types';

interface FeaturedIssueCardProps {
  issue: Issue;
  isNgoRole?: boolean;
  onDonate: (issue: Issue) => void;
  onVolunteer: (issue: Issue) => void;
  onKnowMore: (issue: Issue) => void;
  onRaiseFunds?: (issue: Issue) => void;
  onCreateEvent?: (issue: Issue) => void;
}

const getSeverityBadge = (severity: SeverityLevel) => {
  switch (severity) {
    case 'Critical':
      return 'bg-red-50 text-red-600 border-red-200';
    case 'High':
      return 'bg-orange-50 text-orange-600 border-orange-200';
    case 'Moderate':
      return 'bg-amber-50 text-amber-700 border-amber-200';
    case 'Low':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200';
  }
};

export const FeaturedIssueCard: React.FC<FeaturedIssueCardProps> = ({
  issue,
  isNgoRole = false,
  onDonate,
  onVolunteer,
  onKnowMore,
  onRaiseFunds,
  onCreateEvent
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col justify-between h-full">
      {/* Top Title & Severity Badge matching Screenshot 1 */}
      <div>
        <div className="flex items-start justify-between gap-4">
          <h3 className="text-xl font-bold text-slate-900 tracking-tight leading-snug">
            {issue.title}
          </h3>
          <span
            className={`shrink-0 text-xs font-semibold px-2.5 py-0.5 rounded-full border ${getSeverityBadge(
              issue.severity
            )}`}
          >
            {issue.severity}
          </span>
        </div>

        {/* Location & Distance */}
        <div className="mt-2 flex items-center gap-1.5 text-xs text-slate-500 font-medium">
          <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <span>
            {issue.locality} · {issue.distanceKm} km away
          </span>
        </div>

        {/* Issue Description */}
        <p className="mt-3.5 text-sm text-slate-600 leading-relaxed">
          {issue.description}
        </p>

        {/* Tags, Status & Evidence Confidence Bar matching Screenshot 1 */}
        <div className="mt-5 flex flex-wrap items-center gap-2.5">
          <span className="bg-slate-100 text-slate-700 text-xs font-medium px-2.5 py-1 rounded-md">
            {issue.category}
          </span>

          <span className="bg-sky-50 text-sky-700 border border-sky-200 text-xs font-medium px-2.5 py-1 rounded-md inline-flex items-center gap-1">
            {issue.status === 'Verified' ? (
              <CheckCircle className="w-3 h-3 text-sky-600" />
            ) : (
              <Clock className="w-3 h-3 text-slate-400" />
            )}
            {issue.status}
          </span>

          {/* Confidence Indicator with horizontal bar */}
          <div className="flex items-center gap-2 ml-auto text-xs text-slate-600 font-medium">
            <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-sky-600 rounded-full"
                style={{ width: `${issue.evidenceConfidence}%` }}
              />
            </div>
            <span className="text-[11px] text-slate-500 font-medium">
              {issue.evidenceConfidence}% confidence
            </span>
          </div>
        </div>

        {/* NGO Badge or Ranking note */}
        {isNgoRole ? (
          <div className="mt-4 p-2.5 bg-emerald-50/70 border border-emerald-200 rounded-lg flex items-center gap-2 text-xs text-emerald-800">
            <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>
              <strong>NGO Coordinator Mode:</strong> You can launch fundraising goals and schedule volunteer events for this problem.
            </span>
          </div>
        ) : (
          <p className="mt-4 text-[11px] text-slate-400 leading-relaxed italic">
            Ranked by severity, distance, recency and evidence confidence — not distance alone.
          </p>
        )}
      </div>

      {/* 3 Main Action Buttons */}
      <div className="mt-6 pt-4 border-t border-slate-100 grid grid-cols-3 gap-2.5">
        {isNgoRole ? (
          /* NGO ACTIONS: Raise Funds, Create Event, Know More */
          <>
            <button
              onClick={() => onRaiseFunds && onRaiseFunds(issue)}
              className="flex items-center justify-center gap-1.5 bg-[#0284c7] hover:bg-[#0369a1] text-white text-xs sm:text-sm font-semibold py-2.5 px-3 rounded-lg shadow-2xs transition active:scale-95"
            >
              <CircleDollarSign className="w-4 h-4 fill-white/20" />
              <span>Raise Funds</span>
            </button>

            <button
              onClick={() => onCreateEvent && onCreateEvent(issue)}
              className="flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs sm:text-sm font-semibold py-2.5 px-3 rounded-lg shadow-2xs transition active:scale-95"
            >
              <CalendarPlus className="w-4 h-4" />
              <span>Create Event</span>
            </button>

            <button
              onClick={() => onKnowMore(issue)}
              className="flex items-center justify-center gap-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs sm:text-sm font-semibold py-2.5 px-3 rounded-lg transition active:scale-95"
            >
              <Info className="w-4 h-4 text-slate-500" />
              <span>Know More</span>
            </button>
          </>
        ) : (
          /* CITIZEN ACTIONS: Donate, Volunteer, Know More */
          <>
            <button
              onClick={() => onDonate(issue)}
              className="flex items-center justify-center gap-1.5 bg-[#0284c7] hover:bg-[#0369a1] text-white text-xs sm:text-sm font-semibold py-2.5 px-3 rounded-lg shadow-2xs transition active:scale-95"
            >
              <Heart className="w-4 h-4 fill-white/20" />
              <span>Donate</span>
            </button>

            <button
              onClick={() => onVolunteer(issue)}
              className="flex items-center justify-center gap-1.5 bg-white border border-emerald-400/80 hover:bg-emerald-50/60 text-emerald-700 text-xs sm:text-sm font-semibold py-2.5 px-3 rounded-lg transition active:scale-95"
            >
              <Users className="w-4 h-4 text-emerald-600" />
              <span>Volunteer</span>
            </button>

            <button
              onClick={() => onKnowMore(issue)}
              className="flex items-center justify-center gap-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs sm:text-sm font-semibold py-2.5 px-3 rounded-lg transition active:scale-95"
            >
              <Info className="w-4 h-4 text-slate-500" />
              <span>Know More</span>
            </button>
          </>
        )}
      </div>
    </div>
  );
};
