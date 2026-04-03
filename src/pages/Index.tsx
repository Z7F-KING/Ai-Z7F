import { useState } from "react";
import { Menu, X } from "lucide-react";
import ChatSidebar from "@/components/ChatSidebar";
import WelcomeScreen from "@/components/WelcomeScreen";
import ChatInput from "@/components/ChatInput";
import MobileHeader from "@/components/MobileHeader";

const Index = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen w-full overflow-hidden" style={{ direction: "rtl" }}>
      {/* Main content */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Mobile header */}
        <div className="lg:hidden">
          <MobileHeader onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
        </div>

        <div className="flex-1 overflow-y-auto scrollbar-thin">
          <WelcomeScreen />
        </div>
        <ChatInput />
      </main>

      {/* Sidebar - always visible on desktop */}
      <div className="hidden lg:block">
        <ChatSidebar />
      </div>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-50 flex" style={{ direction: "rtl" }}>
          <div className="absolute inset-0 bg-black/50" onClick={() => setSidebarOpen(false)} />
          <div className="relative mr-auto">
            <ChatSidebar />
          </div>
        </div>
      )}
    </div>
  );
};

export default Index;
