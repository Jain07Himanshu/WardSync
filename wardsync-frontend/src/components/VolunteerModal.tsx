import React, { useState } from 'react';
import { 
  X, Users, Calendar, MapPin, CheckCircle2, Clock, 
  Sparkles, ShieldCheck, AlertCircle, PlusCircle, UserCheck
} from 'lucide-react';
import { Issue, VolunteerRegistration } from '../types';

interface VolunteerModalProps {
  issue: Issue | null;
  isOpen: boolean;
  onClose: () => void;
  onRegisterVolunteer: (reg: VolunteerRegistration) => void;
  userRegistrations: VolunteerRegistration[];
  onCancelRegistration: (id: string) => void;
}

export const VolunteerModal: React.FC<VolunteerModalProps> = ({
  issue,
  isOpen,
  onClose,
  onRegisterVolunteer,
  userRegistrations,
  onCancelRegistration
}) => {
  const [volunteerName, setVolunteerName] = useState('Priya Sen');
  const [contact, setContact] = useState('+91 98301 22415');
  const [skills, setSkills] = useState('Relief Kit Distribution, First Aid');
  const [participantCount, setParticipantCount] = useState(1);
  const [selectedSlotId, setSelectedSlotId] = useState<string>('');
  const [customSlot, setCustomSlot] = useState('');
  const [isSuggestingNew, setIsSuggestingNew] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  if (!isOpen || !issue) return null;

  // Find if already registered
  const existingRegistration = userRegistrations.find((r) => r.issueId === issue.id);

  // Set default slot if not set
  const popularSlot = issue.volunteerSlots.find((s) => s.isPopular) || issue.volunteerSlots[0];
  const activeSlotId = selectedSlotId || popularSlot?.id;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    let slotText = '';
    if (isSuggestingNew && customSlot) {
      slotText = `Proposed: ${customSlot}`;
    } else {
      const chosen = issue.volunteerSlots.find((s) => s.id === activeSlotId);
      slotText = chosen ? chosen.dateTime : 'Saturday Morning Slot';
    }

    const reg: VolunteerRegistration = {
      id: `reg-${Date.now()}`,
      issueId: issue.id,
      issueTitle: issue.title,
      volunteerName,
      contact,
      skills,
      slotDateTime: slotText,
      participantCount,
      status: 'Confirmed'
    };

    onRegisterVolunteer(reg);
    setIsSubmitted(true);
    setTimeout(() => {
      setIsSubmitted(false);
      onClose();
    }, 2000);
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

        {/* Modal Header */}
        <div className="flex items-center gap-2 mb-1">
          <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
            <Users className="w-5 h-5" />
          </div>
          <h3 className="text-xl font-bold text-slate-900">Volunteer Coordination</h3>
        </div>
        <p className="text-xs text-slate-500 mb-5 font-medium">{issue.title} — {issue.locationName}</p>

        {isSubmitted ? (
          <div className="py-10 text-center">
            <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h4 className="text-lg font-bold text-slate-900">Registration Confirmed!</h4>
            <p className="text-sm text-slate-600 mt-1 max-w-sm mx-auto">
              You are signed up to assist in resolving <strong>{issue.title}</strong>. Instructions and meeting details have been added to your citizen dashboard.
            </p>
          </div>
        ) : existingRegistration ? (
          /* CURRENT REGISTRATION STATUS & CANCEL OPTION */
          <div className="space-y-4">
            <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-900">
              <div className="flex items-center gap-2 font-bold text-sm mb-1">
                <UserCheck className="w-4 h-4 text-emerald-600" />
                You are registered for this civic event!
              </div>
              <p className="text-xs text-emerald-800">
                Time Slot: <strong>{existingRegistration.slotDateTime}</strong>
              </p>
              <p className="text-xs text-emerald-800 mt-0.5">
                Participants: <strong>{existingRegistration.participantCount} person(s)</strong>
              </p>
            </div>

            {/* Event Briefing Details matching Requirement 6 */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs space-y-3">
              <h4 className="font-bold text-slate-900 text-sm">Event Action Briefing</h4>
              <div>
                <span className="font-semibold text-slate-600 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" /> Meeting Point:
                </span>
                <p className="mt-0.5 text-slate-800">{issue.volunteerMeetingPoint}</p>
              </div>
              <div>
                <span className="font-semibold text-slate-600">Activity on Ground:</span>
                <p className="mt-0.5 text-slate-800">{issue.volunteerActivity}</p>
              </div>
              <div>
                <span className="font-semibold text-slate-600">Resources Required to Carry:</span>
                <p className="mt-0.5 text-slate-800">{issue.volunteerResourcesRequired}</p>
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => onCancelRegistration(existingRegistration.id)}
                className="w-full py-2.5 bg-red-50 hover:bg-red-100 text-red-700 border border-red-200 text-xs font-semibold rounded-lg transition"
              >
                Cancel My Participation RSVP
              </button>
              <button
                type="button"
                onClick={onClose}
                className="w-full py-2.5 bg-slate-900 text-white text-xs font-semibold rounded-lg transition"
              >
                Done
              </button>
            </div>
          </div>
        ) : (
          /* REGISTRATION FORM */
          <form onSubmit={handleSubmit} className="space-y-5 text-xs">
            {/* Event Details Card */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-2">
              <div className="flex items-start gap-2">
                <MapPin className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-slate-700">Meeting Point:</span>{' '}
                  <span className="text-slate-600">{issue.volunteerMeetingPoint}</span>
                </div>
              </div>
              <div className="flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-slate-700">Lead Field Coordinator:</span>{' '}
                  <span className="text-slate-600">
                    {issue.relevantNgos[0]?.name || 'WardSync Civic Action Alliance'} (Verified)
                  </span>
                </div>
              </div>
            </div>

            {/* Date & Time Slot Polling matching Requirement 6 */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="font-bold text-slate-800 text-xs flex items-center gap-1.5">
                  <Calendar className="w-4 h-4 text-sky-600" />
                  Select Date & Time Slot (Group Consensus Polling)
                </label>
                <span className="text-[11px] text-slate-500">
                  {issue.registeredVolunteersCount} volunteers signed up so far
                </span>
              </div>

              <div className="space-y-2">
                {issue.volunteerSlots.map((slot) => {
                  const isSelected = activeSlotId === slot.id && !isSuggestingNew;

                  return (
                    <div
                      key={slot.id}
                      onClick={() => {
                        setSelectedSlotId(slot.id);
                        setIsSuggestingNew(false);
                      }}
                      className={`p-3 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                        isSelected
                          ? 'border-emerald-500 bg-emerald-50/40 ring-1 ring-emerald-500/30'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${
                          isSelected ? 'border-emerald-600 bg-emerald-600' : 'border-slate-300'
                        }`}>
                          {isSelected && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                        </div>
                        <div>
                          <p className="font-semibold text-slate-900 text-xs sm:text-sm">{slot.dateTime}</p>
                          <div className="flex items-center gap-2 mt-0.5">
                            <span className="text-slate-500 text-[11px]">
                              {slot.voteCount} people interested
                            </span>
                            {slot.isConfirmed ? (
                              <span className="text-emerald-700 bg-emerald-100 text-[10px] font-semibold px-1.5 py-0.2 rounded">
                                Confirmed by Organizer
                              </span>
                            ) : (
                              <span className="text-amber-700 bg-amber-100 text-[10px] font-semibold px-1.5 py-0.2 rounded">
                                Pending confirmation
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      {slot.isPopular && (
                        <span className="bg-sky-100 text-sky-800 font-bold text-[10px] px-2 py-0.5 rounded-full flex items-center gap-1">
                          <Sparkles className="w-3 h-3 text-sky-600" />
                          Recommended
                        </span>
                      )}
                    </div>
                  );
                })}

                {/* Suggest new date/time option */}
                <div
                  onClick={() => setIsSuggestingNew(true)}
                  className={`p-3 rounded-xl border cursor-pointer transition ${
                    isSuggestingNew
                      ? 'border-sky-500 bg-sky-50/40 ring-1 ring-sky-500/30'
                      : 'border-dashed border-slate-300 hover:border-slate-400 bg-white'
                  }`}
                >
                  <div className="flex items-center gap-2 text-slate-700 font-semibold mb-1">
                    <PlusCircle className="w-4 h-4 text-sky-600" />
                    <span>Suggest an alternate date or time</span>
                  </div>
                  {isSuggestingNew && (
                    <input
                      type="text"
                      placeholder="e.g. Next Tuesday at 4:30 PM"
                      value={customSlot}
                      onChange={(e) => setCustomSlot(e.target.value)}
                      className="w-full mt-2 px-3 py-1.5 border border-slate-300 rounded-lg text-xs"
                    />
                  )}
                </div>
              </div>
            </div>

            {/* Volunteer Personal Details */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Your Full Name</label>
                <input
                  type="text"
                  required
                  value={volunteerName}
                  onChange={(e) => setVolunteerName(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Contact Phone / WhatsApp</label>
                <input
                  type="tel"
                  required
                  value={contact}
                  onChange={(e) => setContact(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Relevant Skills or Background</label>
                <input
                  type="text"
                  placeholder="e.g. Plumbing, Field Survey, Student, First Aid"
                  value={skills}
                  onChange={(e) => setSkills(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Number of Participants Coming</label>
                <select
                  value={participantCount}
                  onChange={(e) => setParticipantCount(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs bg-white"
                >
                  <option value={1}>1 (Just me)</option>
                  <option value={2}>2 people</option>
                  <option value={3}>3 people</option>
                  <option value={4}>4 people</option>
                  <option value={5}>5+ (Group/Team)</option>
                </select>
              </div>
            </div>

            {/* Submit RSVP */}
            <button
              type="submit"
              className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm rounded-lg shadow-xs transition active:scale-95"
            >
              Confirm Volunteer RSVP for this Event
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
