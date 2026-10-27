"use client";

import { useState, ChangeEvent, FormEvent, useEffect } from "react";
import {
  Upload,
  FileText,
  Loader2,
  AlertCircle,
  CheckCircle2,
  XCircle,
  ExternalLink,
  Sparkles,
  BookOpen,
  Code,
  ClipboardCopy,
  Check,
  FileSearch,
  LayoutDashboard,
  History,
  Trash2,
  Eye,
  LogOut,
  LogIn,
  UserPlus,
  Mail,
  Lock,
} from "lucide-react";

// -------------------------------------------------------
// INTERFACES
// -------------------------------------------------------
interface LearningResource {
  skill: string;
  resources: { title: string; url: string; type: string }[];
}

interface PredictionResult {
  prediction: string;
  confidence?: number;
  missing_skills?: string[];
  matching_skills?: string[];
  gap_percentage?: number;
  match_score?: number;
  match_level?: string;
  learning_resources?: LearningResource[];
  [key: string]: any;
}

interface HistoryItem extends PredictionResult {
  id: string;
  timestamp: number;
  fileName: string;
}

interface User {
  email: string;
}

// -------------------------------------------------------
// MAIN COMPONENT
// -------------------------------------------------------
export default function Home() {
  // --- Auth State ---
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [authLoading, setAuthLoading] = useState<boolean>(false);
  const [authError, setAuthError] = useState<string | null>(null);

  // Form State for Auth
  const [authMode, setAuthMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  // --- App State ---
  const [activeTab, setActiveTab] = useState<
    "analyzer" | "results" | "history"
  >("analyzer");
  const [jobDescription, setJobDescription] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>("");
  const [toast, setToast] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  const API_URL = "http://localhost:8000";

  // -------------------------------------------------------
  // EFFECTS
  // -------------------------------------------------------

  // Check session on mount
  useEffect(() => {
    const storedUser = localStorage.getItem("skillgap_user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }

    // Load history
    try {
      const savedHistory = localStorage.getItem("skillGapHistory");
      if (savedHistory) {
        setHistory(JSON.parse(savedHistory));
      }
    } catch (e) {
      console.error("Failed to load history", e);
    }
  }, []);

  useEffect(() => {
    if (result) {
      setActiveTab("results");
    }
  }, [result]);

  // -------------------------------------------------------
  // AUTH HANDLERS
  // -------------------------------------------------------

  const handleAuthSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setAuthLoading(true);
    setAuthError(null);

    const endpoint =
      authMode === "signup"
        ? `${API_URL}/auth/signup`
        : `${API_URL}/auth/login`;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Authentication failed");
      }

      // Success
      const userData = { email };
      localStorage.setItem("skillgap_user", JSON.stringify(userData));
      setUser(userData);
      setIsAuthenticated(true);
      showToast(`Welcome ${authMode === "signup" ? "aboard" : "back"}!`);
    } catch (err: any) {
      setAuthError(err.message);
    } finally {
      setAuthLoading(false);
    }
  };

  const handleSignOut = () => {
    localStorage.removeItem("skillgap_user");
    setIsAuthenticated(false);
    setUser(null);
    setResult(null); // Clear results on sign out
    setActiveTab("analyzer");
    showToast("Signed out successfully");
  };

  // -------------------------------------------------------
  // APP HANDLERS
  // -------------------------------------------------------

  const showToast = (message: string) => {
    setToast(message);
    setTimeout(() => setToast(null), 3000);
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (!selectedFile.name.match(/\.(pdf|txt|doc|docx)$/i)) {
        setError("Only PDF, DOC, DOCX, and TXT files are supported.");
        return;
      }
      if (selectedFile.size > 5 * 1024 * 1024) {
        setError("File size exceeds 5MB limit.");
        return;
      }
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setError(null);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file || !jobDescription.trim()) {
      setError("Please provide both a resume and job description.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Server error.");

      setResult(data);
      showToast("Analysis Complete!");
      saveToHistory(data, file.name);
    } catch (err: any) {
      setError(err.message);
      setActiveTab("analyzer");
    } finally {
      setLoading(false);
    }
  };

  const saveToHistory = (data: PredictionResult, fName: string) => {
    const newEntry: HistoryItem = {
      ...data,
      id: new Date().toISOString(),
      timestamp: Date.now(),
      fileName: fName,
    };

    const updatedHistory = [newEntry, ...history].slice(0, 20);
    setHistory(updatedHistory);
    localStorage.setItem("skillGapHistory", JSON.stringify(updatedHistory));
  };

  const loadFromHistory = (item: HistoryItem) => {
    setResult(item);
    setFileName(item.fileName);
    setActiveTab("results");
  };

  const deleteFromHistory = (id: string) => {
    const updatedHistory = history.filter((item) => item.id !== id);
    setHistory(updatedHistory);
    localStorage.setItem("skillGapHistory", JSON.stringify(updatedHistory));
    showToast("History item deleted");
  };

  const handleCopySkills = (skills: string[]) => {
    navigator.clipboard.writeText(skills.join(", "));
    showToast("Skills copied to clipboard!");
  };

  const getMatchColor = (level?: string) => {
    if (!level) return "text-slate-400";
    if (level.includes("Highly")) return "text-green-400";
    if (level.includes("Strongly")) return "text-cyan-400";
    return "text-yellow-400";
  };

  // -------------------------------------------------------
  // SUB-COMPONENTS
  // -------------------------------------------------------

  const Skeleton = ({ className }: { className: string }) => (
    <div className={`animate-pulse bg-slate-700 rounded-lg ${className}`}></div>
  );

  const LoadingState = () => (
    <div className="space-y-6 mt-10">
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 border border-slate-700 rounded-2xl p-6 h-64 flex flex-col items-center justify-center">
          <Skeleton className="w-32 h-32 rounded-full mb-4" />
          <Skeleton className="w-24 h-4" />
        </div>
        <div className="bg-slate-800/50 border border-slate-700 rounded-2xl p-6 flex flex-col justify-center items-center">
          <Skeleton className="w-16 h-16 rounded-full mb-4" />
          <Skeleton className="w-32 h-6 mb-2" />
          <Skeleton className="w-48 h-4" />
        </div>
      </div>
      <Skeleton className="w-full h-64 rounded-2xl" />
    </div>
  );

  // -------------------------------------------------------
  // RENDER: AUTH SCREEN
  // -------------------------------------------------------

  if (!isAuthenticated) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white flex flex-col items-center justify-center p-4">
        {/* Toast */}
        {toast && (
          <div className="fixed top-5 right-5 z-50 bg-green-600 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-2">
            <Check className="w-5 h-5" />
            <span>{toast}</span>
          </div>
        )}

        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              Skill Gap Analyzer
            </h1>
            <p className="text-slate-400">Sign in to continue</p>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl shadow-2xl p-8">
            {/* Tab Switcher */}
            <div className="flex mb-6 bg-slate-900/50 rounded-lg p-1">
              <button
                onClick={() => {
                  setAuthMode("signin");
                  setAuthError(null);
                }}
                className={`w-1/2 py-2 text-sm font-medium rounded-md transition-colors ${authMode === "signin" ? "bg-cyan-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                Sign In
              </button>
              <button
                onClick={() => {
                  setAuthMode("signup");
                  setAuthError(null);
                }}
                className={`w-1/2 py-2 text-sm font-medium rounded-md transition-colors ${authMode === "signup" ? "bg-cyan-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                Sign Up
              </button>
            </div>

            <form onSubmit={handleAuthSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-2.5 w-5 h-5 text-slate-500" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full pl-10 pr-4 py-2 bg-slate-900/50 border border-slate-600 rounded-lg focus:ring-2 focus:ring-cyan-500 outline-none text-white placeholder-slate-500"
                    placeholder="you@example.com"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-2.5 w-5 h-5 text-slate-500" />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="w-full pl-10 pr-4 py-2 bg-slate-900/50 border border-slate-600 rounded-lg focus:ring-2 focus:ring-cyan-500 outline-none text-white placeholder-slate-500"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              {authError && (
                <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-2 rounded-lg text-sm">
                  <AlertCircle className="w-4 h-4" />
                  {authError}
                </div>
              )}

              <button
                type="submit"
                disabled={authLoading}
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-bold py-2.5 px-4 rounded-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {authLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <>
                    {authMode === "signin" ? (
                      <LogIn className="w-5 h-5" />
                    ) : (
                      <UserPlus className="w-5 h-5" />
                    )}
                    {authMode === "signin" ? "Sign In" : "Create Account"}
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </main>
    );
  }

  // -------------------------------------------------------
  // RENDER: DASHBOARD (LOGGED IN)
  // -------------------------------------------------------

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white p-4 md:p-8">
      {/* Toast Notification */}
      {toast && (
        <div className="fixed top-5 right-5 z-50 bg-green-600 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-2 animate-in slide-in-from-top transition-transform">
          <Check className="w-5 h-5" />
          <span>{toast}</span>
        </div>
      )}

      <div className="max-w-5xl mx-auto">
        {/* -------------------------------------------------------
            UPDATED HEADER LAYOUT
        ------------------------------------------------------- */}
        <div className="mb-8">
          {/* Title: Centered at Top */}
          <div className="text-center mb-4">
            <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              AI Skill Gap Analyzer
            </h1>
          </div>

          {/* Sub-header: Welcome Left, Sign Out Right */}
          <div className="flex justify-between items-center">
            <p className="text-slate-400 text-sm">
              Welcome back,{" "}
              <span className="text-cyan-400 font-medium">{user?.email}</span>
            </p>

            <button
              onClick={handleSignOut}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-slate-300 hover:text-white transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex bg-slate-800/60 p-1 rounded-xl border border-slate-700">
            <button
              onClick={() => setActiveTab("analyzer")}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-medium transition-all duration-200 ${
                activeTab === "analyzer"
                  ? "bg-cyan-600 text-white shadow-lg"
                  : "text-slate-400 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <FileSearch className="w-4 h-4" />
              Analyzer
            </button>
            <button
              onClick={() => result && setActiveTab("results")}
              disabled={!result}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-medium transition-all duration-200 ${
                activeTab === "results"
                  ? "bg-cyan-600 text-white shadow-lg"
                  : "text-slate-400 hover:text-white hover:bg-slate-700/50 disabled:opacity-50 disabled:cursor-not-allowed"
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              Results
            </button>

            <button
              onClick={() => setActiveTab("history")}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-medium transition-all duration-200 ${
                activeTab === "history"
                  ? "bg-cyan-600 text-white shadow-lg"
                  : "text-slate-400 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <History className="w-4 h-4" />
              History
              {history.length > 0 && (
                <span className="bg-slate-900 text-cyan-300 text-xs px-1.5 py-0.5 rounded-full">
                  {history.length}
                </span>
              )}
            </button>
          </div>
        </div>

        {/* TAB CONTENT: ANALYZER */}
        {activeTab === "analyzer" && (
          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl shadow-2xl p-6 md:p-8 animate-in fade-in duration-300">
            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Resume
                  </label>
                  <label
                    htmlFor="dropzone-file"
                    className={`flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-xl cursor-pointer transition-all duration-300 ${
                      file
                        ? "border-green-500 bg-green-500/10"
                        : "border-slate-600 bg-slate-800 hover:border-cyan-500 hover:bg-slate-700/30"
                    }`}
                  >
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      {file ? (
                        <>
                          <CheckCircle2 className="w-12 h-12 text-green-400 mb-3" />
                          <p className="text-sm text-green-400 font-semibold px-4 text-center">
                            {fileName}
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            Click to change
                          </p>
                        </>
                      ) : (
                        <>
                          <Upload className="w-10 h-10 text-slate-400 mb-3" />
                          <p className="text-sm text-slate-400">
                            <span className="font-semibold">
                              Click to upload
                            </span>
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            PDF, DOCX, TXT (MAX. 5MB)
                          </p>
                        </>
                      )}
                    </div>
                    <input
                      id="dropzone-file"
                      type="file"
                      className="hidden"
                      onChange={handleFileChange}
                      accept=".pdf,.txt,.doc,.docx"
                    />
                  </label>
                </div>

                <div className="flex flex-col">
                  <label
                    htmlFor="jd"
                    className="block text-sm font-medium text-slate-300 mb-2"
                  >
                    Job Description
                  </label>
                  <textarea
                    id="jd"
                    rows={8}
                    className="w-full h-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-xl focus:ring-2 focus:ring-cyan-500 outline-none resize-none text-slate-200 placeholder-slate-500 transition-all"
                    placeholder="Paste the full job description here..."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                  />
                </div>
              </div>

              {error && (
                <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg animate-in fade-in">
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                  <span className="text-sm">{error}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={loading || !file || !jobDescription}
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-[1.01] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing Resume...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Analyze Skill Gap
                  </>
                )}
              </button>
            </form>
          </div>
        )}

        {/* TAB CONTENT: RESULTS */}
        {activeTab === "results" && (
          <div className="animate-in fade-in duration-300">
            {loading ? (
              <LoadingState />
            ) : result ? (
              <div className="space-y-6">
                {/* Top Summary Cards */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="bg-slate-800/50 border border-slate-700 rounded-2xl p-6 flex flex-col items-center justify-center relative overflow-hidden">
                    <div className="absolute w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl -top-10 -left-10"></div>

                    <div className="relative w-40 h-40 flex items-center justify-center">
                      <svg
                        className="w-full h-full transform -rotate-90"
                        viewBox="0 0 100 100"
                      >
                        <circle
                          cx="50"
                          cy="50"
                          r="40"
                          stroke="currentColor"
                          strokeWidth="10"
                          fill="transparent"
                          className="text-slate-700"
                        />
                        <circle
                          cx="50"
                          cy="50"
                          r="40"
                          stroke="currentColor"
                          strokeWidth="10"
                          fill="transparent"
                          strokeDasharray={251.2}
                          strokeDashoffset={
                            251.2 - (251.2 * (result.match_score || 0)) / 100
                          }
                          strokeLinecap="round"
                          className={
                            result.match_score && result.match_score > 50
                              ? "text-green-500"
                              : "text-yellow-500"
                          }
                        />
                      </svg>
                      <div className="absolute text-center">
                        <span className="text-4xl font-bold">
                          {result.match_score || 0}%
                        </span>
                        <span className="block text-xs text-slate-400">
                          Match Score
                        </span>
                      </div>
                    </div>
                    <div className="mt-4 text-center z-10">
                      <p className="text-slate-400 text-sm">Gap Percentage</p>
                      <p className="text-xl font-bold text-white">
                        {result.gap_percentage || 0}% Gap Detected
                      </p>
                    </div>
                  </div>

                  <div className="bg-slate-800/50 border border-slate-700 rounded-2xl p-6 flex flex-col justify-center items-center relative">
                    <Sparkles
                      className={`w-20 h-20 mb-4 ${getMatchColor(result.match_level)}`}
                    />
                    <p className="text-slate-400 text-sm mb-2">
                      Candidate Potential
                    </p>
                    <h3
                      className={`text-3xl font-bold text-center ${getMatchColor(result.match_level)}`}
                    >
                      {result.match_level || "Analyzing..."}
                    </h3>
                    <p className="text-slate-500 text-sm mt-4 text-center max-w-xs">
                      {result.match_level === "Highly Matched"
                        ? "Excellent fit! Minimal skill gaps detected."
                        : result.match_level === "Strongly Matched"
                          ? "Good potential. Some areas to improve."
                          : "Considerable gaps. Upskilling recommended."}
                    </p>
                  </div>
                </div>

                {/* Skills Section */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="bg-slate-800/50 border border-green-500/30 rounded-2xl p-6 transition-all hover:border-green-500/50">
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-lg font-bold text-white flex items-center gap-2">
                        <CheckCircle2 className="w-5 h-5 text-green-400" />
                        Matched Skills
                      </h3>
                      <span className="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded-full">
                        {result.matching_skills?.length || 0} Found
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-2 min-h-[50px] items-start">
                      {result.matching_skills &&
                      result.matching_skills.length > 0 ? (
                        result.matching_skills.map((skill, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1.5 inline-flex items-center bg-green-500/20 text-green-300 border border-green-500/30 rounded-lg text-sm font-medium transition-transform hover:scale-105"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <p className="text-slate-500 text-sm italic">
                          No specific skills matched.
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="bg-slate-800/50 border border-red-500/30 rounded-2xl p-6 transition-all hover:border-red-500/50">
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-lg font-bold text-white flex items-center gap-2">
                        <XCircle className="w-5 h-5 text-red-400" />
                        Unmatched Skills
                      </h3>
                      <button
                        onClick={() =>
                          handleCopySkills(result.missing_skills || [])
                        }
                        className="text-xs bg-slate-700 hover:bg-slate-600 text-slate-300 px-2 py-1 rounded-full flex items-center gap-1 transition-colors"
                      >
                        <ClipboardCopy className="w-3 h-3" /> Copy
                      </button>
                    </div>
                    <div className="flex flex-wrap gap-2 min-h-[50px] items-start">
                      {result.missing_skills &&
                      result.missing_skills.length > 0 ? (
                        result.missing_skills.map((skill, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1.5 inline-flex items-center bg-red-500/20 text-red-300 border border-red-500/30 rounded-lg text-sm font-medium transition-transform hover:scale-105"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <p className="text-slate-500 text-sm italic">
                          No skill gaps detected!
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Learning Resources */}
                {result.learning_resources &&
                  result.learning_resources.length > 0 && (
                    <div className="bg-slate-800/50 border border-cyan-500/30 rounded-2xl p-6">
                      <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <BookOpen className="w-6 h-6 text-cyan-400" />
                        Recommended Learning Paths
                      </h3>
                      <div className="space-y-4">
                        {result.learning_resources.map((item, index) => (
                          <div
                            key={index}
                            className="bg-slate-900/40 rounded-xl p-4 border border-slate-700 hover:border-slate-600 transition-colors"
                          >
                            <h4 className="text-lg font-semibold text-cyan-300 mb-3 flex items-center gap-2">
                              <span className="w-2 h-2 bg-cyan-400 rounded-full"></span>
                              Resources for:{" "}
                              <span className="text-white">{item.skill}</span>
                            </h4>
                            <div className="grid sm:grid-cols-2 gap-3">
                              {item.resources.map((res, idx) => {
                                const title =
                                  typeof res === "string" ? res : res.title;
                                const url =
                                  typeof res === "string" ? "#" : res.url;
                                return (
                                  <a
                                    key={idx}
                                    href={url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg hover:bg-slate-700 transition-all group border border-slate-600 hover:border-cyan-500 hover:shadow-md"
                                  >
                                    <ExternalLink className="w-5 h-5 text-cyan-400 flex-shrink-0 group-hover:scale-110 transition-transform" />
                                    <span className="text-slate-200 group-hover:text-white text-sm font-medium">
                                      {title}
                                    </span>
                                  </a>
                                );
                              })}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                <details className="mt-4 text-xs text-slate-500 group">
                  <summary className="cursor-pointer hover:text-slate-300 flex items-center gap-2 select-none">
                    <Code className="w-4 h-4 group-open:rotate-90 transition-transform" />{" "}
                    View Raw API Response
                  </summary>
                  <pre className="mt-2 p-4 bg-slate-900 rounded-lg overflow-auto text-slate-400 border border-slate-700 max-h-64">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </details>
              </div>
            ) : (
              <div className="text-center py-20 text-slate-400">
                <FileSearch className="w-16 h-16 mx-auto mb-4 opacity-20" />
                <p>No results yet. Run an analysis first.</p>
              </div>
            )}
          </div>
        )}

        {/* TAB CONTENT: HISTORY */}
        {activeTab === "history" && (
          <div className="animate-in fade-in duration-300 space-y-4">
            {history.length === 0 ? (
              <div className="text-center py-20 text-slate-400 bg-slate-800/50 rounded-2xl border border-slate-700">
                <History className="w-16 h-16 mx-auto mb-4 opacity-20" />
                <p>No history yet. Analyze a resume to start tracking.</p>
              </div>
            ) : (
              <>
                <div className="flex justify-between items-center mb-2 px-1">
                  <span className="text-slate-400 text-sm">
                    {history.length} previous analyses stored locally
                  </span>
                  <button
                    onClick={() => {
                      if (
                        confirm("Are you sure you want to clear all history?")
                      ) {
                        setHistory([]);
                        localStorage.removeItem("skillGapHistory");
                        showToast("History cleared");
                      }
                    }}
                    className="text-xs text-red-400 hover:text-red-300 transition-colors"
                  >
                    Clear All
                  </button>
                </div>
                <div className="grid gap-4">
                  {history.map((item) => (
                    <div
                      key={item.id}
                      className="bg-slate-800/50 border border-slate-700 rounded-xl p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:border-slate-600 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <div className="p-3 bg-slate-700/50 rounded-lg">
                          <FileText className="w-6 h-6 text-cyan-400" />
                        </div>
                        <div>
                          <h4 className="font-semibold text-white">
                            {item.fileName}
                          </h4>
                          <p className="text-xs text-slate-500">
                            {new Date(item.timestamp).toLocaleDateString()} at{" "}
                            {new Date(item.timestamp).toLocaleTimeString()}
                          </p>
                          <div className="flex gap-2 mt-1">
                            <span
                              className={`text-xs font-medium ${getMatchColor(item.match_level)}`}
                            >
                              {item.match_level}
                            </span>
                            <span className="text-xs text-slate-600">•</span>
                            <span className="text-xs text-slate-400">
                              Score: {item.match_score}%
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="flex gap-2 w-full sm:w-auto">
                        <button
                          onClick={() => loadFromHistory(item)}
                          className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-lg text-white text-sm font-medium transition-colors"
                        >
                          <Eye className="w-4 h-4" /> View
                        </button>
                        <button
                          onClick={() => deleteFromHistory(item.id)}
                          className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2 bg-slate-700 hover:bg-red-500/20 hover:text-red-400 rounded-lg text-slate-300 text-sm font-medium transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        )}

        <footer className="text-center mt-12 text-slate-600 text-sm">
          Powered by FastAPI & Next.js
        </footer>
      </div>
    </main>
  );
}
