import Link from 'next/link';
import { ScrollArea } from '@radix-ui/react-scroll-area';
import { Button } from '../ui/button';
// Import icons later (e.g., from lucide-react)
// import { Home, Gamepad2, Image, Briefcase } from 'lucide-react';

const Sidebar = () => {
  // Placeholder navigation items
  const navItems = [
    { href: '/', label: 'Dashboard' /*, icon: Home */ },
    { href: '/minigames', label: 'Minigames' /*, icon: Gamepad2 */ },
    { href: '/memes', label: 'Meme Gallery' /*, icon: Image */ },
    { href: '/portfolio', label: 'Portfolio' /*, icon: Briefcase */ },
    // Add more items as needed
  ];

  return (
    <div className="flex h-full max-h-screen flex-col gap-2"> {/* Full height, vertical gap */}
      {/* Logo/Header Area */}
      <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          {/* Replace with your Logo/Icon */}
          <span className="text-lg font-bold tracking-tight text-primary">MECH OS</span>
          {/* <YourLogoComponent className="h-6 w-6" /> */}
          {/* <span className="">Your Site Name</span> */}
        </Link>
        {/* Optional: Add a small button or icon here */}
      </div>

      {/* Navigation Area */}
      <ScrollArea className="flex-1 px-3 py-4"> {/* Takes remaining space, scrollable */}
        <nav className="grid items-start gap-1 text-sm font-medium">
          {navItems.map((item) => (
            <Link key={item.label} href={item.href}>
              {/* Use ShadCN Button with variant="ghost" for link appearance */}
              <Button variant="ghost" className="w-full justify-start gap-2">
                {/* {item.icon && <item.icon className="h-4 w-4" />} */}
                {item.label}
              </Button>
            </Link>
          ))}
        </nav>
      </ScrollArea>

      {/* Optional: Footer Area in Sidebar (e.g., User info, Settings link) */}
      {/* <div className="mt-auto p-4 border-t">
        <p>User Info / Settings</p>
      </div> */}
    </div>
  );
};

export default Sidebar;