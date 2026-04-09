import React, { useRef } from "react";
import { useState } from "react";
import ChartsSection from "./components/chartsection";
import { scanRepo,scanFile,scanGlobal,scanText } from "./services/api";
import toast from "react-hot-toast";
import { Toaster } from "react-hot-toast";

export default function App() {
  const [activeTab,setactiveTab] = useState("Text");
  const tabs=["Text","File","Repo","Global"];

  const sampleresults=[
    {
      secret:"sk_test_***abcd",
      type:"OPENAI_KEY",
      risk:"HIGH",
      confidence:0.95,
      source:"Text",
      reason:"High entropy, production context",
   }
  ]
  const [input,setinput]=useState("");
  const [file,setfile]=useState(null);
  const [Loading,setLoading]=useState(false);
  const [results,setresults] = useState([]);
  const [filter ,setfilter] = useState("All");
  const [message,setmessage]=useState("");

  const filteredresults = filter==="All"?results:results.filter(r=>r.risk===filter);
  const filters=['All','HIGH','MEDIUM','LOW'];
  const resultsRef=useRef(null);

  const handleScan = async () => {
  setLoading(true);
    console.log("activetab:", activeTab)
 
  try {
     let response;
    if (activeTab === "Text") {
      response = await scanText(input);
    }

    else if (activeTab === "File") {
      response = await scanFile(file);
    }

    else if (activeTab === "Repo") {
      response = await scanRepo(input);
    }

    else if (activeTab === "Global") {
      response = await scanGlobal(10);
    }

    if(!response) {
      toast.error("Server error")
      throw new Error("No Response From server");
    }

    if (response?.error) {
      toast.error(response.error);
    } else {
      setresults(response.results || []);
      toast.success("scan completed successfully! scroll down to see results");
      setTimeout(()=>{
        resultsRef.current?.scrollIntoView({behavior:"smooth"});
      },100);
      
    }

  } catch (err) {
    console.error(err);
    toast.error("Something went wrong!")
    setresults([]);
  }

  setLoading(false);
};

  const converToCSV=(data)=>{
    if(!data||data.length==0) return "";
    const headers=Object.keys(data[0]);
    const rows=data.map(obj=> headers.map(h=>`"${obj[h] ?? ""}"`).join(","));
    return [headers.join(","), ...rows].join("\n");
  }

  const downloadCSV=(data,filename)=>{
   if(!data||data.length==0) {
    alert("No data found");
    return;
   }
   const csv=converToCSV(data);
   const blob=new Blob([csv],{type:"text/csv;charset=utf-8;"});
   const link=document.createElement("a");
   link.href=URL.createObjectURL(blob);
   link.download=filename;
   link.click();
  };

  

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white  ">

      <nav className="w-full bg-gray-900 text-white px-12 py-4 flex items-center justify-between shadow-md sticky top-0 z-50">
          <h1 className="text-xl font-bold tracking-wide">
            DetectLeaks
          </h1>
          <div className=" text-sm text-gray-400">
            Secrets scanner
          </div>
      </nav>
      <Toaster position="top-right" reverseOrder={false}/>

      {/* Hero */}
      <section className="hero w-full max-w-6xl mx-auto  pt-24 pb-8 text-center ">
              <div className="Hero bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl shadow-2xl px-6 py-16 ">

              <div className="text-center">
                <h1 className="text-4xl font-bold  text-center bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-4">Secret Leak Detection Platform</h1>
                <p className="text-gray-400 text-lg mb-8"> Detect exposed credentials across text,files,repositories and global sources</p>
              </div>

            {/* Tabs */}

              <div className="tabs flex flex-wrap justify-center mt-16 mb-6 gap-4">
                {tabs.map((tab) => (
                  <button
                    key={tab}
                    onClick={()=> setactiveTab(tab)}
                    className={`px-4 py-2 rounded-full font-medium transition ${activeTab===tab?"bg-blue-600 text-white shadow-lg":"bg-white/10 text-gray-300 hover:bg-white/20"}`}
                  >
                    {tab} Scan
                  </button>
                ))}
              </div>

              {/* Input section */}

              <div className="max-w-3xl mx-auto mt-8 bg-white p-6 rounded-xl shadow">
                {activeTab === "Text" && (
                  <textarea
                  value={input} onChange={(e)=> setinput(e.target.value)}
                    className="w-full h-40 p-4 rounded-xl bg-gray-900 text-white border border-gray-600 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Paste your text here..."
                  ></textarea>
                )}
                
                {activeTab === "File" && (
                  <input type="file" onChange={(e)=>setfile(e.target.files[0])} className="w-full  p-4 rounded-xl bg-gray-900 text-white border border-gray-600 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Select your file"/>
                )}
                
                {activeTab === "Repo" && (
                  <input type="text" value={input} onChange={(e)=>setinput(e.target.value)} className="w-full p-4 rounded-xl bg-gray-900 text-white border border-gray-600 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter Github repo Url">
                  </input>
                )}
                
                {activeTab === "Global" && (
                  <h2 className="text-center text-xl text-gray-500 font-semibold mb-2">Run a global scan across public sources</h2>
                )}
                <div className="flex justify-center">
                  <button onClick={handleScan} className="mt-4 px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl shadow-lg transition text-lg font-semibold">
                  {Loading?"Scanning...": "Run Scan"}
                </button>
                </div>
              </div>



            </div>
      </section>

         {/* Results */}

      <section ref={resultsRef} className="results mt-4 max-w-6xl mx-auto px-6 py-16">
            <h2 className="text-3xl font-bold text-center">Scan results</h2>
                      {/* Alerts */}
                    <div className="alerts space-y-4 ">
                      <h2 className="text-2xl my-4 font-semibold text-center bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-4">Alerts</h2>
                      <div className=" flex flex-col gap-4">
                      {
                        results.some((r)=>r.risk==="HIGH")?(
                          results.filter(r=>r.risk==="HIGH").map((r,index)=>(
                            <div key={index} className="bg-red-500/20 border border-red-500 p-4 rounded-lg text-red-300">
                              {r.type} detected | Risk: {r.risk} <br/>
                              <span className="text-sm text-red-200">{r.reason}</span>
                            </div>
                        ))
                      ):(
                        <div className="text-green-400"> No Critical alerts</div>
                      )
                      }
                      </div>

                    </div>

                      {/* filters + Resultcards*/}
                  <div className="">
                    <h2 className="text-2xl font-semibold text-center bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent my-4">Results</h2>
                  <div className="flex gap-3 justify-center my-6">
                      {
                      filters.map((level)=>(
                        <button key={level} onClick={()=>setfilter(level)} className={`px-4 py-2 rounded-full font-medium transition ${filter===level?"bg-blue-600 text-white shadow-lg":"bg-white/10 text-gray-300 hover:bg-white/20"}`}>
                          {level}
                        </button>
                      ))}
                  </div>

                      {/* Results cards*/}
                  <div className="resultcards space-y-4">
                    <div className="grid md:grid-cols-2 gap-6 m-6">
                    {
                      filteredresults.map((item,index)=>(
                        <div key={index} className="bg-white/10 border border-white/20 p-5 rounded-xl shadow-lg backdrop-blur">
                          <div className="flex justify-between items-center mb-2">
                            <h3 className="font-semibold text-lg"> {item.type}</h3>
                            <span className={`text-xs px-2 py-1 rounded ${
                            item.risk==="HIGH"?"bg-red-500 text-white":
                            item.risk==="MEDIUM"?"bg-yellow-500 text-white":
                            "bg-green-500 text-white"
                          }`}>
                              {item.risk}
                              </span>
                              </div>
                              <p className="text-gray-300 text-sm mb-2 break-all">{item.secret}</p>
                              <p className="text-sm text-gray-400 break-words">{item.reason}</p>
                              <p className="text-xs text-gray-500 mt-2 break-words">Source: {item.source} | Confidence: {(item.confidence*100).toFixed(1)}%</p>
                        </div>
                      ))
                    }


                  {filteredresults.length===0 && (
                    <div className="text-gray-500 text-center mt-10">No results matching the selected filter.</div>
                  )}

                  </div>
                  </div>
                </div>
        

    {/* Charts */}
  
    <ChartsSection data={filteredresults}/>
    
    {/* Download buttons */}
            <div className="max-w-6xl mx-auto px-6 py-16 text-center">

          <h2 className="text-3xl font-bold mb-10">
            Export Results
          </h2>

          <div className="flex flex-col md:flex-row justify-center gap-6">

            {/* FULL DOWNLOAD */}
            <button
              onClick={() => downloadCSV(results, "full_report.csv")}
              className="px-6 py-3 rounded-xl bg-green-500 hover:bg-green-600 transition shadow-lg"
            >
              Download Full Report
            </button>

            {/* FILTERED DOWNLOAD */}
            <button
              onClick={() => downloadCSV(filteredResults, "filtered_report.csv")}
              className="px-6 py-3 rounded-xl bg-blue-500 hover:bg-blue-600 transition shadow-lg"
            >
              Download Filtered Results
            </button>

          </div>

        </div>
    </section>

    

    </main>
  );
}