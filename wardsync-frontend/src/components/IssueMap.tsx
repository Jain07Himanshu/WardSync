import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { Issue, SeverityLevel } from '../types';

interface IssueMapProps {
  issues: Issue[];
  selectedIssue: Issue;
  onSelectIssue: (issue: Issue) => void;
}

const getMarkerColor = (severity: SeverityLevel) => {
  switch (severity) {
    case 'Critical': return '#dc2626'; // Red
    case 'High': return '#ea580c';     // Orange
    case 'Moderate': return '#ca8a04'; // Yellow
    case 'Low': return '#16a34a';      // Green
    default: return '#0284c7';
  }
};

export const IssueMap: React.FC<IssueMapProps> = ({
  issues,
  selectedIssue,
  onSelectIssue
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markersRef = useRef<{ [id: string]: L.Marker }>({});

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      // Initialize map centered on Mumbai & Thane
      const map = L.map(mapContainerRef.current, {
        center: [selectedIssue.latitude, selectedIssue.longitude],
        zoom: 12,
        zoomControl: true,
        attributionControl: true
      });

      // Add CartoDB Positron or OpenStreetMap tiles matching the screenshot's clean look
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
      }).addTo(map);

      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;

    // Clear previous markers
    Object.values(markersRef.current).forEach((m) => m.remove());
    markersRef.current = {};

    // Add markers for all issues
    issues.forEach((issue) => {
      const isSelected = issue.id === selectedIssue.id;
      const color = getMarkerColor(issue.severity);
      const size = isSelected ? 30 : 20;

      // Custom HTML Marker matching screenshot
      const iconHtml = `
        <div style="
          width: ${size}px;
          height: ${size}px;
          background-color: ${color};
          border: ${isSelected ? '3px solid #ffffff' : '2px solid #ffffff'};
          box-shadow: 0 2px 8px rgba(0,0,0,0.35);
          border-radius: 50%;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transform: translate(-50%, -50%);
          transition: transform 0.2s ease, width 0.2s ease;
        ">
          ${isSelected ? '<div style="width: 8px; height: 8px; background: white; border-radius: 50%;"></div>' : ''}
        </div>
      `;

      const customIcon = L.divIcon({
        className: 'custom-civic-marker',
        html: iconHtml,
        iconSize: [size, size],
        iconAnchor: [size / 2, size / 2]
      });

      const marker = L.marker([issue.latitude, issue.longitude], { icon: customIcon })
        .addTo(map)
        .on('click', () => {
          onSelectIssue(issue);
        });

      // Tooltip
      marker.bindTooltip(`<strong>${issue.title}</strong><br/><span style="color:${color}">${issue.severity} Priority</span>`, {
        direction: 'top',
        offset: [0, -10]
      });

      markersRef.current[issue.id] = marker;
    });

    // Pan smoothly to selected issue
    map.panTo([selectedIssue.latitude, selectedIssue.longitude], { animate: true, duration: 0.8 });

    return () => {
      // Cleanup on unmount if needed
    };
  }, [issues, selectedIssue, onSelectIssue]);

  return (
    <div className="flex flex-col h-full">
      {/* Map Canvas */}
      <div className="relative w-full h-[400px] lg:h-[420px] rounded-xl overflow-hidden border border-slate-200 shadow-xs bg-slate-100">
        <div ref={mapContainerRef} className="w-full h-full" />
      </div>

      {/* Map Legend matching Screenshot 1 bottom */}
      <div className="mt-3 flex items-center justify-start gap-4 text-xs text-slate-600 px-1">
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-red-600 inline-block"></span>
          <span>Critical</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-orange-500 inline-block"></span>
          <span>High</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span>
          <span>Moderate</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-600 inline-block"></span>
          <span>Low</span>
        </div>
      </div>
    </div>
  );
};
