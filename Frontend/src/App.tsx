import React, { useState } from "react";
import { Search, Image as ImageIcon, Loader2, Download } from "lucide-react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [images, setImages] = useState<
    { image_path: string; caption: string }[]
  >([]);
  const [loading, setLoading] = useState(false);

  const searchImages = async (searchTerm: string) => {
    setLoading(true);
    try {
      const res = await fetch(
        `http://localhost:8000/search?query=${encodeURIComponent(searchTerm)}`
      );
      const data = await res.json();

      const imageUrls = data.map(
        (item: { image_path: string; caption: string }) => ({
          url: `http://localhost:8000/images/${item.image_path}`,
          caption: item.caption,
        })
      );
      console.log(imageUrls);

      setImages(imageUrls);
    } catch (err) {
      console.error("Error fetching images:", err);
      setImages([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      searchImages(prompt);
    }
  };

  return (
    <div className="min-h-screen bg-[#0F172A] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="flex flex-col items-center justify-center mb-16 text-center">
          <div className="bg-indigo-500/10 p-3 rounded-2xl mb-4">
            <ImageIcon className="w-8 h-8 text-indigo-400" />
          </div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400 mb-3">
            ImageFinder
          </h1>
          <p className="text-slate-400 max-w-md">AI-powered image search</p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto mb-16">
          <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
            <div className="relative flex items-center">
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter your image prompt..."
                className="w-full px-6 py-4 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-transparent transition-all duration-300"
              />
              <button
                type="submit"
                className="absolute right-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-6 py-2 rounded-lg transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-indigo-500/25"
              >
                <Search className="w-5 h-5" />
              </button>
            </div>
          </div>
        </form>

        {/* Results */}
        <div className="max-w-7xl mx-auto">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-12 gap-4">
              <Loader2 className="w-8 h-8 animate-spin text-indigo-400" />
              <p className="text-slate-400">Searching for amazing images...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {images.map((img, index) => (
                <div
                  key={index}
                  className="group relative overflow-hidden rounded-xl bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 transition-all duration-500 hover:scale-[1.02] hover:shadow-xl hover:shadow-indigo-500/10"
                >
                  <img
                    src={img.url} // assumes FastAPI serves images from /data/images/
                    //alt={img.caption}
                    className="w-full h-72 object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/50 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300">
                    <div className="absolute bottom-0 left-0 right-0 p-6">
                      <a
                        href={img.url}
                        download
                        className="w-full bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white px-4 py-3 rounded-lg flex items-center justify-center gap-2 transition-all duration-300 transform hover:scale-105"
                      >
                        <Download className="w-5 h-5" />
                        <span>Download Image</span>
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
