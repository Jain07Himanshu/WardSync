import React from 'react';
import { Navigation, AlertCircle, ChevronDown, Check } from 'lucide-react';

interface HeroProps {
  selectedLocation: string;
  onSelectLocation: (loc: string) => void;
  onUseMyLocation: () => void;
  isLocating: boolean;
}

const LOCALITY_OPTIONS = [
  'All Mumbai & Thane Metropolitan Area',
  'Dadar West, Ward G/North (Mumbai)',
  'Bandra West, Ward H/West (Mumbai)',
  'Majiwada, Ward 3 (Thane)',
  'Naupada, Ward 1 (Thane)',
  'Andheri East, Ward K/East (Mumbai)',
  'Kurla West, Ward L (Mumbai)',
  'Wagle Estate, Ward 2 (Thane)',
  'Ghodbunder Road, Ward 4 (Thane)',
  'Chembur, Ward M/West (Mumbai)',
  'Kalwa, Ward 6 (Thane)',
  'Colaba, Ward A (South Mumbai)'
];

export const Hero: React.FC<HeroProps> = ({
  selectedLocation,
  onSelectLocation,
  onUseMyLocation,
  isLocating
}) => {
  const [dropdownOpen, setDropdownOpen] = React.useState(false);

  return (
    <section className="pt-10 pb-8 px-4 sm:px-6 lg:px-8 text-center max-w-4xl mx-auto">
      {/* Main Tagline Title matching Screenshot 1 */}
      <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
        Local Problems. <span className="text-[#0284c7]">Collective Action.</span>
      </h1>

      {/* Subtitle matching Screenshot 1 */}
      <p className="mt-4 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
        WardSync discovers civic issues from citizen reports, public information and official sources — then connects citizens, NGOs and authorities to fix them.
      </p>

      {/* Location Selector Controls */}
      <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3 max-w-xl mx-auto relative">
        {/* Custom Select dropdown styled to look exactly like the screenshot */}
        <div className="relative w-full sm:w-80 text-left">
          <button
            type="button"
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="w-full flex items-center justify-between bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-sm text-slate-700 shadow-xs hover:border-slate-400 focus:outline-hidden focus:ring-2 focus:ring-sky-500/20"
          >
            <span className="truncate">{selectedLocation || 'Select your city, ward or locality'}</span>
            <ChevronDown className="w-4 h-4 text-slate-400 ml-2 shrink-0" />
          </button>

          {dropdownOpen && (
            <div className="absolute top-full left-0 mt-1 w-full bg-white border border-slate-200 rounded-lg shadow-lg z-50 py-1 max-h-60 overflow-y-auto">
              {LOCALITY_OPTIONS.map((loc) => (
                <button
                  key={loc}
                  onClick={() => {
                    onSelectLocation(loc);
                    setDropdownOpen(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 flex items-center justify-between"
                >
                  <span>{loc}</span>
                  {selectedLocation === loc && <Check className="w-4 h-4 text-sky-600" />}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Use my location button matching Screenshot 1 */}
        <button
          onClick={onUseMyLocation}
          disabled={isLocating}
          className="w-full sm:w-auto flex items-center justify-center gap-2 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-sm font-medium px-4 py-2.5 rounded-lg shadow-xs transition active:scale-95 disabled:opacity-60"
        >
          <Navigation className={`w-4 h-4 text-slate-600 ${isLocating ? 'animate-spin' : ''}`} />
          <span>{isLocating ? 'Detecting GPS...' : 'Use my location'}</span>
        </button>
      </div>

      {/* Demo Prototype disclaimer badge matching Screenshot 1 */}
      <div className="mt-4 flex items-center justify-center gap-1.5 text-xs text-slate-500">
        <AlertCircle className="w-3.5 h-3.5 text-slate-400" />
        <span>Demo prototype — Issues shown are labelled sample data, not live verified incidents.</span>
      </div>
    </section>
  );
};
