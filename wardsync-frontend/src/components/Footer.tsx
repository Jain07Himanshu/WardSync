import React from 'react';
import { MapPin } from 'lucide-react';

interface FooterProps {
  onNavClick: (view: 'about' | 'privacy' | 'terms' | 'contact') => void;
}

export const Footer: React.FC<FooterProps> = ({ onNavClick }) => {
  return (
    <footer className="border-t border-slate-200 bg-white pt-12 pb-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-8 pb-10">
          {/* Brand & Mission matching Screenshot 2 */}
          <div className="max-w-md">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-sky-600 text-white flex items-center justify-center">
                <MapPin className="w-4 h-4 fill-white/20" />
              </div>
              <span className="text-lg font-bold text-slate-900 tracking-tight">WardSync</span>
            </div>
            <p className="mt-2 text-sm text-slate-700 font-medium">
              Local Problems. Collective Action.
            </p>
            <p className="mt-3 text-xs text-slate-500 leading-relaxed">
              Prototype running on clearly labelled sample data. Issues shown are demonstrations, not live verified incidents.
            </p>
          </div>

          {/* Quick Links matching Screenshot 2 */}
          <div className="grid grid-cols-2 gap-x-12 gap-y-3 text-sm text-slate-600">
            <button
              onClick={() => onNavClick('about')}
              className="text-left hover:text-slate-900 transition"
            >
              About
            </button>
            <button
              onClick={() => onNavClick('contact')}
              className="text-left hover:text-slate-900 transition"
            >
              Contact
            </button>
            <button
              onClick={() => onNavClick('privacy')}
              className="text-left hover:text-slate-900 transition"
            >
              Privacy Policy
            </button>
            <button
              onClick={() => onNavClick('terms')}
              className="text-left hover:text-slate-900 transition"
            >
              Terms
            </button>
          </div>
        </div>

        {/* Bottom copyright line matching Screenshot 2 */}
        <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-2">
          <p>© 2026 WardSync. Built for civic coordination.</p>
          <p className="text-slate-400">Accessible · Transparent · Evidence-backed</p>
        </div>
      </div>
    </footer>
  );
};
