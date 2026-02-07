import { useEffect, useState } from "react";

import {
  Shield,
  AlertTriangle,
  Activity,
  Globe,
  Server,
  Search
} from "lucide-react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function SentinelShieldDashboard() {

  const [stats, setStats] = useState({
    totalRequests: 0,
    blocked: 0,
    allowed: 0,
    highRisk: 0
  });

  const [events, setEvents] = useState([]);
  const [filter, setFilter] = useState("");

  // -----------------------------
  // Auto Refresh (5 seconds)
  // -----------------------------
  useEffect(() => {
    const fetchData = () => {

      fetch("http://localhost:5000/api/stats")
        .then(res => res.json())
        .then(data => setStats(data));

      fetch("http://localhost:5000/api/events")
        .then(res => res.json())
        .then(data => setEvents(data));
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  // -----------------------------
  // Ban IP
  // -----------------------------
  function banIP(ip) {
    fetch("http://localhost:5000/api/ban_ip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ip })
    })
      .then(res => res.json())
      .then(data => alert("IP Banned: " + data.ip));
  }

  // -----------------------------
  // Filters
  // -----------------------------
  const filteredEvents = events.filter(e =>
    e.ip.includes(filter) ||
    e.reasons.join(" ").toLowerCase().includes(filter.toLowerCase())
  );

  const chartData = events.slice(-20).map((e, i) => ({
    name: i,
    score: e.score
  }));

  // -----------------------------
  // UI
  // -----------------------------
  return (
    <div className="flex min-h-screen bg-gray-950 text-gray-100">

      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 p-6 border-r border-gray-800">
        <div className="flex items-center gap-2 mb-10">
          <Shield className="text-green-400" />
          <h2 className="text-xl font-bold">SentinelShield</h2>
        </div>

        <nav className="space-y-4">
          <MenuItem icon={<Server />} label="Dashboard" />
          <MenuItem icon={<Activity />} label="Live Events" />
          <MenuItem icon={<AlertTriangle />} label="Alerts" />
          <MenuItem icon={<Globe />} label="Traffic" />
        </nav>
      </aside>

      {/* Main */}
      <main className="flex-1 p-8">

        {/* Top Bar */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Security Operations Center</h1>

          <div className="flex items-center gap-2 bg-gray-900 px-3 py-2 rounded-xl">
            <Search size={16} />
            <input
              className="bg-transparent outline-none"
              placeholder="Search IP / Attack"
              value={filter}
              onChange={e => setFilter(e.target.value)}
            />
          </div>
        </div>

        {/* Stat Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
          <StatCard title="Total Requests" value={stats.totalRequests} />
          <StatCard title="Blocked Attacks" value={stats.blocked} color="red" />
          <StatCard title="Allowed Requests" value={stats.allowed} color="green" />
          <StatCard title="High Risk" value={stats.highRisk} color="yellow" />
        </div>

        {/* Chart */}
        <div className="bg-gray-900 rounded-2xl p-6 mb-10 shadow-xl">
          <h2 className="text-lg font-semibold mb-4">Risk Score Trend</h2>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="score" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Events Table */}
        <div className="bg-gray-900 rounded-2xl p-6 shadow-xl">
          <h2 className="text-lg font-semibold mb-4">Recent Security Events</h2>

          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-700 text-gray-400">
                <th className="py-2">Time</th>
                <th>IP</th>
                <th>Reason</th>
                <th>Score</th>
                <th>Action</th>
                <th>Control</th>
              </tr>
            </thead>

            <tbody>
              {filteredEvents.map((e, i) => (
                <tr key={i} className="border-b border-gray-800 hover:bg-gray-800">

                  <td className="py-2">{e.timestamp}</td>
                  <td>{e.ip}</td>
                  <td>{e.reasons.join(", ")}</td>
                  <td>{e.score}</td>

                  <td>
                    <span
                      className={`px-3 py-1 rounded-full text-sm ${
                        e.action === "BLOCK"
                          ? "bg-red-600"
                          : e.action === "LOG"
                          ? "bg-yellow-600"
                          : "bg-green-600"
                      }`}
                    >
                      {e.action}
                    </span>
                  </td>

                  <td>
                    <button
                      className="px-2 py-1 bg-red-800 rounded text-xs hover:bg-red-700"
                      onClick={() => banIP(e.ip)}
                    >
                      Ban IP
                    </button>
                  </td>

                </tr>
              ))}
            </tbody>

          </table>
        </div>

      </main>
    </div>
  );
}

// -----------------------------
// Components
// -----------------------------

function MenuItem({ icon, label }) {
  return (
    <div className="flex items-center gap-3 text-gray-300 hover:text-white cursor-pointer">
      {icon}
      <span>{label}</span>
    </div>
  );
}

function StatCard({ title, value, color }) {

  const colorMap = {
    red: "text-red-400",
    green: "text-green-400",
    yellow: "text-yellow-400"
  };

  return (
    <div className="bg-gray-900 p-6 rounded-2xl shadow-xl">
      <p className="text-gray-400 text-sm">{title}</p>
      <h2 className={`text-3xl font-bold ${colorMap[color] || "text-white"}`}>
        {value}
      </h2>
    </div>
  );
}
