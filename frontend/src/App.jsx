import { useEffect, useState } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";
import { getDashboardStats } from "./api";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function checkAuth() {
      const token = localStorage.getItem("token");

      if (!token) {
        if (isMounted) {
          setLoggedIn(false);
          setCheckingAuth(false);
        }
        return;
      }

      try {
        // any protected call works as auth check
        await getDashboardStats(token);
        if (isMounted) setLoggedIn(true);
      } catch (err) {
        console.error("Auth check failed", err);
        localStorage.removeItem("token");
        if (isMounted) setLoggedIn(false);
      } finally {
        if (isMounted) setCheckingAuth(false);
      }
    }

    checkAuth();

    return () => {
      isMounted = false;
    };
  }, []);

  if (checkingAuth) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-gray-900 text-white">
        Checking authentication…
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-gray-900 flex items-center justify-center">
      {loggedIn ? (
        <Dashboard
          onLogout={() => {
            localStorage.removeItem("token");
            setLoggedIn(false);
          }}
        />
      ) : (
        <Login onLogin={() => setLoggedIn(true)} />
      )}
    </div>
  );
}
