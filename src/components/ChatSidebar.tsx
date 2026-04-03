import { useState } from "react";
import { MessageSquare, Plus, Zap } from "lucide-react";

const ChatSidebar = () => {
  return (
    <aside className="w-72 bg-sidebar border-l border-sidebar-border flex flex-col h-full">
      {/* Header */}
      <div className="p-3">
        <div className="flex items-center gap-2 justify-end mb-4 px-2 pt-2">
          <div className="text-right">
            <h1 className="text-sm font-bold text-foreground">ذكي AI</h1>
            <p className="text-xs text-muted-foreground">مبرمج ذكي بلا حدود</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
            <Zap className="w-4 h-4 text-primary" />
          </div>
        </div>

        <button className="w-full flex items-center justify-center gap-2 bg-primary text-primary-foreground rounded-xl py-2.5 text-sm font-medium hover:brightness-110 transition-all active:scale-[0.97]">
          <span>محادثة جديدة</span>
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* Empty chat list */}
      <div className="flex-1 overflow-y-auto scrollbar-thin px-2">
        <p className="text-center text-muted-foreground text-xs mt-8">لا توجد محادثات بعد</p>
      </div>

      {/* Footer */}
      <div className="p-3 border-t border-sidebar-border">
        <div className="flex items-center justify-center gap-1 text-xs">
          <span className="text-amber-400">⚡</span>
          <span className="text-muted-foreground">ذكي AI</span>
        </div>
      </div>
    </aside>
  );
};

export default ChatSidebar;
