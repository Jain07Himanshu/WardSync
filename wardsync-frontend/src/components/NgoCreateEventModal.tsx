import React, { useState } from 'react';
import { X, CalendarPlus, MapPin, Users, CheckCircle2, ShieldCheck, Sparkles } from 'lucide-react';
import { Issue, NgoEvent } from '../types';

interface NgoCreateEventModalProps {
  issue: Issue | null;
  isOpen: boolean;
  onClose: () => void;
  onEventCreated: (event: NgoEvent, updatedIssue: Issue) => void;
  ngoName: string;
}

export const NgoCreateEventModal: React.FC<NgoCreateEventModalProps> = ({
  issue,
  isOpen,
  onClose,
  onEventCreated,
  ngoName
}) => {
  const [eventTitle, setEventTitle] = useState('');
  const [eventDate, setEventDate] = useState('2026-10-24');
  const [eventTime, setEventTime] = useState('10:00 AM - 1:00 PM');
  const [meetingPoint, setMeetingPoint] = useState('');
  const [maxVolunteers, setMaxVolunteers] = useState(25);
  const [activityDescription, setActivityDescription] = useState('');
  const [resourcesRequired, setResourcesRequired] = useState('');
  const [leadCoordinator, setLeadCoordinator] = useState('Ananya Das (Field Lead)');
  const [contactPhone, setContactPhone] = useState('+91 98302 11099');
  const [isSuccess, setIsSuccess] = useState(false);

  // Auto-populate reasonable defaults when an issue is selected
  React.useEffect(() => {
    if (issue) {
      setEventTitle(`Community Field Response: ${issue.title}`);
      setMeetingPoint(`${issue.locality} Community Hall / Main Ward Gate`);
      setActivityDescription(`Organized ground action to resolve ${issue.title}. Distributing supplies and assisting affected local households.`);
      setResourcesRequired('Gloves and safety badges provided by NGO. Volunteers should bring personal water bottles and wear comfortable footwear.');
    }
  }, [issue]);

  if (!isOpen || !issue) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const formattedDateTime = `${new Date(eventDate).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })} · ${eventTime}`;

    const newEvent: NgoEvent = {
      id: `ngo-ev-${Date.now()}`,
      issueId: issue.id,
      issueTitle: issue.title,
      title: eventTitle,
      dateTime: formattedDateTime,
      meetingPoint,
      maxVolunteers,
      enrolledCount: 0,
      activityDescription,
      resourcesRequired,
      leadCoordinator,
      contactPhone,
      status: 'Upcoming'
    };

    // Update the issue's volunteer coordination data so citizens see it immediately!
    const updatedIssue: Issue = {
      ...issue,
      volunteerSlots: [
        {
          id: `slot-confirmed-${Date.now()}`,
          dateTime: formattedDateTime,
          voteCount: 1,
          isConfirmed: true,
          isPopular: true
        },
        ...issue.volunteerSlots.map(s => ({ ...s, isPopular: false }))
      ],
      volunteerMeetingPoint: meetingPoint,
      volunteerActivity: activityDescription,
      volunteerResourcesRequired: resourcesRequired
    };

    onEventCreated(newEvent, updatedIssue);
    setIsSuccess(true);

    setTimeout(() => {
      setIsSuccess(false);
      onClose();
    }, 1800);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[92vh] overflow-y-auto shadow-2xl border border-slate-200 relative p-6 sm:p-7">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {isSuccess ? (
          <div className="py-10 text-center">
            <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Volunteer Event Published!</h3>
            <p className="text-xs text-slate-600 mt-1 max-w-sm mx-auto">
              This event is now live on the civic map and citizen portal. Citizens registering to volunteer will receive this schedule and meeting point.
            </p>
          </div>
        ) : (
          <>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
                <CalendarPlus className="w-5 h-5" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Create Volunteer Event</h3>
            </div>
            <p className="text-xs text-slate-500 mb-5 font-medium">
              Publish an organized volunteer schedule for: <strong className="text-slate-800">{issue.title}</strong>
            </p>

            {/* Organizer Banner */}
            <div className="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl text-xs text-emerald-900 flex items-center justify-between mb-5">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span>Host Organization: <strong>{ngoName}</strong></span>
              </div>
              <span className="bg-emerald-200 text-emerald-900 text-[10px] font-semibold px-2 py-0.5 rounded">
                Verified NGO Host
              </span>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Event Action Headline</label>
                <input
                  type="text"
                  required
                  value={eventTitle}
                  onChange={(e) => setEventTitle(e.target.value)}
                  placeholder="e.g. Rapid Water Pipeline Repair & Filter Distribution Drive"
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>

              {/* Date & Time Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Scheduled Date</label>
                  <input
                    type="date"
                    required
                    value={eventDate}
                    onChange={(e) => setEventDate(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs bg-white"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Time Slot / Hours</label>
                  <input
                    type="text"
                    required
                    value={eventTime}
                    onChange={(e) => setEventTime(e.target.value)}
                    placeholder="e.g. 10:00 AM - 1:00 PM"
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                  />
                </div>
              </div>

              {/* Location & Volunteer Count */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="sm:col-span-2">
                  <label className="block font-semibold text-slate-700 mb-1">Specific Meeting Point</label>
                  <div className="relative">
                    <input
                      type="text"
                      required
                      value={meetingPoint}
                      onChange={(e) => setMeetingPoint(e.target.value)}
                      placeholder="e.g. Dadar Flower Market Junction or Majiwada Flyover Service Road"
                      className="w-full pl-8 pr-3 py-2 border border-slate-300 rounded-lg text-xs"
                    />
                    <MapPin className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
                  </div>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Max Volunteers Needed</label>
                  <div className="relative">
                    <input
                      type="number"
                      min="1"
                      max="200"
                      required
                      value={maxVolunteers}
                      onChange={(e) => setMaxVolunteers(parseInt(e.target.value) || 1)}
                      className="w-full pl-8 pr-3 py-2 border border-slate-300 rounded-lg text-xs"
                    />
                    <Users className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
                  </div>
                </div>
              </div>

              {/* Activity Details */}
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Ground Activity Briefing</label>
                <textarea
                  required
                  rows={2}
                  value={activityDescription}
                  onChange={(e) => setActivityDescription(e.target.value)}
                  placeholder="Detail the exact tasks volunteers will perform on the ground..."
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>

              {/* Gear and Resources */}
              <div>
                <label className="block font-semibold text-slate-700 mb-1">What to Bring & What NGO Provides</label>
                <textarea
                  required
                  rows={2}
                  value={resourcesRequired}
                  onChange={(e) => setResourcesRequired(e.target.value)}
                  placeholder="e.g. NGO supplies rubber boots & gloves. Volunteers should bring water bottle and ID badge..."
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>

              {/* Lead Coordinator */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Field Coordinator Name</label>
                  <input
                    type="text"
                    required
                    value={leadCoordinator}
                    onChange={(e) => setLeadCoordinator(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Coordinator Emergency Contact</label>
                  <input
                    type="tel"
                    required
                    value={contactPhone}
                    onChange={(e) => setContactPhone(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                  />
                </div>
              </div>

              <div className="p-3 bg-sky-50 border border-sky-200 rounded-xl text-sky-900 text-[11px] flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-sky-600 shrink-0" />
                <span>
                  Publishing this event sets it as the <strong>primary confirmed schedule</strong> for this problem. When citizens click <em>Volunteer</em>, they will see this schedule and be able to RSVP directly.
                </span>
              </div>

              <button
                type="submit"
                className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm rounded-lg shadow-xs transition active:scale-95"
              >
                Publish Volunteer Event to WardSync
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
};
