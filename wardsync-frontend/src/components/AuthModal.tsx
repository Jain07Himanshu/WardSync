import React, { useState } from 'react';
import { X, User, Building2, Landmark, CheckCircle, AlertTriangle, ShieldCheck } from 'lucide-react';
import { UserAccount, UserRole } from '../types';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoginSuccess: (user: UserAccount) => void;
  initialRole?: 'citizen' | 'ngo' | 'government';
}

export const AuthModal: React.FC<AuthModalProps> = ({
  isOpen,
  onClose,
  onLoginSuccess,
  initialRole = 'citizen'
}) => {
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login');
  const [selectedRole, setSelectedRole] = useState<'citizen' | 'ngo' | 'government'>(initialRole);

  // Form states
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [locality, setLocality] = useState('Dadar West, Ward G/North');

  // NGO specific
  const [orgName, setOrgName] = useState('');
  const [contactPerson, setContactPerson] = useState('');
  const [focusAreas, setFocusAreas] = useState('Clean Water, Sanitation & Road Safety');
  const [serviceAreas, setServiceAreas] = useState('Mumbai & Thane Metropolitan Region');
  const [docUploaded, setDocUploaded] = useState(false);

  // Government specific
  const [department, setDepartment] = useState('Hydraulic & Roads Department');
  const [designation, setDesignation] = useState('Executive Ward Engineer');
  const [jurisdiction, setJurisdiction] = useState('Ward G/North & Ward 1 (Thane)');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (activeTab === 'login') {
      // Simulate login
      const mockUser: UserAccount = {
        id: `user-${Date.now()}`,
        name: selectedRole === 'citizen' ? (name || 'Priya Sen') : selectedRole === 'ngo' ? (orgName || 'CleanWater Bengal') : (name || 'Engr. Subhash Roy'),
        email: email || `${selectedRole}@wardsync.org`,
        role: selectedRole,
        isVerified: selectedRole === 'citizen' ? true : false, // NGO and Gov require approval
        locality,
        organizationName: orgName,
        department,
        designation,
        jurisdiction
      };
      onLoginSuccess(mockUser);
      onClose();
    } else {
      // Registration
      const newUser: UserAccount = {
        id: `user-${Date.now()}`,
        name: selectedRole === 'citizen' ? name : selectedRole === 'ngo' ? orgName : name,
        email,
        phone,
        role: selectedRole,
        isVerified: selectedRole === 'citizen' ? true : false, // Not officially verified yet for NGO/Gov!
        locality,
        organizationName: orgName,
        focusAreas,
        serviceAreas,
        department,
        designation,
        jurisdiction
      };
      onLoginSuccess(newUser);
      onClose();
    }
  };

  const handleQuickDemoLogin = (role: UserRole) => {
    if (role === 'citizen') {
      onLoginSuccess({
        id: 'cit-1',
        name: 'Aarav Patil',
        email: 'aarav.patil@mumbai.citizen.in',
        role: 'citizen',
        isVerified: true,
        phone: '+91 98201 44521',
        locality: 'Dadar West, Ward G/North (Mumbai)'
      });
    } else if (role === 'ngo') {
      onLoginSuccess({
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
      onLoginSuccess({
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
      onLoginSuccess({
        id: 'adm-1',
        name: 'Platform Administrator',
        email: 'admin@wardsync.org',
        role: 'admin',
        isVerified: true
      });
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative max-h-[90vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Title */}
        <div className="text-center mb-6">
          <h3 className="text-2xl font-bold text-slate-900">
            {activeTab === 'login' ? 'Sign in to WardSync' : 'Create an Account'}
          </h3>
          <p className="text-sm text-slate-500 mt-1">
            Connect directly with your neighborhood's civic response team.
          </p>
        </div>

        {/* Quick Demo Logins Bar for easy evaluation */}
        <div className="mb-5 p-3 bg-sky-50/70 border border-sky-200 rounded-xl text-xs">
          <p className="font-semibold text-sky-900 mb-1.5 flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-sky-600" />
            Quick Demo Sign-In (1-Click Prototype):
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
            <button
              type="button"
              onClick={() => handleQuickDemoLogin('citizen')}
              className="bg-white hover:bg-sky-100 text-sky-800 border border-sky-300 py-1 px-2 rounded-md font-medium text-[11px] transition"
            >
              👤 Citizen
            </button>
            <button
              type="button"
              onClick={() => handleQuickDemoLogin('ngo')}
              className="bg-white hover:bg-sky-100 text-emerald-800 border border-emerald-300 py-1 px-2 rounded-md font-medium text-[11px] transition"
            >
              🏢 NGO
            </button>
            <button
              type="button"
              onClick={() => handleQuickDemoLogin('government')}
              className="bg-white hover:bg-sky-100 text-amber-800 border border-amber-300 py-1 px-2 rounded-md font-medium text-[11px] transition"
            >
              🏛️ Government
            </button>
            <button
              type="button"
              onClick={() => handleQuickDemoLogin('admin')}
              className="bg-white hover:bg-sky-100 text-purple-800 border border-purple-300 py-1 px-2 rounded-md font-medium text-[11px] transition"
            >
              ⚙️ Admin
            </button>
          </div>
        </div>

        {/* Login / Register Toggle */}
        <div className="flex rounded-lg bg-slate-100 p-1 mb-5 text-sm font-medium">
          <button
            type="button"
            onClick={() => setActiveTab('login')}
            className={`flex-1 py-1.5 rounded-md transition ${
              activeTab === 'login' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('register')}
            className={`flex-1 py-1.5 rounded-md transition ${
              activeTab === 'register' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Register
          </button>
        </div>

        {/* 3 Role Selection Tabs matching Section 3 */}
        <div className="grid grid-cols-3 gap-2 mb-6">
          <button
            type="button"
            onClick={() => setSelectedRole('citizen')}
            className={`flex flex-col items-center justify-center p-3 rounded-xl border text-xs font-semibold transition ${
              selectedRole === 'citizen'
                ? 'border-sky-500 bg-sky-50/50 text-sky-900'
                : 'border-slate-200 hover:border-slate-300 text-slate-600'
            }`}
          >
            <User className="w-5 h-5 mb-1 text-sky-600" />
            <span>Citizen</span>
          </button>

          <button
            type="button"
            onClick={() => setSelectedRole('ngo')}
            className={`flex flex-col items-center justify-center p-3 rounded-xl border text-xs font-semibold transition ${
              selectedRole === 'ngo'
                ? 'border-emerald-500 bg-emerald-50/50 text-emerald-900'
                : 'border-slate-200 hover:border-slate-300 text-slate-600'
            }`}
          >
            <Building2 className="w-5 h-5 mb-1 text-emerald-600" />
            <span>NGO</span>
          </button>

          <button
            type="button"
            onClick={() => setSelectedRole('government')}
            className={`flex flex-col items-center justify-center p-3 rounded-xl border text-xs font-semibold transition ${
              selectedRole === 'government'
                ? 'border-amber-500 bg-amber-50/50 text-amber-900'
                : 'border-slate-200 hover:border-slate-300 text-slate-600'
            }`}
          >
            <Landmark className="w-5 h-5 mb-1 text-amber-600" />
            <span>Government</span>
          </button>
        </div>

        {/* Informational Banner about Verification */}
        {selectedRole !== 'citizen' && (
          <div className="mb-5 p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800 flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Role Verification Required</p>
              <p className="mt-0.5 text-amber-700">
                {selectedRole === 'ngo'
                  ? 'NGO registrations require official registration documents and admin review before verified donation permissions are unlocked.'
                  : 'Official government accounts remain pending until municipal department email and designation are confirmed.'}
              </p>
            </div>
          </div>
        )}

        {/* Dynamic Form based on selected role */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {activeTab === 'register' ? (
            <>
              {/* CITIZEN FIELDS */}
              {selectedRole === 'citizen' && (
                <>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Priya Sen"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Email</label>
                      <input
                        type="email"
                        required
                        placeholder="priya@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Phone</label>
                      <input
                        type="tel"
                        required
                        placeholder="+91 98300 XXXXX"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Home Ward / Locality</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Ward 42, Entally, Kolkata"
                      value={locality}
                      onChange={(e) => setLocality(e.target.value)}
                      className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                    />
                  </div>
                </>
              )}

              {/* NGO FIELDS */}
              {selectedRole === 'ngo' && (
                <>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Organization Name</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. CleanWater Bengal Foundation"
                      value={orgName}
                      onChange={(e) => setOrgName(e.target.value)}
                      className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Contact Person</label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Ananya Das"
                        value={contactPerson}
                        onChange={(e) => setContactPerson(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Official NGO Email</label>
                      <input
                        type="email"
                        required
                        placeholder="info@cleanwater.org"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Focus Areas</label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Clean Water, Public Health"
                        value={focusAreas}
                        onChange={(e) => setFocusAreas(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Service Areas</label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Kolkata Borough VI"
                        value={serviceAreas}
                        onChange={(e) => setServiceAreas(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Registration Certificate / 80G Proof</label>
                    <div
                      onClick={() => setDocUploaded(!docUploaded)}
                      className={`border-2 border-dashed rounded-lg p-3 text-center cursor-pointer transition text-xs ${
                        docUploaded ? 'border-emerald-400 bg-emerald-50 text-emerald-800' : 'border-slate-300 hover:border-slate-400 text-slate-500'
                      }`}
                    >
                      {docUploaded ? '✓ Certificate_WB_80G.pdf uploaded' : 'Click to attach Registration Document (PDF/JPG)'}
                    </div>
                  </div>
                </>
              )}

              {/* GOVERNMENT FIELDS */}
              {selectedRole === 'government' && (
                <>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Officer Name</label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Subhash Roy"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Designation</label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Executive Engineer"
                        value={designation}
                        onChange={(e) => setDesignation(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Official Government Department</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. KMC Water Supply Directorate"
                      value={department}
                      onChange={(e) => setDepartment(e.target.value)}
                      className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Official Email (.gov.in / official)</label>
                      <input
                        type="email"
                        required
                        placeholder="sroy@kmcgov.in"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Jurisdiction / Wards</label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Ward 42-45"
                        value={jurisdiction}
                        onChange={(e) => setJurisdiction(e.target.value)}
                        className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                      />
                    </div>
                  </div>
                </>
              )}

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Set Password</label>
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                />
              </div>
            </>
          ) : (
            <>
              {/* LOGIN FIELDS */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Registered Email</label>
                <input
                  type="email"
                  required
                  placeholder={`${selectedRole}@wardsync.org`}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                />
              </div>
            </>
          )}

          <button
            type="submit"
            className="w-full mt-4 py-2.5 bg-[#0284c7] hover:bg-[#0369a1] text-white font-semibold rounded-lg text-sm transition shadow-xs active:scale-95"
          >
            {activeTab === 'login' ? `Sign In as ${selectedRole.toUpperCase()}` : `Register as ${selectedRole.toUpperCase()}`}
          </button>
        </form>
      </div>
    </div>
  );
};
