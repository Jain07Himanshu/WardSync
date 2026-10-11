import React, { useState } from 'react';
import { X, CircleDollarSign, ShieldCheck, HeartHandshake, CheckCircle2 } from 'lucide-react';
import { Issue, NgoFundraisingCampaign } from '../types';

interface NgoRaiseFundsModalProps {
  issue: Issue | null;
  isOpen: boolean;
  onClose: () => void;
  onCampaignLaunched: (campaign: NgoFundraisingCampaign, updatedIssue: Issue) => void;
  ngoName: string;
}

export const NgoRaiseFundsModal: React.FC<NgoRaiseFundsModalProps> = ({
  issue,
  isOpen,
  onClose,
  onCampaignLaunched,
  ngoName
}) => {
  const [targetAmount, setTargetAmount] = useState<number>(50000);
  const [purpose, setPurpose] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);

  React.useEffect(() => {
    if (issue) {
      setTargetAmount(issue.donationGoal || 45000);
      setPurpose(`Emergency response & sustainable resolution for: ${issue.title}. Procurement of critical supplies, logistics, and neighborhood relief kits.`);
    }
  }, [issue]);

  if (!isOpen || !issue) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const campaign: NgoFundraisingCampaign = {
      id: `ngo-camp-${Date.now()}`,
      issueId: issue.id,
      issueTitle: issue.title,
      targetAmount,
      raisedAmount: issue.donationRaised || 0,
      purpose,
      beneficiaryOrg: ngoName,
      status: 'Active'
    };

    const updatedIssue: Issue = {
      ...issue,
      donationGoal: targetAmount,
      donationBeneficiary: `${ngoName} (Verified Civic Fund)`
    };

    onCampaignLaunched(campaign, updatedIssue);
    setIsSuccess(true);

    setTimeout(() => {
      setIsSuccess(false);
      onClose();
    }, 1800);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
      <div className="bg-white rounded-2xl max-w-lg w-full max-h-[92vh] overflow-y-auto shadow-2xl border border-slate-200 relative p-6 sm:p-7">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {isSuccess ? (
          <div className="py-10 text-center">
            <div className="w-14 h-14 bg-sky-100 text-sky-600 rounded-full flex items-center justify-center mx-auto mb-3">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Fundraising Campaign Live!</h3>
            <p className="text-xs text-slate-600 mt-1 max-w-sm mx-auto">
              Your fundraising goal of <strong>₹{targetAmount.toLocaleString()}</strong> has been assigned to {issue.title}. Citizens can now donate directly through the portal.
            </p>
          </div>
        ) : (
          <>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 rounded-lg bg-sky-100 text-sky-700 flex items-center justify-center">
                <CircleDollarSign className="w-5 h-5" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Launch Fundraising Campaign</h3>
            </div>
            <p className="text-xs text-slate-500 mb-5 font-medium">
              Mobilize public donations for: <strong className="text-slate-800">{issue.title}</strong>
            </p>

            <div className="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl text-xs text-emerald-900 flex items-center justify-between mb-5">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span>Verified Beneficiary: <strong>{ngoName}</strong></span>
              </div>
              <span className="bg-emerald-200 text-emerald-900 text-[10px] font-semibold px-2 py-0.5 rounded">
                Eligible for Tax Exemption
              </span>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Fundraising Target Goal (INR)</label>
                <div className="relative">
                  <span className="absolute left-3 top-2.5 text-slate-400 font-bold">₹</span>
                  <input
                    type="number"
                    min="1000"
                    step="500"
                    required
                    value={targetAmount}
                    onChange={(e) => setTargetAmount(parseInt(e.target.value) || 0)}
                    className="w-full pl-7 pr-3 py-2 border border-slate-300 rounded-lg text-sm font-bold text-slate-900"
                  />
                </div>
                <div className="flex gap-2 mt-2">
                  {[25000, 50000, 75000, 100000].map((preset) => (
                    <button
                      key={preset}
                      type="button"
                      onClick={() => setTargetAmount(preset)}
                      className={`text-[11px] py-1 px-2 rounded border transition ${
                        targetAmount === preset ? 'bg-sky-50 border-sky-600 text-sky-800 font-bold' : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      ₹{preset.toLocaleString()}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Fundraising Purpose & Scope</label>
                <textarea
                  required
                  rows={3}
                  value={purpose}
                  onChange={(e) => setPurpose(e.target.value)}
                  placeholder="Explain exactly how the funds will be utilized for supplies, logistics, or infrastructure..."
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                />
              </div>

              {/* Fund Allocation Plan */}
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs space-y-1.5">
                <span className="font-bold text-slate-800 block">Proposed Fund Allocation Plan:</span>
                <div className="flex justify-between text-slate-600 text-[11px]">
                  <span>Direct Relief Kits & Hardware</span>
                  <span className="font-semibold text-slate-800">65% (₹{(targetAmount * 0.65).toLocaleString()})</span>
                </div>
                <div className="flex justify-between text-slate-600 text-[11px]">
                  <span>Transport, Delivery & Mobile Bowsers</span>
                  <span className="font-semibold text-slate-800">20% (₹{(targetAmount * 0.20).toLocaleString()})</span>
                </div>
                <div className="flex justify-between text-slate-600 text-[11px]">
                  <span>Field Safety Equipment & Testing Kits</span>
                  <span className="font-semibold text-slate-800">15% (₹{(targetAmount * 0.15).toLocaleString()})</span>
                </div>
              </div>

              <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-amber-900 text-[11px] flex items-center gap-2">
                <HeartHandshake className="w-4 h-4 text-amber-600 shrink-0" />
                <span>
                  All received donations are recorded on the public transparency log. Your NGO must submit completion receipts upon expenditure.
                </span>
              </div>

              <button
                type="submit"
                className="w-full py-3 bg-[#0284c7] hover:bg-[#0369a1] text-white font-semibold text-sm rounded-lg shadow-xs transition active:scale-95"
              >
                Launch Campaign & Enable Citizen Donations
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
};
