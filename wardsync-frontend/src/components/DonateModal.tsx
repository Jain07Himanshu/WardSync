import React, { useState } from 'react';
import { X, Heart, ShieldCheck, AlertCircle, CheckCircle2, History } from 'lucide-react';
import { Issue, DonationRecord } from '../types';

interface DonateModalProps {
  issue: Issue | null;
  isOpen: boolean;
  onClose: () => void;
  onDonationComplete: (record: DonationRecord) => void;
  donationHistory: DonationRecord[];
}

const PRESET_AMOUNTS = [250, 500, 1000, 2500];

export const DonateModal: React.FC<DonateModalProps> = ({
  issue,
  isOpen,
  onClose,
  onDonationComplete,
  donationHistory
}) => {
  const [selectedAmount, setSelectedAmount] = useState<number>(500);
  const [customAmount, setCustomAmount] = useState<string>('');
  const [donorName, setDonorName] = useState<string>('Priya Sen');
  const [donorEmail, setDonorEmail] = useState<string>('priya.sen@example.com');
  const [isAnonymous, setIsAnonymous] = useState<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [successRecord, setSuccessRecord] = useState<DonationRecord | null>(null);

  if (!isOpen || !issue) return null;

  const currentAmount = customAmount ? parseFloat(customAmount) || 0 : selectedAmount;
  const remainingAmount = Math.max(0, issue.donationGoal - issue.donationRaised);
  const progressPercent = Math.min(100, Math.round((issue.donationRaised / issue.donationGoal) * 100));

  const handleSimulatePayment = (e: React.FormEvent) => {
    e.preventDefault();
    if (currentAmount <= 0) return;

    setIsProcessing(true);

    setTimeout(() => {
      const newRecord: DonationRecord = {
        id: `sim-txn-${Date.now()}`,
        issueId: issue.id,
        issueTitle: issue.title,
        amount: currentAmount,
        donorName: isAnonymous ? 'Anonymous Citizen' : donorName,
        isAnonymous,
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        simulatedTxnId: `DEMO_WB_${Math.floor(100000 + Math.random() * 900000)}`
      };

      setIsProcessing(false);
      setSuccessRecord(newRecord);
      onDonationComplete(newRecord);
    }, 1200);
  };

  const handleClose = () => {
    setSuccessRecord(null);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-200 relative max-h-[90vh] overflow-y-auto">
        <button
          onClick={handleClose}
          className="absolute right-4 top-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {successRecord ? (
          /* SUCCESS STATE */
          <div className="text-center py-6">
            <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Donation Confirmed! (Demo)</h3>
            <p className="text-sm text-slate-600 mt-1 max-w-sm mx-auto">
              Thank you, <strong>{successRecord.donorName}</strong>. Your simulated pledge of <strong>₹{successRecord.amount.toLocaleString()}</strong> has been credited to {issue.donationBeneficiary}.
            </p>

            <div className="my-5 p-4 bg-slate-50 border border-slate-200 rounded-xl text-left text-xs space-y-1.5 font-mono">
              <div className="flex justify-between">
                <span className="text-slate-500">Transaction Ref:</span>
                <span className="font-semibold text-slate-800">{successRecord.simulatedTxnId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Beneficiary:</span>
                <span className="font-semibold text-slate-800">{issue.donationBeneficiary}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Amount:</span>
                <span className="font-bold text-emerald-700">₹{successRecord.amount.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Status:</span>
                <span className="text-emerald-600 font-semibold">Simulated Demo Success</span>
              </div>
            </div>

            <button
              onClick={handleClose}
              className="w-full py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-medium text-sm rounded-lg transition"
            >
              Close & Return
            </button>
          </div>
        ) : (
          /* DONATION FORM */
          <>
            <div className="flex items-center gap-2 mb-1">
              <Heart className="w-5 h-5 text-sky-600 fill-sky-100" />
              <h3 className="text-lg font-bold text-slate-900">Support Problem Resolution</h3>
            </div>
            <p className="text-xs text-slate-500 mb-4 font-medium">{issue.title}</p>

            {/* Beneficiary Badge */}
            <div className="flex items-center gap-2 p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs mb-5">
              <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
              <div className="truncate">
                <span className="text-slate-500">Verified Recipient NGO:</span>{' '}
                <strong className="text-slate-800">{issue.donationBeneficiary}</strong>
              </div>
            </div>

            {/* Fundraising Progress */}
            <div className="space-y-1.5 mb-6">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500 font-medium">Raised: <strong className="text-slate-800">₹{issue.donationRaised.toLocaleString()}</strong></span>
                <span className="text-slate-500 font-medium">Target: <strong className="text-slate-800">₹{issue.donationGoal.toLocaleString()}</strong></span>
              </div>
              <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-sky-600 rounded-full transition-all duration-500" style={{ width: `${progressPercent}%` }} />
              </div>
              <div className="flex justify-between text-[11px] text-slate-400">
                <span>{progressPercent}% funded</span>
                <span>₹{remainingAmount.toLocaleString()} remaining</span>
              </div>
            </div>

            {/* Safe Prototype Demo Warning Banner matching Requirement 5 */}
            <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800 flex items-start gap-2 mb-5">
              <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">Simulated Prototype Demo</p>
                <p className="mt-0.5 text-amber-700 leading-snug">
                  No real payments are collected. Do not enter actual bank or credit card credentials. In production, this connects to Razorpay/Stripe with audited NGO KYC.
                </p>
              </div>
            </div>

            <form onSubmit={handleSimulatePayment} className="space-y-4 text-xs">
              {/* Preset Amounts */}
              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">Select Contribution Amount (INR)</label>
                <div className="grid grid-cols-4 gap-2">
                  {PRESET_AMOUNTS.map((amt) => (
                    <button
                      key={amt}
                      type="button"
                      onClick={() => {
                        setSelectedAmount(amt);
                        setCustomAmount('');
                      }}
                      className={`py-2 text-xs font-bold rounded-lg border transition ${
                        selectedAmount === amt && !customAmount
                          ? 'bg-sky-50 border-sky-600 text-sky-800 shadow-2xs'
                          : 'bg-white border-slate-200 hover:border-slate-300 text-slate-700'
                      }`}
                    >
                      ₹{amt}
                    </button>
                  ))}
                </div>

                <div className="mt-2.5">
                  <input
                    type="number"
                    min="10"
                    placeholder="Or enter custom amount (₹)"
                    value={customAmount}
                    onChange={(e) => {
                      setCustomAmount(e.target.value);
                    }}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-1 focus:ring-sky-500 focus:border-sky-500"
                  />
                </div>
              </div>

              {/* Donor Info */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Donor Name</label>
                  <input
                    type="text"
                    disabled={isAnonymous}
                    value={donorName}
                    onChange={(e) => setDonorName(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs disabled:bg-slate-100 disabled:text-slate-400"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Receipt Email</label>
                  <input
                    type="email"
                    value={donorEmail}
                    onChange={(e) => setDonorEmail(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs"
                  />
                </div>
              </div>

              {/* Anonymous Checkbox */}
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="anonymousCheck"
                  checked={isAnonymous}
                  onChange={(e) => setIsAnonymous(e.target.checked)}
                  className="rounded text-sky-600 focus:ring-sky-500"
                />
                <label htmlFor="anonymousCheck" className="text-slate-600 text-xs cursor-pointer select-none">
                  Make my donation anonymous on public leaderboards
                </label>
              </div>

              {/* Submit Demo Payment */}
              <button
                type="submit"
                disabled={isProcessing || currentAmount <= 0}
                className="w-full py-2.5 bg-[#0284c7] hover:bg-[#0369a1] text-white font-semibold text-sm rounded-lg shadow-xs transition active:scale-95 disabled:opacity-50"
              >
                {isProcessing ? 'Processing Demo Payment...' : `Simulate Donation of ₹${currentAmount.toLocaleString()}`}
              </button>
            </form>

            {/* Recent Donations History List */}
            {donationHistory.length > 0 && (
              <div className="mt-6 pt-4 border-t border-slate-100">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 mb-2">
                  <History className="w-3.5 h-3.5 text-slate-400" />
                  <span>Recent Simulated Contributions</span>
                </div>
                <div className="space-y-1.5 max-h-24 overflow-y-auto pr-1">
                  {donationHistory.slice(0, 3).map((item) => (
                    <div key={item.id} className="flex justify-between items-center text-[11px] p-1.5 bg-slate-50 rounded">
                      <span className="text-slate-700 truncate max-w-[180px]">{item.donorName}</span>
                      <span className="font-semibold text-emerald-700">₹{item.amount.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};
