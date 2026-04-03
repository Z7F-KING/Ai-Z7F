import { Sparkles, Bot, Code, Zap } from "lucide-react";

const suggestions = [
  {
    icon: Bot,
    text: "اسوي لي بوت Discord",
    gradient: "from-blue-500/10 to-blue-600/5",
    delay: "0ms",
  },
  {
    icon: Code,
    text: "اكتب لي موقع HTML",
    gradient: "from-primary/10 to-accent/5",
    delay: "100ms",
  },
  {
    icon: Zap,
    text: "اشرح لي React",
    gradient: "from-yellow-500/10 to-orange-500/5",
    delay: "200ms",
  },
];

const WelcomeScreen = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center px-4 animate-fade-in-up">
      {/* Icon */}
      <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/10 flex items-center justify-center mb-6 animate-float animate-glow-pulse">
        <Sparkles className="w-9 h-9 text-primary" />
      </div>

      {/* Title */}
      <h2 className="text-2xl font-bold mb-3 bg-gradient-to-l from-primary to-accent bg-clip-text text-transparent">
        مرحباً بك في ذكي AI
      </h2>

      {/* Subtitle */}
      <p className="text-muted-foreground text-sm max-w-md leading-relaxed mb-8">
        مبرمج ذكي يقدر يسوي لك أي شيء — مواقع، بوتات، سكربتات، أدوات. جرب اسألني! 🚀
      </p>

      {/* Suggestion buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full max-w-lg">
        {suggestions.map((s, i) => (
          <button
            key={i}
            style={{ animationDelay: s.delay }}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl bg-gradient-to-br ${s.gradient} border border-border/50 text-sm text-foreground hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5 active:scale-[0.97] transition-all duration-200`}
          >
            <s.icon className="w-[18px] h-[18px] text-primary shrink-0" />
            <span>{s.text}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default WelcomeScreen;
