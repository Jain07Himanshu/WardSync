import React from 'react';
import { MapPin, User, LogOut, ShieldCheck, Building2, Landmark, CheckCircle2 } from 'lucide-react';
import { UserAccount } from '../types';

interface HeaderProps {
  currentUser: UserAccount | null;
  onOpenAuth: (role?: 'citizen' | 'ngo' | 'government') => void;
  onLogout: () => void;
  onSwitchUser: (role: 'citizen' | 'ngo' | 'government' | 'admin' | 'guest') => void;
  activeView: 'home' | 'explore' | 'volunteer' | 'about' | 'dashboards';
  setActiveView: (view: 'home' | 'explore' | 'volunteer' | 'about' | 'dashboards') => void;
  onOpenReportModal: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentUser,
  onOpenAuth,
  onLogout,
  onSwitchUser,
  activeView,
  setActiveView,
  onOpenReportModal
}) => {
  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200">
      {/* Top Demo Bar to easily test all 4 roles specified in requirements */}
      <div className="bg-slate-900 text-slate-200 text-xs py-1.5 px-4">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="font-medium text-slate-300">Prototype Demo Persona:</span>
            <span className="text-white font-semibold">
              {currentUser ? `${currentUser.name} (${currentUser.role.toUpperCase()})` : 'Public Visitor (Guest)'}
            </span>
            {currentUser?.isVerified ? (
              <span className="inline-flex items-center gap-1 bg-emerald-950 text-emerald-300 text-[10px] px-1.5 py-0.5 rounded border border-emerald-800">
                <CheckCircle2 className="w-3 h-3" /> Verified
              </span>
            ) : currentUser && (
              <span className="inline-flex items-center gap-1 bg-amber-950 text-amber-300 text-[10px] px-1.5 py-0.5 rounded border border-amber-800">
                Pending Verification
              </span>
            )}
          </div>

          <div className="flex items-center gap-1.5 text-[11px]">
            <span className="text-slate-400">Switch persona:</span>
            <button
              onClick={() => onSwitchUser('citizen')}
              className={`px-2 py-0.5 rounded transition ${currentUser?.role === 'citizen' ? 'bg-sky-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              Citizen
            </button>
            <button
              onClick={() => onSwitchUser('ngo')}
              className={`px-2 py-0.5 rounded transition ${currentUser?.role === 'ngo' ? 'bg-sky-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              NGO
            </button>
            <button
              onClick={() => onSwitchUser('government')}
              className={`px-2 py-0.5 rounded transition ${currentUser?.role === 'government' ? 'bg-sky-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              Government
            </button>
            <button
              onClick={() => onSwitchUser('admin')}
              className={`px-2 py-0.5 rounded transition ${currentUser?.role === 'admin' ? 'bg-sky-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              Admin
            </button>
            <button
              onClick={() => onSwitchUser('guest')}
              className={`px-2 py-0.5 rounded transition ${!currentUser ? 'bg-sky-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              Guest
            </button>
          </div>
        </div>
      </div>

      {/* Main Header matching screenshot */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <div 
          onClick={() => setActiveView('home')}
          className="flex items-center gap-2.5 cursor-pointer group select-none"
        >
          <div className="w-9 h-9 rounded-xl bg-sky-600 text-white flex items-center justify-center shadow-sm group-hover:bg-sky-700 transition">
            <MapPin className="w-5 h-5 fill-white/20 stroke-[2.2]" />
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-900 font-sans">
            WardSync
          </span>
        </div>

        {/* Navigation items matching screenshot */}
        <nav className="hidden md:flex items-center gap-8 text-[15px] font-medium text-slate-600">
          <button 
            onClick={() => setActiveView('home')}
            className={`transition hover:text-slate-900 ${activeView === 'home' ? 'text-sky-600 font-semibold' : ''}`}
          >
            Home
          </button>
          <button 
            onClick={() => setActiveView('explore')}
            className={`transition hover:text-slate-900 ${activeView === 'explore' ? 'text-sky-600 font-semibold' : ''}`}
          >
            Explore Issues
          </button>
          <button 
            onClick={() => setActiveView('volunteer')}
            className={`transition hover:text-slate-900 ${activeView === 'volunteer' ? 'text-sky-600 font-semibold' : ''}`}
          >
            Volunteer
          </button>
          <button 
            onClick={() => setActiveView('about')}
            className={`transition hover:text-slate-900 ${activeView === 'about' ? 'text-sky-600 font-semibold' : ''}`}
          >
            About
          </button>
          {currentUser && (
            <button 
              onClick={() => setActiveView('dashboards')}
              className={`transition hover:text-slate-900 flex items-center gap-1.5 ${activeView === 'dashboards' ? 'text-sky-600 font-semibold' : ''}`}
            >
              {currentUser.role === 'citizen' && <User className="w-4 h-4 text-sky-600" />}
              {currentUser.role === 'ngo' && <Building2 className="w-4 h-4 text-emerald-600" />}
              {currentUser.role === 'government' && <Landmark className="w-4 h-4 text-amber-600" />}
              {currentUser.role === 'admin' && <ShieldCheck className="w-4 h-4 text-purple-600" />}
              <span>Dashboard</span>
            </button>
          )}
        </nav>

        {/* Right Action buttons matching screenshot */}
        <div className="flex items-center gap-3">
          <button
            onClick={onOpenReportModal}
            className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-sky-700 bg-sky-50 border border-sky-200 rounded-lg hover:bg-sky-100 transition"
          >
            + Report Issue
          </button>

          {currentUser ? (
            <div className="flex items-center gap-3">
              <button
                onClick={() => setActiveView('dashboards')}
                className="hidden sm:flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition"
              >
                <span>{currentUser.name.split(' ')[0]}</span>
                <span className="text-[11px] text-slate-500 uppercase">({currentUser.role})</span>
              </button>
              <button
                onClick={onLogout}
                title="Sign out"
                className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <>
              <button
                onClick={() => onOpenAuth()}
                className="text-[15px] font-medium text-slate-700 hover:text-slate-900 px-3 py-1.5 transition"
              >
                Sign In
              </button>
              <button
                onClick={() => onOpenAuth('citizen')}
                className="text-[15px] font-medium bg-[#0284c7] hover:bg-[#0369a1] text-white px-4 py-2 rounded-lg shadow-sm transition active:scale-95"
              >
                Get Started
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
};
