import React, { useState } from 'react';
import { MapPin, ChevronDown, CheckCircle, Clock } from 'lucide-react';
import { Issue, SeverityLevel } from '../types';

interface NearbyIssuesGridProps {
  issues: Issue[];
  selectedIssueId: string;
  onSelectIssue: (issue: Issue) => void;
  onKnowMore: (issue: Issue) => void;
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

export const NearbyIssuesGrid: React.FC<NearbyIssuesGridProps> = ({
  issues,
  selectedIssueId,
  onSelectIssue,
  onKnowMore
}) => {
  const [categoryFilter, setCategoryFilter] = useState<string>('All categories');
  const [severityFilter, setSeverityFilter] = useState<string>('All severities');
  const [distanceFilter, setDistanceFilter] = useState<string>('Any distance');

  const filteredIssues = issues.filter((issue) => {
    if (categoryFilter !== 'All categories' && issue.category !== categoryFilter) {
      return false;
    }
    if (severityFilter !== 'All severities' && issue.severity !== severityFilter) {
      return false;
    }
    if (distanceFilter !== 'Any distance') {
      const maxDistance = parseFloat(distanceFilter);
      if (issue.distanceKm > maxDistance) return false;
    }
    return true;
  });

  return (
    <section className="mt-14 mb-16">
      {/* Header and Filter Controls matching Screenshot 2 */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
          Other nearby issues
        </h2>

        {/* Filter dropdowns matching Screenshot 2 */}
        <div className="flex flex-wrap items-center gap-2.5 text-xs">
          {/* Category Filter */}
          <div className="relative">
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="appearance-none bg-white border border-slate-300 hover:border-slate-400 rounded-lg px-3 py-1.5 pr-7 text-xs font-medium text-slate-700 shadow-2xs cursor-pointer focus:outline-hidden focus:ring-1 focus:ring-sky-500"
            >
              <option value="All categories">All categories</option>
              <option value="Water & Sanitation">Water & Sanitation</option>
              <option value="Health">Health</option>
              <option value="Roads & Transport">Roads & Transport</option>
              <option value="Public Safety">Public Safety</option>
              <option value="Waste Management">Waste Management</option>
              <option value="Environment">Environment</option>
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2 top-2.5 pointer-events-none" />
          </div>

          {/* Severity Filter */}
          <div className="relative">
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="appearance-none bg-white border border-slate-300 hover:border-slate-400 rounded-lg px-3 py-1.5 pr-7 text-xs font-medium text-slate-700 shadow-2xs cursor-pointer focus:outline-hidden focus:ring-1 focus:ring-sky-500"
            >
              <option value="All severities">All severities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Moderate">Moderate</option>
              <option value="Low">Low</option>
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2 top-2.5 pointer-events-none" />
          </div>

          {/* Distance Filter */}
          <div className="relative">
            <select
              value={distanceFilter}
              onChange={(e) => setDistanceFilter(e.target.value)}
              className="appearance-none bg-white border border-slate-300 hover:border-slate-400 rounded-lg px-3 py-1.5 pr-7 text-xs font-medium text-slate-700 shadow-2xs cursor-pointer focus:outline-hidden focus:ring-1 focus:ring-sky-500"
            >
              <option value="Any distance">Any distance</option>
              <option value="2">Within 2 km</option>
              <option value="5">Within 5 km</option>
              <option value="10">Within 10 km</option>
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2 top-2.5 pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Grid of Issues (2 columns on lg, matching Screenshot 2) */}
      {filteredIssues.length === 0 ? (
        <div className="bg-slate-50 border border-dashed border-slate-300 rounded-xl p-10 text-center text-slate-500 text-sm">
          No civic issues match your selected filters. Try broadening the distance or category criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredIssues.map((issue) => {
            const isSelected = issue.id === selectedIssueId;

            return (
              <div
                key={issue.id}
                onClick={() => onSelectIssue(issue)}
                className={`bg-white border rounded-xl p-5 shadow-2xs transition cursor-pointer hover:shadow-xs group ${
                  isSelected
                    ? 'border-sky-500 ring-1 ring-sky-500/30'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                {/* Header row: Title + Severity badge */}
                <div className="flex items-start justify-between gap-3">
                  <h4 className="font-semibold text-slate-900 group-hover:text-sky-700 transition line-clamp-1 text-[15px]">
                    {issue.title}
                  </h4>
                  <span
                    className={`shrink-0 text-xs font-semibold px-2 py-0.5 rounded-full border ${getSeverityBadge(
                      issue.severity
                    )}`}
                  >
                    {issue.severity}
                  </span>
                </div>

                {/* Location & Distance */}
                <div className="mt-1.5 flex items-center gap-1.5 text-xs text-slate-500">
                  <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span>
                    {issue.locationName} · {issue.distanceKm} km away
                  </span>
                </div>

                {/* Tags row & Confidence */}
                <div className="mt-4 flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-100">
                  <div className="flex items-center gap-2">
                    <span className="bg-slate-100 text-slate-700 text-xs font-medium px-2 py-0.5 rounded-sm">
                      {issue.category}
                    </span>
                    <span className="bg-slate-50 text-slate-600 border border-slate-200 text-xs px-2 py-0.5 rounded-sm inline-flex items-center gap-1">
                      {issue.status === 'Verified' ? (
                        <CheckCircle className="w-3 h-3 text-sky-600" />
                      ) : (
                        <Clock className="w-3 h-3 text-slate-400" />
                      )}
                      {issue.status}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                    <div className="w-14 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-sky-600 rounded-full"
                        style={{ width: `${issue.evidenceConfidence}%` }}
                      />
                    </div>
                    <span className="text-[11px] text-slate-500">
                      {issue.evidenceConfidence}% confidence
                    </span>
                  </div>
                </div>

                {/* Quick action button */}
                <div className="mt-3 flex justify-end">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      onKnowMore(issue);
                    }}
                    className="text-xs font-medium text-sky-600 hover:text-sky-800 hover:underline inline-flex items-center gap-1"
                  >
                    <span>View full details & action plan &rarr;</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
};
