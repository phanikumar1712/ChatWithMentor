// import NavLinks from "./NavLinks";
// import CategoryMenu from "./CategoryMenu";
// import HeaderCTA from "./HeaderCTA";

// export default function Header() {
//   return (
//     <header className="sticky top-0 z-50 bg-white/80 backdrop-blur border-b border-gray-200">
//       <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        
//         {/* Brand */}
//         <div className="flex flex-col">
//           <span className="text-2xl font-bold text-indigo-600 tracking-tight">
//             AI Mentor
//           </span>
//           <span className="text-xs text-gray-500">
//             Wisdom across time, one conversation at a time
//           </span>
//         </div>

//         {/* Navigation */}
//         <div className="hidden md:flex items-center gap-8">
//           <NavLinks />
//           <CategoryMenu />
//         </div>

//         {/* CTA */}
//         <HeaderCTA />
//       </div>
//     </header>
//   );
// }


// src/components/header/Header.jsx
import NavLinks from "./NavLinks";
import CategoryMenu from "./CategoryMenu";
import AboutMentorsButton from "./AboutMentorsButton"; // ← New import

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        
        {/* Brand */}
        <div className="flex flex-col">
          <span className="text-2xl font-bold text-indigo-600 tracking-tight">
            AI Mentor
          </span>
          <span className="text-xs text-gray-500">
            Wisdom across time, one conversation at a time
          </span>
        </div>

        {/* Navigation - visible on medium+ screens */}
        <div className="hidden md:flex items-center gap-8">
          <NavLinks />
          <CategoryMenu />
        </div>

        {/* New Button on Top Right */}
        <AboutMentorsButton />
      </div>
    </header>
  );
}