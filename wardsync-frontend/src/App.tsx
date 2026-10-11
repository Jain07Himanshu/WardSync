import { useState, useEffect } from 'react';
import { SAMPLE_ISSUES } from './data/sampleIssues';
import { Issue, UserAccount, DonationRecord, VolunteerRegistration, NgoEvent, NgoFundraisingCampaign } from './types';
import { civicApi } from './services/api';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { IssueMap } from './components/IssueMap';
import { FeaturedIssueCard } from './components/FeaturedIssueCard';
import { NearbyIssuesGrid } from './components/NearbyIssuesGrid';
import { Footer } from './components/Footer';
import { AuthModal } from './components/AuthModal';
import { IssueDetailsModal } from './components/IssueDetailsModal';
import { DonateModal } from './components/DonateModal';
import { VolunteerModal } from './components/VolunteerModal';
import { Dashboards } from './components/Dashboards';
import { ReportIssueModal } from './components/ReportIssueModal';
import { InfoPages } from './components/InfoPages';
import { NgoCreateEventModal } from './components/NgoCreateEventModal';
import { NgoRaiseFundsModal } from './components/NgoRaiseFundsModal';
import { MapPin } from 'lucide-react';

export function App() {
  // State for Issues
  const [issues, setIssues] = useState<Issue[]>(SAMPLE_ISSUES);
  const [selectedIssue, setSelectedIssue] = useState<Issue>(SAMPLE_ISSUES[0]);
  const [selectedLocation, setSelectedLocation] = useState<string>('Dadar West, Ward G/North (Mumbai)');
  const [isLocating, setIsLocating] = useState<boolean>(false);

  // Sync with live backend engine on load
  useEffect(() => {
    let isMounted = true;
    civicApi.fetchIssues().then((fetched) => {
      if (isMounted && fetched && fetched.length > 0) {
        setIssues(fetched);
        setSelectedIssue(fetched[0]);
      }
    });
    return () => { isMounted = false; };
  }, []);

  // User Authentication State
  const [currentUser, setCurrentUser] = useState<UserAccount | null>({
    id: 'cit-1',
    name: 'Aarav Patil',
    email: 'aarav.patil@mumbai.citizen.in',
    role: 'citizen',
    isVerified: true,
    phone: '+91 98201 44521',
    locality: 'Dadar West, Ward G/North (Mumbai)'
  });

  // Navigation View State
  const [activeView, setActiveView] = useState<'home' | 'explore' | 'volunteer' | 'about' | 'dashboards' | 'privacy' | 'terms' | 'contact'>('home');

  // Modals State
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [authInitialRole, setAuthInitialRole] = useState<'citizen' | 'ngo' | 'government'>('citizen');
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [isDonateOpen, setIsDonateOpen] = useState(false);
  const [isVolunteerOpen, setIsVolunteerOpen] = useState(false);
  const [isReportOpen, setIsReportOpen] = useState(false);

  // NGO Specific Modals State
  const [isNgoCreateEventOpen, setIsNgoCreateEventOpen] = useState(false);
  const [isNgoRaiseFundsOpen, setIsNgoRaiseFundsOpen] = useState(false);

  // NGO Events State
  const [ngoEvents, setNgoEvents] = useState<NgoEvent[]>([
    {
      id: 'ngo-ev-1',
      issueId: 'rep-mum-2026-001',
      issueTitle: 'Sewage Overflow & Contaminated Water at Dadar',
      title: 'Emergency Water Testing & Halogen Tablets Distribution Drive',
      dateTime: 'Saturday, Oct 17, 2026 · 10:00 AM - 1:00 PM',
      meetingPoint: 'Ranade Road Junction, Near Dadar Railway Station (West)',
      maxVolunteers: 35,
      enrolledCount: 19,
      activityDescription: 'Door-to-door water quality testing, distribution of water purification halogen tablets, and mapping damaged pipeline connections.',
      resourcesRequired: 'Rubber boots and gloves provided on site. Volunteers to carry valid ID badge.',
      leadCoordinator: 'Sneha Kulkarni (Field Director)',
      contactPhone: '+91 98203 11982',
      status: 'Upcoming'
    },
    {
      id: 'ngo-ev-2',
      issueId: 'rep-tha-2026-003',
      issueTitle: 'Stormwater Drain Clogging & Waterlogging at Majiwada',
      title: 'Majiwada Culvert Desilting & Plastic Interceptor Drive',
      dateTime: 'Sunday, Oct 18, 2026 · 8:30 AM - 11:30 AM',
      meetingPoint: 'Majiwada Junction Service Road, Near Lodha IThink Techno Campus',
      maxVolunteers: 25,
      enrolledCount: 14,
      activityDescription: 'Clearing plastic packaging debris from stormwater box drain grates and placing high-visibility hazard caution barriers.',
      resourcesRequired: 'Heavy-duty gloves and masks provided by Thane Citizen Action Council.',
      leadCoordinator: 'Prasad Joshi',
      contactPhone: '+91 98211 44521',
      status: 'Upcoming'
    }
  ]);

  // NGO Fundraising Campaigns State
  const [ngoCampaigns, setNgoCampaigns] = useState<NgoFundraisingCampaign[]>([
    {
      id: 'ngo-camp-1',
      issueId: 'rep-mum-2026-001',
      issueTitle: 'Sewage Overflow & Contaminated Water at Dadar',
      targetAmount: 45000,
      raisedAmount: 24500,
      purpose: 'Emergency water filtration kits and mobile water bowsers for 800+ low-income families along Ranade Road.',
      beneficiaryOrg: 'Mumbai March Civic Action Collective',
      status: 'Active'
    },
    {
      id: 'ngo-camp-2',
      issueId: 'rep-tha-2026-003',
      issueTitle: 'Stormwater Drain Clogging & Waterlogging at Majiwada',
      targetAmount: 30000,
      raisedAmount: 11200,
      purpose: 'Precast concrete drain slab coverings and heavy-duty steel silt screens for Majiwada culvert.',
      beneficiaryOrg: 'Thane Citizen Action Council',
      status: 'Active'
    }
  ]);

  // Donations State
  const [donations, setDonations] = useState<DonationRecord[]>([
    {
      id: 'sim-init-1',
      issueId: 'rep-mum-2026-001',
      issueTitle: 'Sewage Overflow & Contaminated Water at Dadar',
      amount: 1500,
      donorName: 'Aarav Patil',
      isAnonymous: false,
      date: 'Oct 10, 2026',
      simulatedTxnId: 'DEMO_MUM_849201'
    }
  ]);

  // Volunteer Registrations State
  const [volunteerRegistrations, setVolunteerRegistrations] = useState<VolunteerRegistration[]>([
    {
      id: 'reg-init-1',
      issueId: 'rep-mum-2026-001',
      issueTitle: 'Sewage Overflow & Contaminated Water at Dadar',
      volunteerName: 'Aarav Patil',
      contact: '+91 98201 44521',
      skills: 'Water Quality Testing, First Aid',
      slotDateTime: 'Saturday, Oct 17, 2026 · 10:00 AM - 1:00 PM',
      participantCount: 1,
      status: 'Confirmed'
    }
  ]);

  // Handler for Selecting Issue from map or list
  const handleSelectIssue = (issue: Issue) => {
    setSelectedIssue(issue);
  };

  // Citizen Action Handlers
  const handleOpenDonate = (issue: Issue) => {
    setSelectedIssue(issue);
    setIsDonateOpen(true);
  };

  const handleOpenVolunteer = (issue: Issue) => {
    setSelectedIssue(issue);
    setIsVolunteerOpen(true);
  };

  const handleOpenKnowMore = (issue: Issue) => {
    setSelectedIssue(issue);
    setIsDetailsOpen(true);
  };

  // NGO Action Handlers (Raise Funds & Create Event)
  const handleOpenRaiseFunds = (issue: Issue) => {
    setSelectedIssue(issue);
    setIsNgoRaiseFundsOpen(true);
  };

  const handleOpenCreateEvent = (issue: Issue) => {
    setSelectedIssue(issue);
    setIsNgoCreateEventOpen(true);
  };

  // Event Created by NGO Handler: updates state so Citizens immediately see the schedule!
  const handleEventCreated = (newEvent: NgoEvent, updatedIssue: Issue) => {
    setNgoEvents((prev) => [newEvent, ...prev]);
    setIssues((prev) =>
      prev.map((iss) => (iss.id === updatedIssue.id ? updatedIssue : iss))
    );
    if (selectedIssue.id === updatedIssue.id) {
      setSelectedIssue(updatedIssue);
    }
    civicApi.publishNgoEvent(newEvent);
  };

  // Fundraising Campaign Launched by NGO Handler
  const handleCampaignLaunched = (newCampaign: NgoFundraisingCampaign, updatedIssue: Issue) => {
    setNgoCampaigns((prev) => {
      const filtered = prev.filter((c) => c.issueId !== newCampaign.issueId);
      return [newCampaign, ...filtered];
    });
    setIssues((prev) =>
      prev.map((iss) => (iss.id === updatedIssue.id ? updatedIssue : iss))
    );
    if (selectedIssue.id === updatedIssue.id) {
      setSelectedIssue(updatedIssue);
    }
    civicApi.launchCampaign(newCampaign);
  };

  // Complete Donation Handler (from Citizen)
  const handleDonationComplete = (record: DonationRecord) => {
    setDonations((prev) => [record, ...prev]);
    // Increment raised amount in issues
    setIssues((prev) =>
      prev.map((iss) =>
        iss.id === record.issueId
          ? { ...iss, donationRaised: iss.donationRaised + record.amount }
          : iss
      )
    );
    // Also update campaign progress in NGO campaigns list
    setNgoCampaigns((prev) =>
      prev.map((camp) =>
        camp.issueId === record.issueId
          ? { ...camp, raisedAmount: camp.raisedAmount + record.amount }
          : camp
      )
    );
    if (selectedIssue.id === record.issueId) {
      setSelectedIssue((prev) => ({
        ...prev,
        donationRaised: prev.donationRaised + record.amount
      }));
    }
    civicApi.recordDonation(record);
  };

  // Register Volunteer Handler (from Citizen)
  const handleRegisterVolunteer = (reg: VolunteerRegistration) => {
    setVolunteerRegistrations((prev) => [reg, ...prev]);
    // Increment registered count in issues
    setIssues((prev) =>
      prev.map((iss) =>
        iss.id === reg.issueId
          ? { ...iss, registeredVolunteersCount: iss.registeredVolunteersCount + reg.participantCount }
          : iss
      )
    );
    // Increment enrolled count in NGO events list
    setNgoEvents((prev) =>
      prev.map((ev) =>
        ev.issueId === reg.issueId
          ? { ...ev, enrolledCount: ev.enrolledCount + reg.participantCount }
          : ev
      )
    );
    if (selectedIssue.id === reg.issueId) {
      setSelectedIssue((prev) => ({
        ...prev,
        registeredVolunteersCount: prev.registeredVolunteersCount + reg.participantCount
      }));
    }
    civicApi.registerVolunteer(reg);
  };

  // Cancel Volunteer Registration
  const handleCancelRegistration = (regId: string) => {
    const target = volunteerRegistrations.find((r) => r.id === regId);
    if (target) {
      setIssues((prev) =>
        prev.map((iss) =>
          iss.id === target.issueId
            ? { ...iss, registeredVolunteersCount: Math.max(0, iss.registeredVolunteersCount - target.participantCount) }
            : iss
        )
      );
      setNgoEvents((prev) =>
        prev.map((ev) =>
          ev.issueId === target.issueId
            ? { ...ev, enrolledCount: Math.max(0, ev.enrolledCount - target.participantCount) }
            : ev
        )
      );
    }
    setVolunteerRegistrations((prev) => prev.filter((r) => r.id !== regId));
  };

  // Add newly reported issue
  const handleAddIssue = (newIssue: Issue) => {
    setIssues((prev) => [newIssue, ...prev]);
    setSelectedIssue(newIssue);
    civicApi.reportIssue(newIssue).then((serverIssue) => {
      if (serverIssue) {
        setIssues((prev) => prev.map((iss) => (iss.id === newIssue.id ? serverIssue : iss)));
        setSelectedIssue((prev) => (prev.id === newIssue.id ? serverIssue : prev));
      }
    });
  };

  // Status update from Government Dashboard
  const handleUpdateIssueStatus = (issueId: string, newStatus: Issue['status']) => {
    setIssues((prev) =>
      prev.map((iss) => (iss.id === issueId ? { ...iss, status: newStatus } : iss))
    );
    if (selectedIssue.id === issueId) {
      setSelectedIssue((prev) => ({ ...prev, status: newStatus }));
    }
    civicApi.updateIssueStatus(issueId, newStatus);
  };

  // Persona quick switch
  const handleSwitchUser = (role: 'citizen' | 'ngo' | 'government' | 'admin' | 'guest') => {
    if (role === 'guest') {
      setCurrentUser(null);
    } else if (role === 'citizen') {
      setCurrentUser({
        id: 'cit-1',
        name: 'Aarav Patil',
        email: 'aarav.patil@mumbai.citizen.in',
        role: 'citizen',
        isVerified: true,
        phone: '+91 98201 44521',
        locality: 'Dadar West, Ward G/North (Mumbai)'
      });
    } else if (role === 'ngo') {
      setCurrentUser({
        id: 'ngo-1',
        name: 'Mumbai March Civic Trust',
        email: 'contact@mumbaimarch.org',
        role: 'ngo',
        isVerified: true,
        organizationName: 'Mumbai March Civic Action Collective',
        focusAreas: 'Pothole Audits, Public Safety & Drainage Relief',
        serviceAreas: 'Mumbai & Thane Metropolitan Region'
      });
    } else if (role === 'government') {
      setCurrentUser({
        id: 'gov-1',
        name: 'Er. Rajesh Sawant',
        email: 'rajesh.sawant@mcgm.gov.in',
        role: 'government',
        isVerified: true,
        department: 'Brihanmumbai Municipal Corporation (BMC) & TMC Directorate',
        designation: 'Executive Ward Engineer',
        jurisdiction: 'Ward G/North & Ward 1 (Thane)'
      });
    } else if (role === 'admin') {
      setCurrentUser({
        id: 'adm-1',
        name: 'Platform Administrator',
        email: 'admin@wardsync.org',
        role: 'admin',
        isVerified: true
      });
    }
  };

  // Use My Location handler
  const handleUseMyLocation = () => {
    setIsLocating(true);
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        () => {
          setIsLocating(false);
          setSelectedLocation('Ward 42, Entally, Kolkata (GPS Detected)');
        },
        () => {
          setIsLocating(false);
          setSelectedLocation('Ward 42, Entally, Kolkata (Defaulting)');
        },
        { timeout: 4000 }
      );
    } else {
      setTimeout(() => {
        setIsLocating(false);
        setSelectedLocation('Ward 42, Entally, Kolkata');
      }, 500);
    }
  };

  const isNgoActive = currentUser?.role === 'ngo';

  return (
    <div className="min-h-screen flex flex-col bg-white text-slate-900 font-sans selection:bg-sky-100 selection:text-sky-900">
      {/* Persistent Navigation Header */}
      <Header
        currentUser={currentUser}
        onOpenAuth={(role) => {
          if (role) setAuthInitialRole(role);
          setIsAuthOpen(true);
        }}
        onLogout={() => setCurrentUser(null)}
        onSwitchUser={handleSwitchUser}
        activeView={activeView === 'privacy' || activeView === 'terms' || activeView === 'contact' ? 'about' : activeView}
        setActiveView={(v) => setActiveView(v)}
        onOpenReportModal={() => setIsReportOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1">
        {activeView === 'home' && (
          <div className="w-full">
            {/* Hero Section */}
            <Hero
              selectedLocation={selectedLocation}
              onSelectLocation={(loc) => setSelectedLocation(loc)}
              onUseMyLocation={handleUseMyLocation}
              isLocating={isLocating}
            />

            {/* Main Interactive Issue Map & Featured Issue Section matching Screenshot 1 */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
              {/* Section Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
                    Most Important Issue Near You
                  </h2>
                  {isNgoActive && (
                    <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded-full border border-emerald-300">
                      NGO Workspace Mode
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  <span>Demo area — Kolkata</span>
                </div>
              </div>

              {/* 2-Column Responsive Layout: Map on left, Featured Issue Card on right */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
                <div className="lg:col-span-7">
                  <IssueMap
                    issues={issues}
                    selectedIssue={selectedIssue}
                    onSelectIssue={handleSelectIssue}
                  />
                </div>

                <div className="lg:col-span-5">
                  <FeaturedIssueCard
                    issue={selectedIssue}
                    isNgoRole={isNgoActive}
                    onDonate={handleOpenDonate}
                    onVolunteer={handleOpenVolunteer}
                    onKnowMore={handleOpenKnowMore}
                    onRaiseFunds={handleOpenRaiseFunds}
                    onCreateEvent={handleOpenCreateEvent}
                  />
                </div>
              </div>

              {/* Other nearby issues grid matching Screenshot 2 */}
              <NearbyIssuesGrid
                issues={issues}
                selectedIssueId={selectedIssue.id}
                onSelectIssue={handleSelectIssue}
                onKnowMore={handleOpenKnowMore}
              />
            </div>
          </div>
        )}

        {/* Dashboards View */}
        {activeView === 'dashboards' && (
          <Dashboards
            currentUser={currentUser}
            issues={issues}
            selectedIssue={selectedIssue}
            donations={donations}
            volunteerRegistrations={volunteerRegistrations}
            ngoEvents={ngoEvents}
            ngoCampaigns={ngoCampaigns}
            onSelectIssue={handleSelectIssue}
            onUpdateIssueStatus={handleUpdateIssueStatus}
            onOpenReportModal={() => setIsReportOpen(true)}
            onRaiseFunds={handleOpenRaiseFunds}
            onCreateEvent={handleOpenCreateEvent}
            onKnowMore={handleOpenKnowMore}
          />
        )}

        {/* Info & Secondary Views */}
        {(activeView === 'about' ||
          activeView === 'privacy' ||
          activeView === 'terms' ||
          activeView === 'contact' ||
          activeView === 'explore' ||
          activeView === 'volunteer') && (
          <InfoPages
            view={activeView}
            onBackToHome={() => setActiveView('home')}
            onExploreIssueClick={() => setActiveView('home')}
            onVolunteerClick={() => {
              setActiveView('home');
              setIsVolunteerOpen(true);
            }}
          />
        )}
      </main>

      {/* Footer matching Screenshot 2 */}
      <Footer onNavClick={(v) => setActiveView(v)} />

      {/* Modals */}
      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        initialRole={authInitialRole}
        onLoginSuccess={(user) => {
          setCurrentUser(user);
          setIsAuthOpen(false);
        }}
      />

      <IssueDetailsModal
        issue={selectedIssue}
        isOpen={isDetailsOpen}
        onClose={() => setIsDetailsOpen(false)}
        onDonate={handleOpenDonate}
        onVolunteer={handleOpenVolunteer}
      />

      <DonateModal
        issue={selectedIssue}
        isOpen={isDonateOpen}
        onClose={() => setIsDonateOpen(false)}
        onDonationComplete={handleDonationComplete}
        donationHistory={donations}
      />

      <VolunteerModal
        issue={selectedIssue}
        isOpen={isVolunteerOpen}
        onClose={() => setIsVolunteerOpen(false)}
        onRegisterVolunteer={handleRegisterVolunteer}
        userRegistrations={volunteerRegistrations}
        onCancelRegistration={handleCancelRegistration}
      />

      <ReportIssueModal
        isOpen={isReportOpen}
        onClose={() => setIsReportOpen(false)}
        onAddIssue={handleAddIssue}
      />

      {/* NGO SPECIFIC ACTION MODALS */}
      <NgoCreateEventModal
        issue={selectedIssue}
        isOpen={isNgoCreateEventOpen}
        onClose={() => setIsNgoCreateEventOpen(false)}
        onEventCreated={handleEventCreated}
        ngoName={currentUser?.organizationName || 'CleanWater Bengal Relief Foundation'}
      />

      <NgoRaiseFundsModal
        issue={selectedIssue}
        isOpen={isNgoRaiseFundsOpen}
        onClose={() => setIsNgoRaiseFundsOpen(false)}
        onCampaignLaunched={handleCampaignLaunched}
        ngoName={currentUser?.organizationName || 'CleanWater Bengal Relief Foundation'}
      />
    </div>
  );
}

export default App;
