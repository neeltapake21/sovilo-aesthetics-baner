import { Link, NavLink } from "react-router-dom";
import { CalendarDays, Menu, Phone } from "lucide-react";
import { useState } from "react";
import { useAuth } from "../../contexts/AuthContext";

const navItems = [
  { to: "/", label: "Home" },
  { to: "/services", label: "Services" },
  { to: "/about", label: "About Us" },
  { to: "/contact", label: "Contact" },
];

export function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed inset-x-0 top-0 z-40 border-b border-gray-200 bg-white/80 backdrop-blur">
      <div className="container-xl flex h-20 items-center justify-between">
        <Link to="/" className="flex flex-col">
          <span className="font-heading italic text-2xl font-semibold tracking-tight text-primary">
            Sovilo Aesthetics Baner
          </span>
          <span className="text-xs text-gray-500">Laser Therapy By Doctor&apos;s</span>
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  "text-sm font-medium transition-colors",
                  isActive ? "text-primary" : "text-gray-700 hover:text-primary",
                ].join(" ")
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="hidden items-center gap-3 md:flex">
          <a
            href="tel:8177955821"
            className="inline-flex items-center gap-2 rounded-full border border-primary px-3 py-1.5 text-sm font-semibold text-primary hover:bg-primary/5"
          >
            <Phone className="h-4 w-4" />
            8177955821
          </a>
          <Link
            to="/contact"
            className="inline-flex items-center gap-2 rounded-full bg-primary px-4 py-1.5 text-sm font-semibold text-white shadow hover:bg-primary-light"
          >
            <CalendarDays className="h-4 w-4" />
            Book Now
          </Link>

          {/* Auth buttons */}
          <AuthButtons />
        </div>

        <button
          className="inline-flex items-center justify-center rounded-full border border-gray-200 p-2 md:hidden"
          onClick={() => setOpen((v) => !v)}
          aria-label="Toggle navigation"
        >
          <Menu className="h-5 w-5 text-charcoal" />
        </button>
      </div>

      {open && (
        <div className="border-t border-gray-200 bg-white md:hidden">
          <nav className="container-xl flex flex-col gap-2 py-4">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className="py-2 text-sm font-medium text-charcoal"
                onClick={() => setOpen(false)}
              >
                {item.label}
              </NavLink>
            ))}
            <a
              href="tel:8177955821"
              className="mt-2 inline-flex items-center gap-2 rounded-full border border-primary px-4 py-2 text-sm font-semibold text-primary"
            >
              <Phone className="h-4 w-4" />
              Call: 8177955821
            </a>
            <Link
              to="/contact"
              className="mt-2 inline-flex items-center justify-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-semibold text-white"
              onClick={() => setOpen(false)}
            >
              <CalendarDays className="h-4 w-4" />
              Book Appointment
            </Link>
            <div className="mt-2 flex gap-2">
              <Link to="/signin" onClick={() => setOpen(false)} className="px-3 py-2">
                Sign in
              </Link>
              <Link to="/signup" onClick={() => setOpen(false)} className="px-3 py-2">
                Sign up
              </Link>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}

function AuthButtons() {
  const { user, signout } = useAuth();

  if (user) {
    return (
      <div className="flex items-center gap-2">
        <span className="text-sm">{user.email || "Account"}</span>
        <button onClick={signout} className="rounded border px-3 py-1 text-sm">
          Logout
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <Link to="/signin" className="text-sm font-medium text-gray-700 hover:text-primary">
        Sign in
      </Link>
      <Link to="/signup" className="inline-flex items-center gap-2 rounded-full bg-primary px-3 py-1.5 text-sm font-semibold text-white">
        Sign up
      </Link>
    </div>
  );
}

