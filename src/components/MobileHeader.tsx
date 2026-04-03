import { Menu, Sparkles } from "lucide-react";

interface MobileHeaderProps {
  onMenuToggle: () => void;
}

const MobileHeader = ({ onMenuToggle }: MobileHeaderProps) => {
  return (
    <header className="flex items-center justify-between px-4 py-3 border-b border-border">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
          <Sparkles className="w-4 h-4 text-primary" />
        </div>
        <div className="text-right">
          <h1 className="text-sm font-bold text-foreground">ذكي AI</h1>
          <p className="text-xs text-muted-foreground">مبرمج ذكي بلا حدود</p>
        </div>
      </div>
      <button
        onClick={onMenuToggle}
        className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
      >
        <Menu className="w-5 h-5" />
      </button>
    </header>
  );
};

export default MobileHeader;
