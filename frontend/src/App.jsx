import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BookOpen, MessageSquare, ExternalLink, Loader2, Star, Send } from 'lucide-react';

const API_BASE = "http://127.0.0.1:8000/api";

const App = () => {
  const [books, setBooks] = useState([]);
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState('dashboard');

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get(`${API_BASE}/books/`); 
        setBooks(response.data);
      } catch (err) {
        console.error("Failed to fetch books:", err);
      }
    };
    fetchBooks();
  }, []);

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!query) return;
    setLoading(true);
    setResult(null); // Clear previous result
    try {
      const response = await axios.post(`${API_BASE}/query/`, { query });
      setResult(response.data);
    } catch (err) {
      console.error("Query failed:", err);
      alert("The AI service is currently unavailable. Please try again later.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] font-sans text-slate-900">
      {/* Navbar */}
      <nav className="bg-slate-900 text-white p-4 sticky top-0 z-50 shadow-lg border-b border-white/10">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-black tracking-tighter uppercase italic">
            Ergosphere <span className="text-blue-400 not-italic">Intel</span>
          </h1>
          <div className="flex bg-slate-800 p-1 rounded-xl border border-slate-700">
            <button 
              onClick={() => setView('dashboard')}
              className={`px-5 py-2 rounded-lg text-sm font-bold transition-all ${view === 'dashboard' ? 'bg-blue-600 shadow-lg text-white' : 'text-slate-400 hover:text-white'}`}
            >
              Bookshelf
            </button>
            <button 
              onClick={() => setView('chat')}
              className={`px-5 py-2 rounded-lg text-sm font-bold transition-all ${view === 'chat' ? 'bg-blue-600 shadow-lg text-white' : 'text-slate-400 hover:text-white'}`}
            >
              AI Assistant
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto p-6">
        {view === 'dashboard' ? (
          /* --- BOOKSHELF VIEW --- */
          <div className="animate-in fade-in slide-in-from-bottom-2 duration-700">
            <div className="flex justify-between items-end mb-8 border-b border-slate-200 pb-4">
              <div>
                <h2 className="text-3xl font-black text-slate-800">The Catalog</h2>
                <p className="text-slate-500 font-medium">Browse through {books.length} automated discoveries</p>
              </div>
              <BookOpen className="text-blue-600 opacity-20" size={48} />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {books.map((book) => (
                <div key={book.id} className="group bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden">
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div className="bg-blue-50 text-blue-600 p-2 rounded-lg group-hover:bg-blue-600 group-hover:text-white transition-colors">
                        <BookOpen size={20} />
                      </div>
                      <div className="flex items-center gap-1 bg-amber-50 text-amber-600 px-2 py-1 rounded-full text-xs font-black border border-amber-100">
                        <Star size={12} fill="currentColor" /> {book.rating}
                      </div>
                    </div>
                    <h3 className="font-bold text-lg text-slate-900 mb-1 line-clamp-1">{book.title}</h3>
                    <p className="text-xs font-bold text-blue-500 uppercase tracking-widest mb-4">By {book.author}</p>
                    <p className="text-sm text-slate-500 leading-relaxed line-clamp-3 mb-6">{book.description}</p>
                    <a 
                      href={book.book_url} 
                      target="_blank" 
                      className="inline-flex items-center gap-2 text-xs font-bold text-slate-400 hover:text-blue-600 transition-colors"
                    >
                      <ExternalLink size={14} /> SOURCE REPOSITORY
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          /* --- AI ASSISTANT VIEW --- */
          <div className="max-w-3xl mx-auto animate-in slide-in-from-bottom-4 duration-500">
            <div className="text-center mb-10">
              <div className="inline-flex bg-blue-100 p-3 rounded-2xl text-blue-600 mb-4">
                <MessageSquare size={32} />
              </div>
              <h2 className="text-3xl font-black text-slate-800">Intelligence Nexus</h2>
              <p className="text-slate-500 font-medium">Ask questions across your entire library</p>
            </div>

            <form onSubmit={handleQuery} className="mb-10">
              <div className="flex gap-3 bg-white p-2 rounded-2xl border-2 border-slate-200 shadow-sm focus-within:border-blue-500 transition-all">
                <input 
                  type="text"
                  placeholder="e.g., What are the main themes of biology in these books?"
                  className="flex-1 p-3 outline-none bg-transparent font-medium"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <button 
                  disabled={loading || !query}
                  className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 disabled:bg-slate-300 transition flex items-center gap-2 font-bold shadow-lg"
                >
                  {loading ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
                  {loading ? "Analyzing..." : "Query AI"}
                </button>
              </div>
            </form>

            {result && (
              <div className="bg-white rounded-3xl border border-blue-100 shadow-2xl p-8 animate-in zoom-in-95 duration-300">
                <div className="flex items-center gap-2 mb-6 text-blue-600">
                  <div className="h-2 w-2 rounded-full bg-blue-600 animate-pulse"></div>
                  <span className="text-xs font-black uppercase tracking-widest">Synthetic Analysis</span>
                </div>
                <div className="prose prose-slate max-w-none">
                  <p className="text-slate-800 text-lg leading-relaxed whitespace-pre-wrap font-medium">
                    {result.result}
                  </p>
                </div>
                
                {result.sources && result.sources.length > 0 && (
                  <div className="mt-8 pt-6 border-t border-slate-100">
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-3">Contextual Origins</p>
                    <div className="flex flex-wrap gap-2">
                      {result.sources.map((src, idx) => (
                        <span key={idx} className="text-[11px] bg-slate-50 text-slate-600 border border-slate-200 px-3 py-1 rounded-full font-bold">
                          {src}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default App;