import React, { useState } from 'react';
import { CheckCircle, AlertCircle, Copy, Loader2, Sparkles, MoveRight, PenTool } from 'lucide-react';
import { AdFormData, GeneratedAdContent } from './types';
import { CATEGORIES, PRICING_OPTIONS } from './constants';
import { generateAdCopy } from './services/geminiService';
import Input from './components/Input';
import SearchableSelect from './components/SearchableSelect';
import TextArea from './components/TextArea';
import CounterInput from './components/CounterInput';

const App: React.FC = () => {
  const [formData, setFormData] = useState<AdFormData>({
    businessName: '',
    category: CATEGORIES[0],
    teamSize: 1,
    yearsExperience: 5,
    jobsCompleted: 100,
    pricingModel: PRICING_OPTIONS[0],
    pricingAmount: '',
    availability: '',
    locations: '',
    trustSignals: '',
    socialProof: '',
    portfolioLink: '',
  });

  const [result, setResult] = useState<GeneratedAdContent | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: { target: { id: string; value: string | number } }) => {
    const { id, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const handleSubmit = async () => {
    if (!formData.businessName) {
      setError('Please enter a Business Name.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const generatedContent = await generateAdCopy(formData);
      setResult(generatedContent);
    } catch (err: any) {
      setError(err.message || 'An error occurred while generating content.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen bg-[#0b0c15] text-slate-200 selection:bg-indigo-500/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
        
        {/* Header Section */}
        <div className="mb-12">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-4xl">✍️</span>
            <h1 className="text-4xl md:text-5xl font-bold text-white tracking-tight">
              Services Trust-Building Ad Copy Generator
            </h1>
          </div>
          <p className="text-lg text-slate-400 max-w-2xl">
            Generates professional ad copy using <span className="font-semibold text-white">Google Gemini</span>.
          </p>
          <div className="h-px w-full bg-slate-800 mt-8" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          
          {/* Form Section - Takes up 7 columns */}
          <div className="lg:col-span-7 space-y-8">
            
            {/* Business Info Group */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                id="businessName"
                label="Business Name"
                placeholder="e.g. Sahil's man and van company"
                value={formData.businessName}
                onChange={handleChange}
              />
              <CounterInput
                id="jobsCompleted"
                label="Jobs Completed"
                value={formData.jobsCompleted}
                onChange={handleChange}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <SearchableSelect
                id="category"
                label="Category"
                options={CATEGORIES}
                value={formData.category}
                onChange={handleChange}
                placeholder="Select category..."
              />
              <CounterInput
                id="teamSize"
                label="Team Size"
                min={1}
                value={formData.teamSize}
                onChange={handleChange}
              />
            </div>

             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <SearchableSelect
                id="pricingModel"
                label="Pricing Model"
                options={PRICING_OPTIONS}
                value={formData.pricingModel}
                onChange={handleChange}
                placeholder="Select model..."
              />
               <Input
                id="pricingAmount"
                label="Pricing Amount / Detail"
                placeholder="e.g. £50/hr"
                value={formData.pricingAmount}
                onChange={handleChange}
              />
            </div>

             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Using Input for availability but styling it to match */}
               <Input
                id="availability"
                label="Availability"
                placeholder="e.g. Next day"
                value={formData.availability}
                onChange={handleChange}
              />
               <Input
                id="locations"
                label="Locations Covered"
                placeholder="e.g. London, M25, Greater Manchester, and surrounding areas"
                value={formData.locations}
                onChange={handleChange}
              />
            </div>
            
            {/* Long Text Areas */}
            <TextArea
              id="trustSignals"
              label="Trust Signals"
              placeholder="e.g., Insurance (e.g., Public Liability), Certificates (e.g., Gas Safe, DBS Checked), Awards (e.g., Houzz Best of Service, Trustpilot 5-Star)"
              value={formData.trustSignals}
              onChange={handleChange}
              rows={3}
              className="bg-slate-800/50"
            />

            <Input
              id="socialProof"
              label="Social Proof"
              placeholder="e.g. 500+ 5-star reviews"
              value={formData.socialProof}
              onChange={handleChange}
            />

            <Input
              id="portfolioLink"
              label="External Portfolio Link"
              placeholder="e.g. www.yourwebsite.com/portfolio"
              value={formData.portfolioLink}
              onChange={handleChange}
            />

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg flex items-center gap-2">
                <AlertCircle className="w-5 h-5" />
                <span>{error}</span>
              </div>
            )}

            <button
              onClick={handleSubmit}
              disabled={loading}
              className="group w-fit mt-4 bg-slate-100 hover:bg-white text-slate-900 font-semibold py-3 px-8 rounded-lg shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_25px_rgba(255,255,255,0.2)] transition-all transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none flex items-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  Generate Title and Description
                  <MoveRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                </>
              )}
            </button>
          </div>

          {/* Result Section - Takes up 5 columns */}
          <div className="lg:col-span-5 relative">
            <div className={`sticky top-8 transition-all duration-500 ${result ? 'opacity-100 translate-y-0' : 'opacity-100'}`}>
              
              {!result && !loading && (
                 <div className="h-full min-h-[500px] bg-slate-900/30 border-2 border-dashed border-slate-800 rounded-2xl flex flex-col items-center justify-center text-slate-600 p-8 text-center">
                    <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-6">
                      <PenTool className="w-8 h-8 text-slate-500" />
                    </div>
                    <h3 className="text-xl font-bold text-slate-300 mb-2">Ready to Write</h3>
                    <p className="text-slate-500 max-w-xs leading-relaxed">
                      Fill in the details on the left and hit generate to see your ad copy here.
                    </p>
                 </div>
              )}

              {loading && (
                 <div className="h-full min-h-[500px] bg-slate-900/50 rounded-2xl flex flex-col items-center justify-center p-8 border border-slate-800">
                    <Loader2 className="w-10 h-10 text-indigo-500 animate-spin mb-4" />
                    <p className="text-slate-300">Analyzing your business details...</p>
                 </div>
              )}

              {result && (
                <div className="space-y-6 animate-fade-in-up">
                  {/* Headlines */}
                  <div className="bg-[#161b22] rounded-xl border border-slate-800 overflow-hidden shadow-2xl">
                    <div className="px-5 py-4 border-b border-slate-800 flex justify-between items-center bg-[#1f2937]/30">
                      <h3 className="font-semibold text-indigo-400 text-sm uppercase tracking-wider flex items-center gap-2">
                        Headline Options
                      </h3>
                      <button 
                        onClick={() => copyToClipboard(result.headlines)}
                        className="text-slate-400 hover:text-white text-xs flex items-center gap-1 transition-colors px-2 py-1 hover:bg-slate-700 rounded"
                      >
                        <Copy className="w-3 h-3" /> Copy
                      </button>
                    </div>
                    <div className="p-5">
                      <textarea
                        readOnly
                        className="w-full h-32 text-slate-300 bg-transparent border-none p-0 text-sm focus:ring-0 resize-none leading-relaxed font-mono"
                        value={result.headlines}
                      />
                    </div>
                  </div>

                  {/* Body Copy */}
                  <div className="bg-[#161b22] rounded-xl border border-slate-800 overflow-hidden shadow-2xl">
                     <div className="px-5 py-4 border-b border-slate-800 flex justify-between items-center bg-[#1f2937]/30">
                      <h3 className="font-semibold text-emerald-400 text-sm uppercase tracking-wider">
                        Ad Description
                      </h3>
                       <button 
                        onClick={() => copyToClipboard(result.description)}
                        className="text-slate-400 hover:text-white text-xs flex items-center gap-1 transition-colors px-2 py-1 hover:bg-slate-700 rounded"
                      >
                        <Copy className="w-3 h-3" /> Copy
                      </button>
                    </div>
                    <div className="p-5">
                      <textarea
                        readOnly
                        className="w-full h-[400px] text-slate-300 bg-transparent border-none p-0 text-sm focus:ring-0 resize-none leading-relaxed font-mono scrollbar-thin scrollbar-thumb-slate-700"
                        value={result.description}
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
