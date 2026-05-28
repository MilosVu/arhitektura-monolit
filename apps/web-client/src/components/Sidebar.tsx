import { NavLink } from "react-router-dom";

const links = [
  { to: "/cases", label: "Cases" },
  { to: "/laws", label: "Laws" },
  { to: "/system", label: "System" },
  { to: "/audit", label: "Audit Log" },
];

export default function Sidebar() {
  return (
    <aside className="w-56 border-r border-slate-200 bg-slate-900 text-white">
      <div className="border-b border-slate-700 px-4 py-5">
        <h1 className="text-lg font-bold tracking-tight">Cortex AI</h1>
        <p className="text-xs text-slate-400">MVP Mockup</p>
      </div>
      <nav className="flex flex-col gap-1 p-3">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `rounded px-3 py-2 text-sm transition-colors ${
                isActive ? "bg-blue-600 text-white" : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
