import { useState } from "react";
import { Send, Brain } from "lucide-react";

const ChatInput = () => {
  const [message, setMessage] = useState("");
  const [thinkingMode, setThinkingMode] = useState(false);

  return (
    <div className="border-t border-border p-3 md:p-4" style={{ direction: "rtl" }}>
      <div className="max-w-3xl mx-auto">
        <div className="flex items-end gap-2 bg-secondary rounded-2xl p-2">
          <textarea
            placeholder="اكتب رسالتك هنا..."
            rows={1}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-1 bg-transparent resize-none outline-none text-sm placeholder:text-muted-foreground py-2 px-3 max-h-40 scrollbar-thin text-foreground"
            style={{ height: "36px" }}
          />
          <div className="flex items-center gap-1 pb-1">
            <button
              title="تفعيل وضع التفكير"
              onClick={() => setThinkingMode(!thinkingMode)}
              className={`p-2 rounded-lg transition-all duration-150 active:scale-95 ${
                thinkingMode
                  ? "text-primary bg-primary/10"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              <Brain className="w-[18px] h-[18px]" />
            </button>
            <button
              disabled={!message.trim()}
              className="p-2 rounded-lg bg-primary text-primary-foreground hover:brightness-110 active:scale-95 transition-all duration-150 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <Send className="w-[18px] h-[18px]" />
            </button>
          </div>
        </div>
        <div className="flex items-center justify-between mt-2 px-1">
          <span className="text-xs text-muted-foreground"></span>
          <span className="text-xs text-muted-foreground">Shift + Enter لسطر جديد</span>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
