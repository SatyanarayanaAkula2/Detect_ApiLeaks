import { PieChart,Pie,Cell,Tooltip,ResponsiveContainer,BarChart,Bar,XAxis,YAxis,CartesianGrid } from "recharts";

const colors=["#ef4444","#f59e0b","#22c55e"];

const ChartsSection=({data})=>{
    if(!data ||data.length==0){
        return( <div className="mt-10 text-center text-gray-400">
            No data found for charts
        </div>
        );
    }

    const counts={
        HIGH:data.filter(d=>d.risk==="HIGH").length,
        MEDIUM:data.filter(d=>d.risk==="MEDIUM").length,
        LOW:data.filter(d=>d.risk==="LOW").length,
    };

    const chartData=[
        {name:"High",value:counts.HIGH},
        {name:"Medium",value:counts.MEDIUM},
        {name:"Low",value:counts.LOW}
    ];

    return (
    <div className="mt-12">
      
      {/* 🔥 Heading */}
      <h2 className="text-2xl font-semibold text-white mb-6 text-center">
        Risk Analysis
      </h2>

      {/* 🔥 Container */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 w-full">

        {/* 🥧 Pie Chart */}
        <div className="w-full bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6">
          <h3 className="text-lg text-gray-300 mb-4 text-center">
            Risk Distribution
          </h3>

          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                outerRadius={100}
                label
              >
                {chartData.map((entry, index) => (
                  <Cell key={index} fill={colors[index]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* 📊 Bar Chart */}
        <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6">
          <h3 className="text-lg text-gray-300 mb-4 text-center">
            Risk Count
          </h3>

          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis dataKey="name" stroke="#ccc" />
              <YAxis stroke="#ccc" />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

      </div>
    </div>
  );
};

export default ChartsSection;
