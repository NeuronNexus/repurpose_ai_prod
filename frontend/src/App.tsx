import React, { useState } from 'react';
import {
  Network,
  FileSearch,
  Shield,
  CheckCircle,
  Loader,
  Download
} from 'lucide-react';

export default function RepurposeAIDashboard() {
  const [query, setQuery] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [activeAgent, setActiveAgent] = useState<string | null>(null);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState(false);

  const runAnalysis = async () => {
    if (!query.trim()) return;

    setIsRunning(true);
    setActiveAgent('master');
    setResults(null);
    setError(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      if (!res.ok) throw new Error(`API failed: ${res.status}`);

      const data = await res.json();

      setActiveAgent('clinical');
      setTimeout(() => setActiveAgent('patent'), 700);
      setTimeout(() => setActiveAgent('synthesis'), 1300);
      setTimeout(() => setActiveAgent(null), 1800);

      setResults(data);
    } catch (e: any) {
      setError(e.message || 'Unknown error');
    } finally {
      setIsRunning(false);
    }
  };

  const downloadPDF = async () => {
    if (!results) return;

    setDownloading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/report/pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ analysis: results })
      });

      if (!res.ok) throw new Error('PDF generation failed');

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = 'repurpose_report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      alert('Failed to download PDF');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b bg-white px-6 py-10">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-light text-gray-900">RepurposeAI</h1>
          <p className="text-sm text-gray-500">
            Evidence & IP-Aware Drug Repurposing Assistant
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-12">
        {/* Query Input */}
        <section className="mb-8">
          <div className="bg-white rounded-2xl p-8 border shadow-sm">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              rows={3}
              disabled={isRunning}
              placeholder="Evaluate Metformin for inflammatory conditions"
              className="w-full border rounded-lg px-4 py-3 text-sm resize-none"
            />

            <div className="flex justify-between items-center mt-4">
              {results && (
                <button
                  onClick={downloadPDF}
                  disabled={downloading}
                  className="flex items-center gap-2 text-sm px-5 py-2 border rounded-lg bg-white hover:bg-gray-50"
                >
                  {downloading ? (
                    <Loader className="w-4 h-4 animate-spin" />
                  ) : (
                    <Download className="w-4 h-4" />
                  )}
                  Download PDF
                </button>
              )}

              <button
                onClick={runAnalysis}
                disabled={isRunning || !query.trim()}
                className="bg-gray-900 text-white px-8 py-2.5 rounded-lg text-sm flex items-center gap-2 disabled:opacity-50"
              >
                {isRunning ? (
                  <>
                    <Loader className="w-4 h-4 animate-spin" />
                    Running Analysis
                  </>
                ) : (
                  'Run Analysis'
                )}
              </button>
            </div>
          </div>
        </section>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            {error}
          </div>
        )}

        <AgentSection activeAgent={activeAgent} results={results} />
        {results?.synthesis && <SynthesisSection synthesis={results.synthesis} />}
      </main>
    </div>
  );
}

// ================= AGENTS =================

function AgentSection({ activeAgent, results }: any) {
  const agents = [
    { id: 'master', icon: Network, title: 'Master Agent' },
    { id: 'clinical', icon: FileSearch, title: 'Clinical Evidence Agent' },
    { id: 'patent', icon: Shield, title: 'Patent Analysis Agent' }
  ];

  return (
    <section className="space-y-6 mb-12">
      {agents.map((a) => (
        <AgentCard
          key={a.id}
          agent={a}
          active={activeAgent === a.id}
          data={results?.[a.id]}
        />
      ))}
    </section>
  );
}

function AgentCard({ agent, active, data }: any) {
  const Icon = agent.icon;

  return (
    <div
      className={`bg-white rounded-2xl p-6 border ${
        active
          ? 'border-blue-400'
          : data
          ? 'border-green-400'
          : 'border-gray-200'
      }`}
    >
      <div className="flex items-center gap-3 mb-3">
        <div className="w-9 h-9 flex items-center justify-center rounded-lg border">
          {active ? (
            <Loader className="w-4 h-4 animate-spin text-blue-600" />
          ) : data ? (
            <CheckCircle className="w-4 h-4 text-green-600" />
          ) : (
            <Icon className="w-4 h-4 text-gray-400" />
          )}
        </div>
        <h3 className="font-medium">{agent.title}</h3>
      </div>

      {active && <p className="text-sm text-blue-600">Processing…</p>}
      {data && <AgentOutput id={agent.id} data={data} />}
    </div>
  );
}

function AgentOutput({ id, data }: any) {
  if (id === 'master')
    return <List title="Objectives" items={data.objectives} />;

  if (id === 'clinical')
    return <List title="Evidence" items={data.confidence_notes} warning />;

  if (id === 'patent')
    return (
      <>
        <p className="text-sm mb-2">
          Freedom to Operate: <b>{data.freedom_to_operate}</b>
        </p>
        <List title="Risks" items={data.risks} warning />
      </>
    );

  return null;
}

function List({ title, items, warning }: any) {
  if (!items?.length) return null;

  return (
    <div
      className={`mt-3 p-4 rounded border ${
        warning ? 'bg-amber-50 border-amber-200' : 'bg-gray-50 border-gray-200'
      }`}
    >
      <h4 className="text-sm font-medium mb-2">{title}</h4>
      <ul className="text-sm space-y-1">
        {items.map((i: string, idx: number) => (
          <li key={idx}>• {i}</li>
        ))}
      </ul>
    </div>
  );
}

// ================= SYNTHESIS =================

function SynthesisSection({ synthesis }: any) {
  return (
    <section className="bg-white rounded-2xl p-8 border shadow-sm">
      <h2 className="text-xl font-medium mb-4">Final Insight</h2>

      <div className="text-3xl font-light text-green-600 mb-4">
        {synthesis.hypothesis_strength_score.value} / 10
      </div>

      <List title="Aligned Signals" items={synthesis.aligned_signals} />
      <List title="Key Risks" items={synthesis.key_risks} warning />
      <List title="Next Steps" items={synthesis.recommended_next_steps} />

      <div className="mt-6 p-4 bg-gray-50 border rounded text-sm">
        {synthesis.opportunity_summary}
      </div>
    </section>
  );
}
